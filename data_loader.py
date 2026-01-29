  # data_loader.py
import pandas as pd
import numpy as np
from pymongo import MongoClient
from datetime import datetime
import os

class MovieDataLoader:
    def __init__(self, mongo_uri, db_name):
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]
        
    def load_users(self, user_file):
        """Charger les données utilisateurs"""
        print(f"📥 Chargement des utilisateurs depuis {user_file}...")
        
        try:
            columns = ['user_id', 'age', 'gender', 'occupation', 'zip_code']
            users = pd.read_csv(user_file, sep='|', names=columns, encoding='latin-1')
            
            # Transformer pour MongoDB
            users_records = []
            for _, row in users.iterrows():
                try:
                    user_record = {
                        'user_id': int(row['user_id']),
                        'age': int(row['age']),
                        'gender': str(row['gender']),
                        'occupation': str(row['occupation']),
                        'zip_code': str(row['zip_code']),
                        'created_at': datetime.now(),
                        'preferences': {
                            'genre_weights': {},
                            'average_rating': 0.0,
                            'rated_movies': []
                        },
                        'cluster_id': None
                    }
                    users_records.append(user_record)
                except Exception as e:
                    print(f"⚠️ Erreur lors du traitement de l'utilisateur {row['user_id']}: {e}")
                    continue
            
            # Insérer dans MongoDB
            if users_records:
                self.db.users.delete_many({})
                result = self.db.users.insert_many(users_records)
                print(f"✅ {len(result.inserted_ids)} utilisateurs chargés")
            else:
                print("❌ Aucun utilisateur valide à charger")
                
        except Exception as e:
            print(f"❌ Erreur lors du chargement des utilisateurs: {e}")
            import traceback
            traceback.print_exc()
    
    def load_movies(self, item_file):
        """Charger les données films"""
        print(f"📥 Chargement des films depuis {item_file}...")
        
        try:
            columns = [
                'movie_id', 'title', 'release_date', 'video_release_date',
                'imdb_url', 'unknown', 'action', 'adventure', 'animation',
                'children', 'comedy', 'crime', 'documentary', 'drama', 'fantasy',
                'film_noir', 'horror', 'musical', 'mystery', 'romance', 'sci_fi',
                'thriller', 'war', 'western'
            ]
            
            movies = pd.read_csv(item_file, sep='|', names=columns, encoding='latin-1')
            
            # Extraire l'année du titre
            movies['year'] = movies['title'].str.extract(r'\((\d{4})\)')
            movies['title_clean'] = movies['title'].str.replace(r'\s*\(\d{4}\)', '', regex=True)
            
            # Génres
            genre_columns = columns[5:]  # Toutes les colonnes de genre
            
            movies_records = []
            for _, row in movies.iterrows():
                try:
                    # Calculer la popularité bayésienne initiale
                    genres = {col: int(row[col]) for col in genre_columns if col != 'unknown'}
                    
                    # Liste des genres actifs
                    active_genres = []
                    for genre, value in genres.items():
                        if value == 1:
                            active_genres.append(genre)
                    
                    movie_record = {
                        'movie_id': int(row['movie_id']),
                        'title': str(row['title_clean']),
                        'year': int(row['year']) if pd.notna(row['year']) else None,
                        'release_date': str(row['release_date']) if pd.notna(row['release_date']) else None,
                        'imdb_url': str(row['imdb_url']) if pd.notna(row['imdb_url']) else None,
                        'genres': active_genres,
                        'genre_vector': genres,
                        'ratings_count': 0,
                        'average_rating': 0.0,
                        'bayesian_rating': 3.0,
                        'cluster_popularity': {},
                        'created_at': datetime.now(),
                        'item_similarities': {},
                        'content_similarities': {}
                    }
                    movies_records.append(movie_record)
                except Exception as e:
                    print(f"⚠️ Erreur lors du traitement du film {row['movie_id']}: {e}")
                    continue
            
            # Insérer dans MongoDB
            if movies_records:
                self.db.movies.delete_many({})
                result = self.db.movies.insert_many(movies_records)
                print(f"✅ {len(result.inserted_ids)} films chargés")
            else:
                print("❌ Aucun film valide à charger")
                
        except Exception as e:
            print(f"❌ Erreur lors du chargement des films: {e}")
            import traceback
            traceback.print_exc()
    
    def load_ratings(self, data_file):
        """Charger les évaluations"""
        print(f"📥 Chargement des évaluations depuis {data_file}...")
        
        try:
            columns = ['user_id', 'movie_id', 'rating', 'timestamp']
            ratings = pd.read_csv(data_file, sep='\t', names=columns)
            
            # Convertir timestamp
            ratings['timestamp'] = pd.to_datetime(ratings['timestamp'], unit='s')
            
            # Insérer les évaluations
            ratings_records = []
            for _, row in ratings.iterrows():
                try:
                    rating_record = {
                        'user_id': int(row['user_id']),
                        'movie_id': int(row['movie_id']),
                        'rating': float(row['rating']),
                        'timestamp': row['timestamp']
                    }
                    ratings_records.append(rating_record)
                except Exception as e:
                    print(f"⚠️ Erreur lors du traitement de l'évaluation: {e}")
                    continue
            
            if ratings_records:
                self.db.ratings.delete_many({})
                result = self.db.ratings.insert_many(ratings_records)
                print(f"✅ {len(result.inserted_ids)} évaluations chargées")
            else:
                print("❌ Aucune évaluation valide à charger")
            
            # Mettre à jour les statistiques
            print("📊 Mise à jour des statistiques...")
            self._update_movie_stats()
            self._update_user_preferences()
            
        except Exception as e:
            print(f"❌ Erreur lors du chargement des évaluations: {e}")
            import traceback
            traceback.print_exc()
    
    def _update_movie_stats(self):
        """Mettre à jour les statistiques des films"""
        print("📈 Calcul des statistiques des films...")
        
        try:
            pipeline = [
                {
                    '$group': {
                        '_id': '$movie_id',
                        'avg_rating': {'$avg': '$rating'},
                        'rating_count': {'$sum': 1}
                    }
                }
            ]
            
            movie_stats = list(self.db.ratings.aggregate(pipeline))
            print(f"   {len(movie_stats)} films avec statistiques")
            
            for stat in movie_stats:
                try:
                    movie_id = stat['_id']
                    avg_rating = float(stat['avg_rating'])
                    count = int(stat['rating_count'])
                    
                    # Calcul de la note bayésienne
                    C = 3.0  # Note moyenne attendue
                    m = 10   # Nombre minimum de votes
                    bayesian_rating = (count * avg_rating + m * C) / (count + m)
                    
                    result = self.db.movies.update_one(
                        {'movie_id': movie_id},
                        {
                            '$set': {
                                'average_rating': avg_rating,
                                'ratings_count': count,
                                'bayesian_rating': float(bayesian_rating)
                            }
                        }
                    )
                except Exception as e:
                    print(f"⚠️ Erreur lors de la mise à jour du film {stat.get('_id')}: {e}")
                    continue
            
            print("✅ Statistiques des films mises à jour")
            
        except Exception as e:
            print(f"❌ Erreur lors de la mise à jour des statistiques des films: {e}")
            import traceback
            traceback.print_exc()
    
    def _update_user_preferences(self):
        """Mettre à jour les préférences des utilisateurs"""
        print("👤 Mise à jour des préférences utilisateurs...")
        
        try:
            # Pipeline pour obtenir les préférences par genre
            pipeline = [
                {
                    '$lookup': {
                        'from': 'movies',
                        'localField': 'movie_id',
                        'foreignField': 'movie_id',
                        'as': 'movie_info'
                    }
                },
                {'$unwind': '$movie_info'},
                {'$unwind': '$movie_info.genres'},
                {
                    '$group': {
                        '_id': {
                            'user_id': '$user_id',
                            'genre': '$movie_info.genres'
                        },
                        'avg_rating': {'$avg': '$rating'},
                        'count': {'$sum': 1}
                    }
                }
            ]
            
            genre_prefs = list(self.db.ratings.aggregate(pipeline))
            print(f"   {len(genre_prefs)} préférences de genre à traiter")
            
            # Organiser les préférences par utilisateur
            user_genre_prefs = {}
            for pref in genre_prefs:
                try:
                    user_id = pref['_id']['user_id']
                    genre = str(pref['_id']['genre'])
                    avg_rating = float(pref['avg_rating'])
                    
                    if user_id not in user_genre_prefs:
                        user_genre_prefs[user_id] = {}
                    
                    user_genre_prefs[user_id][genre] = avg_rating
                except Exception as e:
                    continue
            
            # Mettre à jour les utilisateurs
            updated_count = 0
            for user_id, genre_weights in user_genre_prefs.items():
                try:
                    result = self.db.users.update_one(
                        {'user_id': user_id},
                        {
                            '$set': {
                                f'preferences.genre_weights': genre_weights
                            }
                        }
                    )
                    if result.modified_count > 0:
                        updated_count += 1
                except Exception as e:
                    print(f"⚠️ Erreur lors de la mise à jour de l'utilisateur {user_id}: {e}")
                    continue
            
            print(f"✅ Préférences mises à jour pour {updated_count} utilisateurs")
            
        except Exception as e:
            print(f"❌ Erreur lors de la mise à jour des préférences utilisateurs: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    # Configuration
    MONGO_URI = "mongodb+srv://aichasaaydi_db_user:W4hass6DEv1AfHe9@cluster0.vifo278.mongodb.net/?appName=Cluster0"
    DB_NAME = "movie_recommender"
    
    try:
        print("🚀 Démarrage du chargement des données MovieLens...")
        
        loader = MovieDataLoader(MONGO_URI, DB_NAME)
        
        # Charger les données (remplacez par vos chemins de fichiers)
        # Assurez-vous que les fichiers sont dans le même répertoire
        data_files = {
            'users': 'u.user',
            'movies': 'u.item',
            'ratings': 'u.data'
        }
        
        # Vérifier que les fichiers existent
        for file_type, file_path in data_files.items():
            if not os.path.exists(file_path):
                print(f"⚠️ Fichier {file_path} non trouvé. Veuillez le placer dans le répertoire courant.")
                # Créer un fichier exemple si besoin (pour les tests)
                if file_type == 'users':
                    with open(file_path, 'w') as f:
                        f.write("1|24|M|technician|85711\n2|53|F|other|94043\n")
                elif file_type == 'movies':
                    with open(file_path, 'w') as f:
                        f.write("1|Toy Story (1995)|01-Jan-1995||http://us.imdb.com/M/title-exact?Toy%20Story%20(1995)|0|0|0|1|1|1|0|0|0|0|0|0|0|0|0|0|0|0|0\n")
                elif file_type == 'ratings':
                    with open(file_path, 'w') as f:
                        f.write("1\t1\t5\t874965758\n1\t2\t3\t876893171\n")
        
        # Charger les données
        loader.load_users(data_files['users'])
        loader.load_movies(data_files['movies'])
        loader.load_ratings(data_files['ratings'])
        
        print("🎉 Chargement des données terminé avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur fatale lors du chargement des données: {e}")
        import traceback
        traceback.print_exc()

    