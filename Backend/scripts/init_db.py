# backend/scripts/init_db.py
"""
Script d'initialisation de la base de données
Charge les films et configure les index
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pymongo import MongoClient
from dotenv import load_dotenv
import csv
from datetime import datetime

load_dotenv()

def init_database():
    """Initialiser la base de données avec les données de films"""
    
    mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/movie_recommender')
    
    print("🚀 Initialisation de la base de données...")
    print(f"   URI: {mongo_uri[:30]}...")
    
    try:
        client = MongoClient(mongo_uri)
        db = client.get_database()
        
        # Tester la connexion
        client.admin.command('ping')
        print("✅ Connexion à MongoDB réussie")
        
        # Créer les index
        print("\n📊 Création des index...")
        
        # Index pour les utilisateurs
        db.users.create_index([('email', 1)], unique=True)
        db.users.create_index([('user_id', 1)], unique=True)
        db.users.create_index([('cluster_id', 1)])
        print("   ✓ Index utilisateurs créés")
        
        # Index pour les films
        db.movies.create_index([('movie_id', 1)], unique=True)
        db.movies.create_index([('title', 'text')])
        db.movies.create_index([('genres', 1)])
        db.movies.create_index([('bayesian_rating', -1)])
        print("   ✓ Index films créés")
        
        # Index pour les évaluations
        db.ratings.create_index([('user_id', 1), ('movie_id', 1)], unique=True)
        db.ratings.create_index([('user_id', 1)])
        db.ratings.create_index([('movie_id', 1)])
        db.ratings.create_index([('timestamp', -1)])
        print("   ✓ Index évaluations créés")
        
        # Index pour la watchlist
        db.watchlist.create_index([('user_id', 1), ('movie_id', 1)], unique=True)
        db.watchlist.create_index([('user_id', 1)])
        print("   ✓ Index watchlist créés")
        
        # Vérifier si des films existent
        movies_count = db.movies.count_documents({})
        
        if movies_count == 0:
            print("\n🎬 Chargement des films depuis u.item...")
            
            # Déterminer le chemin des fichiers
            script_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(os.path.dirname(script_dir))
            item_file = os.path.join(project_root, 'u.item')
            
            if os.path.exists(item_file):
                movies = []
                try:
                    with open(item_file, 'r', encoding='latin-1') as f:
                        for line in f:
                            parts = line.strip().split('|')
                            if len(parts) >= 24:
                                movie_id = int(parts[0])
                                title = parts[1]
                                # Genres: colonnes 5-23 (19 genres possibles)
                                genres = [
                                    'Unknown', 'Action', 'Adventure', 'Animation', 'Children', 
                                    'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 
                                    'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 
                                    'Sci-Fi', 'Thriller', 'War', 'Western'
                                ]
                                movie_genres = [genres[i] for i in range(5, 24) if i < len(parts) and parts[i] == '1']
                                
                                movies.append({
                                    'movie_id': movie_id,
                                    'title': title,
                                    'genres': movie_genres if movie_genres else ['Unknown'],
                                    'bayesian_rating': 3.0,  # Sera calculé après chargement des évaluations
                                    'average_rating': 3.0,
                                    'ratings_count': 0
                                })
                    
                    db.movies.insert_many(movies)
                    print(f"   ✓ {len(movies)} films chargés depuis u.item")
                except Exception as e:
                    print(f"   ⚠️  Erreur lecture u.item: {e}")
            else:
                print(f"   ⚠️  Fichier u.item non trouvé à {item_file}")
                print("   Création de films de test...")
                test_movies = [
                    {'movie_id': 1, 'title': 'The Shawshank Redemption', 'genres': ['Drama'], 'bayesian_rating': 4.8, 'average_rating': 4.8, 'ratings_count': 100},
                    {'movie_id': 2, 'title': 'The Godfather', 'genres': ['Crime', 'Drama'], 'bayesian_rating': 4.7, 'average_rating': 4.7, 'ratings_count': 90},
                    {'movie_id': 3, 'title': 'The Dark Knight', 'genres': ['Action', 'Crime', 'Drama'], 'bayesian_rating': 4.6, 'average_rating': 4.6, 'ratings_count': 95}
                ]
                db.movies.insert_many(test_movies)
                print(f"   ✓ {len(test_movies)} films de test créés")
        else:
            print(f"\n✅ {movies_count} films trouvés dans la base de données")
        
        # Charger les utilisateurs si nécessaire
        users_count = db.users.count_documents({})
        if users_count == 0:
            print("\n👥 Chargement des utilisateurs depuis u.user...")
            user_file = os.path.join(project_root, 'u.user')
            
            if os.path.exists(user_file):
                users = []
                try:
                    with open(user_file, 'r', encoding='latin-1') as f:
                        for line in f:
                            parts = line.strip().split('|')
                            if len(parts) >= 5:
                                user_id = int(parts[0])
                                age = int(parts[1])
                                gender = parts[2]
                                occupation = parts[3]
                                
                                users.append({
                                    'user_id': user_id,
                                    'age': age,
                                    'gender': gender,
                                    'occupation': occupation,
                                    'cluster_id': None,
                                    'preferences': {}
                                })
                    
                    if users:
                        db.users.insert_many(users)
                        print(f"   ✓ {len(users)} utilisateurs chargés depuis u.user")
                except Exception as e:
                    print(f"   ⚠️  Erreur lecture u.user: {e}")
        
        # Charger les évaluations si nécessaire
        ratings_count = db.ratings.count_documents({})
        if ratings_count == 0:
            print("\n⭐ Chargement des évaluations depuis u.data...")
            data_file = os.path.join(project_root, 'u.data')
            
            if os.path.exists(data_file):
                ratings = []
                try:
                    with open(data_file, 'r', encoding='latin-1') as f:
                        for line in f:
                            parts = line.strip().split('\t')
                            if len(parts) >= 3:
                                user_id = int(parts[0])
                                movie_id = int(parts[1])
                                rating = int(parts[2])
                                timestamp = int(parts[3]) if len(parts) > 3 else int(datetime.now().timestamp())
                                
                                ratings.append({
                                    'user_id': user_id,
                                    'movie_id': movie_id,
                                    'rating': rating,
                                    'timestamp': timestamp,
                                    'date': datetime.fromtimestamp(timestamp)
                                })
                    
                    if ratings:
                        db.ratings.insert_many(ratings)
                        print(f"   ✓ {len(ratings)} évaluations chargées depuis u.data")
                except Exception as e:
                    print(f"   ⚠️  Erreur lecture u.data: {e}")
        
        # Afficher les statistiques
        print("\n📊 Statistiques de la base de données:")
        print(f"   • Utilisateurs: {db.users.count_documents({})}")
        print(f"   • Films: {db.movies.count_documents({})}")
        print(f"   • Évaluations: {db.ratings.count_documents({})}")
        print(f"   • Watchlist: {db.watchlist.count_documents({})}")
        
        print("\n✅ Initialisation réussie!")
        
        client.close()
        return True
    
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = init_database()
    sys.exit(0 if success else 1)
