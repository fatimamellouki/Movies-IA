# backend/app.py
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime, timedelta
import bcrypt
import os
import threading
import time
from dotenv import load_dotenv
from offline.recommender import HybridRecommender
import traceback

# Charger les variables d'environnement
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'votre-cle-secrete-tres-longue')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
jwt = JWTManager(app)


# Connexion MongoDB
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/movie_recommender')
client = MongoClient(MONGO_URI)
db = client.movie_recommender

# Initialiser le recommandeur
recommender = HybridRecommender(db)

# Collection cache recommandations
recommendation_cache_col = db.recommendation_cache

# Initialiser le recommandeur
recommender = HybridRecommender(db)

# Collection MongoDB pour stocker les recommandations par utilisateur
recommendation_cache_col = db.recommendation_cache

# ----------------------- Helpers -----------------------
def get_user_from_token():
    """Récupérer l'utilisateur à partir du token JWT"""
    try:
        current_user_id = get_jwt_identity()
        if not current_user_id:
            return None
        return db.users.find_one({'_id': ObjectId(current_user_id)})
    except Exception as e:
        print(f"Erreur lors de la récupération de l'utilisateur: {e}")
        return None

def generate_user_id():
    """Générer un nouvel ID utilisateur numérique"""
    last_user = db.users.find_one(sort=[('user_id', -1)])
    if last_user and 'user_id' in last_user:
        return last_user['user_id'] + 1
    return 1

def get_cached_recommendations(user_id, user_object_id):
    """Retourne le cache si disponible, sinon génère cold-start"""
    cache_doc = recommendation_cache_col.find_one({'user_id': user_id})
    if cache_doc:
        return cache_doc['items'], cache_doc.get('user_type', 'existing')
    
    # Cold-start
    recommendations = recommender.recommend_for_new_user(user_object_id, top_n=30)
    recommendation_cache_col.update_one(
        {'user_id': user_id},
        {'$set': {'items': recommendations, 'user_type': 'new', 'updated_at': datetime.now(), 'ratings_count': 0, 'recomputing': False}},
        upsert=True
    )
    return recommendations, 'new'

def recalc_recommendations_if_needed(user):
    """Recalcule les recommandations en arrière-plan si nécessaire"""
    user_id = user['user_id']
    user_object_id = user['_id']
    ratings_count = db.ratings.count_documents({'user_id': user_id})
    
    cache_doc = recommendation_cache_col.find_one({'user_id': user_id})
    last_count = cache_doc.get('ratings_count', 0) if cache_doc else 0
    recomputing = cache_doc.get('recomputing', False) if cache_doc else False
    
    if (ratings_count - last_count) >= 3 and not recomputing:
        def background():
            try:
                recommendation_cache_col.update_one({'user_id': user_id}, {'$set': {'recomputing': True}}, upsert=True)
                if ratings_count == 0:
                    recs = recommender.recommend_for_new_user(user_object_id, top_n=30)
                    utype = 'new'
                else:
                    recs = recommender.recommend_for_existing_user(user_object_id, top_n=30)
                    utype = 'existing'
                recommendation_cache_col.update_one(
                    {'user_id': user_id},
                    {'$set': {'items': recs, 'user_type': utype, 'updated_at': datetime.now(), 'ratings_count': ratings_count, 'recomputing': False}},
                    upsert=True
                )
                print(f"✅ Recompute terminé pour user {user_id}")
            except Exception as e:
                print(f"⚠️ Erreur recompute user {user_id}: {e}")
                traceback.print_exc()
                recommendation_cache_col.update_one({'user_id': user_id}, {'$set': {'recomputing': False}})
        threading.Thread(target=background, daemon=True).start()
    

# Routes d'authentification
@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        # Vérifier si l'utilisateur existe
        existing_user = db.users.find_one({'email': data.get('email')})
        if existing_user:
            return jsonify({'message': 'Email déjà utilisé'}), 400
        
        # Hasher le mot de passe
        hashed_password = bcrypt.hashpw(
            data['password'].encode('utf-8'), 
            bcrypt.gensalt()
        )
        
        # Générer un nouvel user_id
        user_id = generate_user_id()
        
        # Créer un nouvel utilisateur
        new_user = {
            'user_id': user_id,
            'email': data['email'],
            'password': hashed_password.decode('utf-8'),
            'name': data.get('name', ''),
            'age': int(data.get('age', 25)),
            'gender': data.get('gender', 'M'),
            'occupation': data.get('occupation', 'other'),
            'created_at': datetime.now(),
            'preferences': {
                'genre_weights': {},
                'average_rating': 0,
                'rated_movies': []
            },
            'cluster_id': None
        }
        
        # Insérer dans la base de données
        result = db.users.insert_one(new_user)
        
        # Assigner un cluster
        try:
            recommender.assign_user_cluster(result.inserted_id)
        except Exception as e:
            print(f"Warning: Erreur lors de l'assignation du cluster: {e}")
        
        return jsonify({
            'message': 'Utilisateur créé avec succès',
            'user_id': user_id
        }), 201
    
    except Exception as e:
        print(f"Erreur d'inscription: {e}")
        traceback.print_exc()
        return jsonify({'message': f'Erreur serveur: {str(e)}'}), 500

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        # Trouver l'utilisateur
        user = db.users.find_one({'email': data['email']})
        if not user:
            return jsonify({'message': 'Email ou mot de passe incorrect'}), 401
        
        # Vérifier le mot de passe
        if not bcrypt.checkpw(data['password'].encode('utf-8'), user['password'].encode('utf-8')):
            return jsonify({'message': 'Email ou mot de passe incorrect'}), 401
        
        # Créer le token JWT
        access_token = create_access_token(identity=str(user['_id']))
        
        return jsonify({
            'access_token': access_token,
            'user': {
                'id': str(user['_id']),
                'user_id': user.get('user_id'),
                'email': user['email'],
                'name': user.get('name', ''),
                'age': user.get('age', 25),
                'gender': user.get('gender', 'M'),
                'occupation': user.get('occupation', 'other'),
                'cluster_id': user.get('cluster_id')
            }
        }), 200
    
    except Exception as e:
        print(f"Erreur de connexion: {e}")
        return jsonify({'message': str(e)}), 500

@app.route('/api/user/preferences', methods=['POST'])
@jwt_required()
def set_user_preferences():
    """Mettre à jour les genres préférés de l'utilisateur (après inscription)"""
    try:
        user = get_user_from_token()
        if not user:
            return jsonify({'message': 'Utilisateur non trouvé'}), 404

        data = request.get_json()
        genre_weights = data.get('genre_weights', {})

        # Stocker les poids de genres
        db.users.update_one(
            {'_id': user['_id']},
            {'$set': {'preferences.genre_weights': genre_weights}}
        )
        return jsonify({
            'message': 'Préférences enregistrées',
        }), 200

    except Exception as e:
        print(f"Erreur: {e}")
        traceback.print_exc()
        return jsonify({'message': str(e)}), 500


# Routes publiques (pas besoin d'authentification)
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()}), 200

@app.route('/api/movies/popular', methods=['GET'])
def get_popular_movies():
    """Films populaires pour la première connexion (sans authentification)"""
    try:
        movies = list(db.movies.find(
            {},
            {'_id': 0, 'movie_id': 1, 'title': 1, 'genres': 1, 'year': 1, 'bayesian_rating': 1}
        ).sort('bayesian_rating', -1).limit(20))
        
        return jsonify(movies), 200
    except Exception as e:
        print(f"Erreur: {e}")
        return jsonify({'message': str(e)}), 500


# Routes protégées
@app.route('/api/movies', methods=['GET'])
@jwt_required()
def get_movies():
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 20))
        skip = (page - 1) * limit
        
        movies = list(db.movies.find(
            {},
            {'_id': 0, 'movie_id': 1, 'title': 1, 'genres': 1, 'year': 1, 'bayesian_rating': 1}
        ).skip(skip).limit(limit))
        
        return jsonify(movies), 200
    
    except Exception as e:
        print(f"Erreur: {e}")
        return jsonify({'message': str(e)}), 500

@app.route('/api/movies/search', methods=['GET'])
@jwt_required()
def search_movies():
    try:
        query = request.args.get('q', '')
        
        movies = list(db.movies.find(
            {'title': {'$regex': query, '$options': 'i'}},
            {'_id': 0, 'movie_id': 1, 'title': 1, 'genres': 1, 'year': 1}
        ).limit(20))
        
        return jsonify(movies), 200
    
    except Exception as e:
        print(f"Erreur: {e}")
        return jsonify({'message': str(e)}), 500

# Routes de recommandation
# ----------------------- Recommandations -----------------------
@app.route('/api/recommendations', methods=['GET'])
@jwt_required()
def get_recommendations():
    try:
        start = time.time()
        user = get_user_from_token()
        if not user:
            return jsonify({'message': 'Utilisateur non trouvé'}), 404

        user_id = user['user_id']
        user_object_id = user['_id']
        ratings_count = db.ratings.count_documents({'user_id': user_id})

        # Retourne le cache si disponible
        cache_doc = recommendation_cache_col.find_one({'user_id': user_id})
        if cache_doc and cache_doc.get('items'):
            # Trigger recompute si nécessaire
            recalc_recommendations_if_needed(user)
            resp = {
                'recommendations': cache_doc['items'],
                'user_type': cache_doc.get('user_type', 'existing'),
                'ratings_count': ratings_count,
                'updated_at': cache_doc.get('updated_at').isoformat() if cache_doc.get('updated_at') else None,
                'recomputing': cache_doc.get('recomputing', False)
            }
            duration = time.time() - start
            print(f"/api/recommendations - returned cached for user {user_id} in {duration:.2f}s")
            return jsonify(resp), 200

        # Pas de cache: calcul en background + fallback
        def compute_and_store():
            try:
                recommendation_cache_col.update_one({'user_id': user_id}, {'$set': {'recomputing': True}}, upsert=True)
                if ratings_count == 0:
                    recs = recommender.recommend_for_new_user(user_object_id, top_n=30)
                    utype = 'new'
                else:
                    recs = recommender.recommend_for_existing_user(user_object_id, top_n=30)
                    utype = 'existing'
                recommendation_cache_col.update_one(
                    {'user_id': user_id},
                    {'$set': {'items': recs, 'user_type': utype, 'updated_at': datetime.now(), 'ratings_count': ratings_count, 'recomputing': False}},
                    upsert=True
                )
            except Exception as e:
                print(f"Error computing recommendations: {e}")
                traceback.print_exc()
                recommendation_cache_col.update_one({'user_id': user_id}, {'$set': {'recomputing': False}})
        threading.Thread(target=compute_and_store, daemon=True).start()

        # Fallback rapide aux films populaires
        movies = list(db.movies.find({}, {'_id':0, 'movie_id':1, 'title':1, 'genres':1, 'year':1, 'bayesian_rating':1}).sort('bayesian_rating', -1).limit(20))
        fallback = [{'movie_id': m['movie_id'], 'title': m['title'], 'genres': m.get('genres', []), 'year': m.get('year'), 'score': m.get('bayesian_rating',3.0), 'explanation':'Film populaire (fallback)'} for m in movies]
        duration = time.time() - start
        print(f"/api/recommendations - returned fallback for user {user_id} in {duration:.2f}s")
        return jsonify({'recommendations': fallback, 'user_type':'fallback', 'ratings_count': ratings_count, 'updated_at': None, 'recomputing': True}), 200

    except Exception as e:
        print(f"Erreur recommandations: {e}")
        traceback.print_exc()
        return jsonify({'message': str(e)}), 500


@app.route('/api/rate', methods=['POST'])
@jwt_required()
def rate_movie():
    try:
        user = get_user_from_token()
        if not user:
            return jsonify({'message':'Utilisateur non trouvé'}), 404

        data = request.get_json()
        movie_id = int(data['movie_id'])
        rating = float(data['rating'])
        if rating <1 or rating>5:
            return jsonify({'message':'La note doit être entre 1 et 5'}), 400

        rating_record = {'user_id': user['user_id'], 'movie_id': movie_id, 'rating': rating, 'timestamp': datetime.now()}
        db.ratings.update_one({'user_id': user['user_id'], 'movie_id': movie_id}, {'$set': rating_record}, upsert=True)

        # Mise à jour stats du film
        movie_ratings = list(db.ratings.find({'movie_id': movie_id}))
        if movie_ratings:
            avg_rating = sum(r['rating'] for r in movie_ratings)/len(movie_ratings)
            db.movies.update_one({'movie_id': movie_id}, {'$set': {'average_rating': avg_rating, 'ratings_count': len(movie_ratings), 'bayesian_rating': (len(movie_ratings)*avg_rating+10*3.0)/(len(movie_ratings)+10)}})

        # Update preferences et trigger recompute cache
        try:
            recommender.update_user_preferences(user['_id'])
            recalc_recommendations_if_needed(user)
        except Exception as e:
            print(f"Warning update preferences: {e}")

        return jsonify({'message':'Évaluation enregistrée','movie_id':movie_id,'rating':rating}), 200

    except Exception as e:
        print(f"Erreur rating: {e}")
        return jsonify({'message':str(e)}), 500

@app.route('/api/user/stats', methods=['GET'])
@jwt_required()
def get_user_stats():
    try:
        user = get_user_from_token()
        if not user:
            return jsonify({'message': 'Utilisateur non trouvé'}), 404
        
        # Récupérer les statistiques de l'utilisateur
        ratings_count = db.ratings.count_documents({'user_id': user['user_id']})
        
        return jsonify({
            'user_id': user['user_id'],
            'name': user.get('name', ''),
            'email': user['email'],
            'cluster_id': user.get('cluster_id'),
            'ratings_count': ratings_count,
            'preferences': user.get('preferences', {})
        }), 200
    
    except Exception as e:
        print(f"Erreur: {e}")
        return jsonify({'message': str(e)}), 500

# Routes d'administration
@app.route('/admin/run-offline', methods=['POST'])
def run_offline_calculations():
    """Exécuter les calculs offline (pour les tests)"""
    try:
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return jsonify({'message': 'Token manquant'}), 401
        
        token = auth_header.split(' ')[1]
        
        # Vérifier un token admin simple (pour les tests)
        if token != os.getenv('ADMIN_TOKEN', 'admin-secret-token'):
            return jsonify({'message': 'Accès non autorisé'}), 403
        
        # Exécuter tous les calculs offline
        recommender.run_offline_computations()
        
        return jsonify({'message': 'Calculs offline terminés'}), 200
    
    except Exception as e:
        print(f"Erreur: {e}")
        traceback.print_exc()
        return jsonify({'message': str(e)}), 500

@app.route('/admin/init-db', methods=['POST'])
def init_database():
    """Initialiser la base de données avec des données de test"""
    try:
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return jsonify({'message': 'Token manquant'}), 401
        
        token = auth_header.split(' ')[1]
        
        # Vérifier un token admin simple
        if token != os.getenv('ADMIN_TOKEN', 'admin-secret-token'):
            return jsonify({'message': 'Accès non autorisé'}), 403
        
        # Créer quelques films de test
        test_movies = [
            {
                'movie_id': 1,
                'title': 'The Shawshank Redemption',
                'year': 1994,
                'genres': ['Drama'],
                'bayesian_rating': 4.8,
                'ratings_count': 1000
            },
            {
                'movie_id': 2,
                'title': 'The Godfather',
                'year': 1972,
                'genres': ['Crime', 'Drama'],
                'bayesian_rating': 4.7,
                'ratings_count': 900
            },
            {
                'movie_id': 3,
                'title': 'The Dark Knight',
                'year': 2008,
                'genres': ['Action', 'Crime', 'Drama'],
                'bayesian_rating': 4.6,
                'ratings_count': 950
            },
            {
                'movie_id': 4,
                'title': 'Pulp Fiction',
                'year': 1994,
                'genres': ['Crime', 'Drama'],
                'bayesian_rating': 4.5,
                'ratings_count': 850
            },
            {
                'movie_id': 5,
                'title': 'Forrest Gump',
                'year': 1994,
                'genres': ['Drama', 'Romance'],
                'bayesian_rating': 4.4,
                'ratings_count': 800
            }
        ]
        
        # Insérer les films
        for movie in test_movies:
            db.movies.update_one(
                {'movie_id': movie['movie_id']},
                {'$set': movie},
                upsert=True
            )
        
        return jsonify({
            'message': 'Base de données initialisée avec des données de test',
            'movies_count': len(test_movies)
        }), 200
    
    except Exception as e:
        print(f"Erreur: {e}")
        return jsonify({'message': str(e)}), 500

# Routes de gestion du profil utilisateur
@app.route('/api/user/profile', methods=['GET'])
@jwt_required()
def get_user_profile():
    """Récupérer le profil complet de l'utilisateur"""
    try:
        user = get_user_from_token()
        if not user:
            return jsonify({'message': 'Utilisateur non trouvé'}), 404
        
        ratings_count = db.ratings.count_documents({'user_id': user['user_id']})
        
        return jsonify({
            'id': str(user['_id']),
            'user_id': user.get('user_id'),
            'email': user['email'],
            'name': user.get('name', ''),
            'age': user.get('age', 25),
            'gender': user.get('gender', 'M'),
            'occupation': user.get('occupation', 'other'),
            'cluster_id': user.get('cluster_id'),
            'created_at': user.get('created_at').isoformat() if user.get('created_at') else None,
            'ratings_count': ratings_count,
            'preferences': user.get('preferences', {})
        }), 200
    
    except Exception as e:
        print(f"Erreur: {e}")
        return jsonify({'message': str(e)}), 500

@app.route('/api/user/profile', methods=['PUT'])
@jwt_required()
def update_user_profile():
    """Mettre à jour le profil utilisateur"""
    try:
        user = get_user_from_token()
        if not user:
            return jsonify({'message': 'Utilisateur non trouvé'}), 404
        
        data = request.get_json()
        
        # Préparer les données à mettre à jour
        update_data = {}
        if 'name' in data:
            update_data['name'] = data['name']
        if 'age' in data:
            try:
                age = int(data['age'])
                if 1 <= age <= 120:
                    update_data['age'] = age
            except:
                pass
        if 'gender' in data and data['gender'].upper() in ['M', 'F', 'O']:
            update_data['gender'] = data['gender'].upper()
        if 'occupation' in data:
            update_data['occupation'] = data['occupation']
        
        # Mettre à jour la base de données
        if update_data:
            db.users.update_one({'_id': user['_id']}, {'$set': update_data})
        
        return jsonify({
            'message': 'Profil mis à jour avec succès',
            'updates': update_data
        }), 200
    
    except Exception as e:
        print(f"Erreur: {e}")
        return jsonify({'message': str(e)}), 500

@app.route('/api/user/account', methods=['DELETE'])
@jwt_required()
def delete_user_account():
    """Supprimer le compte utilisateur"""
    try:
        user = get_user_from_token()
        if not user:
            return jsonify({'message': 'Utilisateur non trouvé'}), 404
        
        user_id = user['user_id']
        
        # Supprimer toutes les données de l'utilisateur
        db.ratings.delete_many({'user_id': user_id})
        db.watchlist.delete_many({'user_id': user_id})
        db.users.delete_one({'_id': user['_id']})
        
        return jsonify({'message': 'Compte supprimé avec succès'}), 200
    
    except Exception as e:
        print(f"Erreur: {e}")
        return jsonify({'message': str(e)}), 500

# Routes de gestion des notations
@app.route('/api/user/ratings', methods=['GET'])
@jwt_required()
def get_user_ratings():
    """Récupérer toutes les notes de l'utilisateur"""
    try:
        user = get_user_from_token()
        if not user:
            return jsonify({'message': 'Utilisateur non trouvé'}), 404
        
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 20))
        skip = (page - 1) * limit
        
        # Récupérer les notes avec les détails des films
        ratings = list(db.ratings.find(
            {'user_id': user['user_id']}
        ).skip(skip).limit(limit).sort('timestamp', -1))
        
        # Enrichir avec les données des films
        enriched_ratings = []
        for rating in ratings:
            movie = db.movies.find_one({'movie_id': rating['movie_id']})
            if movie:
                enriched_ratings.append({
                    'movie_id': rating['movie_id'],
                    'rating': rating['rating'],
                    'timestamp': rating['timestamp'].isoformat() if rating.get('timestamp') else None,
                    'movie_title': movie.get('title'),
                    'movie_year': movie.get('year'),
                    'movie_genres': movie.get('genres', [])
                })
        
        total_ratings = db.ratings.count_documents({'user_id': user['user_id']})
        
        return jsonify({
            'ratings': enriched_ratings,
            'total': total_ratings,
            'page': page,
            'limit': limit
        }), 200
    
    except Exception as e:
        print(f"Erreur: {e}")
        return jsonify({'message': str(e)}), 500

@app.route('/api/rate/<int:movie_id>', methods=['DELETE'])
@jwt_required()
def delete_rating(movie_id):
    """Supprimer une note"""
    try:
        user = get_user_from_token()
        if not user:
            return jsonify({'message': 'Utilisateur non trouvé'}), 404
        
        # Supprimer la note
        db.ratings.delete_one({
            'user_id': user['user_id'],
            'movie_id': movie_id
        })
        
        # Mettre à jour les statistiques du film
        movie_ratings = list(db.ratings.find({'movie_id': movie_id}))
        if movie_ratings:
            avg_rating = sum(r['rating'] for r in movie_ratings) / len(movie_ratings)
            db.movies.update_one(
                {'movie_id': movie_id},
                {
                    '$set': {
                        'average_rating': avg_rating,
                        'ratings_count': len(movie_ratings),
                        'bayesian_rating': (len(movie_ratings) * avg_rating + 10 * 3.0) / (len(movie_ratings) + 10)
                    }
                }
            )
        else:
            # Pas de notes, réinitialiser
            db.movies.update_one(
                {'movie_id': movie_id},
                {
                    '$set': {
                        'average_rating': 0,
                        'ratings_count': 0,
                        'bayesian_rating': 3.0
                    }
                }
            )
        
        return jsonify({'message': 'Note supprimée avec succès'}), 200
    
    except Exception as e:
        print(f"Erreur: {e}")
        return jsonify({'message': str(e)}), 500

# Routes de détails des films
@app.route('/api/movies/<int:movie_id>', methods=['GET'])
@jwt_required()
def get_movie_details(movie_id):
    """Récupérer les détails complets d'un film"""
    try:
        movie = db.movies.find_one({'movie_id': movie_id}, {'_id': 0})
        
        if not movie:
            return jsonify({'message': 'Film non trouvé'}), 404
        
        # Récupérer la note de l'utilisateur s'il existe
        user = get_user_from_token()
        user_rating = None
        if user:
            rating_doc = db.ratings.find_one({
                'user_id': user['user_id'],
                'movie_id': movie_id
            })
            if rating_doc:
                user_rating = rating_doc['rating']
        
        # Récupérer la position dans la watchlist
        in_watchlist = False
        if user:
            watchlist_doc = db.watchlist.find_one({
                'user_id': user['user_id'],
                'movie_id': movie_id
            })
            in_watchlist = watchlist_doc is not None
        
        return jsonify({
            **movie,
            'user_rating': user_rating,
            'in_watchlist': in_watchlist
        }), 200
    
    except Exception as e:
        print(f"Erreur: {e}")
        return jsonify({'message': str(e)}), 500

@app.route('/api/movies/<int:movie_id>/ratings', methods=['GET'])
def get_movie_ratings_stats(movie_id):
    """Récupérer les statistiques de notes d'un film"""
    try:
        movie = db.movies.find_one({'movie_id': movie_id})
        
        if not movie:
            return jsonify({'message': 'Film non trouvé'}), 404
        
        # Calculer la distribution des notes
        ratings = list(db.ratings.find({'movie_id': movie_id}))
        
        rating_distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        for rating in ratings:
            rating_val = int(rating['rating'])
            if rating_val in rating_distribution:
                rating_distribution[rating_val] += 1
        
        return jsonify({
            'movie_id': movie_id,
            'title': movie.get('title'),
            'average_rating': movie.get('average_rating', 0),
            'ratings_count': movie.get('ratings_count', 0),
            'bayesian_rating': movie.get('bayesian_rating', 0),
            'rating_distribution': rating_distribution
        }), 200
    
    except Exception as e:
        print(f"Erreur: {e}")
        return jsonify({'message': str(e)}), 500

# Routes de gestion de la watchlist
@app.route('/api/watchlist', methods=['GET'])
@jwt_required()
def get_watchlist():
    """Récupérer la liste de suivi de l'utilisateur"""
    try:
        user = get_user_from_token()
        if not user:
            return jsonify({'message': 'Utilisateur non trouvé'}), 404
        
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 20))
        skip = (page - 1) * limit
        
        # Récupérer les films de la watchlist
        watchlist = list(db.watchlist.find(
            {'user_id': user['user_id']}
        ).skip(skip).limit(limit).sort('added_at', -1))
        
        # Enrichir avec les données des films
        enriched_watchlist = []
        for item in watchlist:
            movie = db.movies.find_one({'movie_id': item['movie_id']}, {'_id': 0})
            if movie:
                enriched_watchlist.append({
                    **movie,
                    'added_at': item['added_at'].isoformat() if item.get('added_at') else None
                })
        
        total_items = db.watchlist.count_documents({'user_id': user['user_id']})
        
        return jsonify({
            'watchlist': enriched_watchlist,
            'total': total_items,
            'page': page,
            'limit': limit
        }), 200
    
    except Exception as e:
        print(f"Erreur: {e}")
        return jsonify({'message': str(e)}), 500

@app.route('/api/watchlist', methods=['POST'])
@jwt_required()
def add_to_watchlist():
    """Ajouter un film à la watchlist"""
    try:
        user = get_user_from_token()
        if not user:
            return jsonify({'message': 'Utilisateur non trouvé'}), 404
        
        data = request.get_json()
        movie_id = int(data['movie_id'])
        
        # Vérifier que le film existe
        movie = db.movies.find_one({'movie_id': movie_id})
        if not movie:
            return jsonify({'message': 'Film non trouvé'}), 404
        
        # Ajouter à la watchlist (éviter les doublons)
        db.watchlist.update_one(
            {'user_id': user['user_id'], 'movie_id': movie_id},
            {
                '$set': {
                    'user_id': user['user_id'],
                    'movie_id': movie_id,
                    'added_at': datetime.now()
                }
            },
            upsert=True
        )
        
        return jsonify({
            'message': 'Film ajouté à la watchlist',
            'movie_id': movie_id
        }), 200
    
    except Exception as e:
        print(f"Erreur: {e}")
        return jsonify({'message': str(e)}), 500

@app.route('/api/watchlist/<int:movie_id>', methods=['DELETE'])
@jwt_required()
def remove_from_watchlist(movie_id):
    """Supprimer un film de la watchlist"""
    try:
        user = get_user_from_token()
        if not user:
            return jsonify({'message': 'Utilisateur non trouvé'}), 404
        
        # Supprimer de la watchlist
        db.watchlist.delete_one({
            'user_id': user['user_id'],
            'movie_id': movie_id
        })
        
        return jsonify({'message': 'Film supprimé de la watchlist'}), 200
    
    except Exception as e:
        print(f"Erreur: {e}")
        return jsonify({'message': str(e)}), 500

# Routes d'administration supplémentaires
@app.route('/admin/stats', methods=['GET'])
def get_admin_stats():
    """Récupérer les statistiques globales (admin)"""
    try:
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return jsonify({'message': 'Token manquant'}), 401
        
        token = auth_header.split(' ')[1]
        
        # Vérifier le token admin
        if token != os.getenv('ADMIN_TOKEN', 'admin-secret-token'):
            return jsonify({'message': 'Accès non autorisé'}), 403
        
        # Récupérer les statistiques
        users_count = db.users.count_documents({})
        movies_count = db.movies.count_documents({})
        ratings_count = db.ratings.count_documents({})
        watchlist_count = db.watchlist.count_documents({})
        
        # Statistiques des films les plus notés
        top_movies = list(db.movies.find(
            {},
            {'_id': 0, 'movie_id': 1, 'title': 1, 'ratings_count': 1, 'bayesian_rating': 1}
        ).sort('bayesian_rating', -1).limit(10))
        
        return jsonify({
            'users_count': users_count,
            'movies_count': movies_count,
            'ratings_count': ratings_count,
            'watchlist_count': watchlist_count,
            'top_movies': top_movies
        }), 200
    
    except Exception as e:
        print(f"Erreur: {e}")
        return jsonify({'message': str(e)}), 500

@app.route('/admin/reset-watchlist', methods=['POST'])
def reset_watchlist():
    """Réinitialiser la watchlist (admin)"""
    try:
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return jsonify({'message': 'Token manquant'}), 401
        
        token = auth_header.split(' ')[1]
        
        # Vérifier le token admin
        if token != os.getenv('ADMIN_TOKEN', 'admin-secret-token'):
            return jsonify({'message': 'Accès non autorisé'}), 403
        
        # Réinitialiser la watchlist
        result = db.watchlist.delete_many({})
        
        return jsonify({
            'message': 'Watchlist réinitialisée',
            'deleted_count': result.deleted_count
        }), 200
    
    except Exception as e:
        print(f"Erreur: {e}")
        return jsonify({'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
