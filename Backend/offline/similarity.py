# backend/offline/similarity.py
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix, save_npz, load_npz
import os
from datetime import datetime

# csr_matrix : pour représenter les matrices creuses (sparse), utile pour économiser de la mémoire.
# save_npz/load_npz : pour sauvegarder/recharger les matrices déjà calculées.

class SimilarityCalculator:
    def __init__(self, db):
        self.db = db
        self.item_similarity = None
        self.user_similarity = None
        
    def calculate_item_similarity(self, min_common_users=5, save_path=None):
        """Calculer la similarité item-item basée sur les évaluations"""
        # Récupérer toutes les évaluations
        ratings = list(self.db.ratings.find(
            {},
            {'user_id': 1, 'movie_id': 1, 'rating': 1}
        ))
        
        if not ratings:
            return None
        
        # Créer un DataFrame
        df = pd.DataFrame(ratings)
        
        # Créer une matrice utilisateur-film
        user_movie_matrix = df.pivot_table(
            index='user_id',
            columns='movie_id',
            values='rating',
            fill_value=0
        )
        
        # Convertir en matrice creuse
        sparse_matrix = csr_matrix(user_movie_matrix.values)
        
        # Calculer la similarité cosinus
        print("Calcul de la similarité item-item...")
        movie_similarity = cosine_similarity(sparse_matrix.T)
        
        # Convertir en DataFrame pour un accès facile
        movie_ids = user_movie_matrix.columns.tolist()
        similarity_df = pd.DataFrame(
            movie_similarity,
            index=movie_ids,
            columns=movie_ids
        )
        
        self.item_similarity = similarity_df
        
        # Sauvegarder si un chemin est fourni
        if save_path:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            similarity_df.to_pickle(save_path)
            print(f"Similarité item-item sauvegardée à {save_path}")
        
        # Mettre à jour dans MongoDB (top 20 similarités par film)
        self._update_item_similarities_in_db(movie_ids, similarity_df)
        
        return similarity_df
    
    def calculate_user_similarity(self, min_common_movies=5, save_path=None):
        """Calculer la similarité user-user basée sur les évaluations"""
        # Récupérer toutes les évaluations
        ratings = list(self.db.ratings.find(
            {},
            {'user_id': 1, 'movie_id': 1, 'rating': 1}
        ))
        
        if not ratings:
            return None
        
        # Créer un DataFrame
        df = pd.DataFrame(ratings)
        
        # Créer une matrice utilisateur-film
        user_movie_matrix = df.pivot_table(
            index='user_id',
            columns='movie_id',
            values='rating',
            fill_value=0
        )
        
        # Convertir en matrice creuse
        sparse_matrix = csr_matrix(user_movie_matrix.values)
        
        # Calculer la similarité cosinus
        print("Calcul de la similarité user-user...")
        user_similarity = cosine_similarity(sparse_matrix)
        
        # Convertir en DataFrame
        user_ids = user_movie_matrix.index.tolist()
        similarity_df = pd.DataFrame(
            user_similarity,
            index=user_ids,
            columns=user_ids
        )
        
        self.user_similarity = similarity_df
        
        # Sauvegarder si un chemin est fourni
        if save_path:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            similarity_df.to_pickle(save_path)
            print(f"Similarité user-user sauvegardée à {save_path}")
        
        # Mettre à jour dans MongoDB (top 30 utilisateurs similaires)
        self._update_user_similarities_in_db(user_ids, similarity_df)
        
        return similarity_df
    
    def _update_item_similarities_in_db(self, movie_ids, similarity_df):
        """Mettre à jour les similarités item-item dans MongoDB"""
        print("Mise à jour des similarités item-item dans MongoDB...")
        
        for movie_id in movie_ids:
            # Obtenir les films les plus similaires
            similar_movies = similarity_df[movie_id].sort_values(ascending=False)
            
            # Exclure le film lui-même et filtrer par seuil
            top_similar = similar_movies[similar_movies.index != movie_id]
            top_similar = top_similar[top_similar > 0.1]  # Seuil de similarité
            
            # Garder les 20 plus similaires
            top_20 = top_similar.head(20)
            
            # Convertir en dictionnaire
            similarities_dict = top_20.to_dict()
            
            # Mettre à jour dans MongoDB
            self.db.movies.update_one(
                {'movie_id': movie_id},
                {
                    '$set': {
                        'item_similarities': similarities_dict,
                        'similarity_updated_at': datetime.now()
                    }
                }
            )
        
        print(f"Similarités item-item mises à jour pour {len(movie_ids)} films")
    
    def _update_user_similarities_in_db(self, user_ids, similarity_df):
        """Mettre à jour les similarités user-user dans MongoDB"""
        print("Mise à jour des similarités user-user dans MongoDB...")
        
        for user_id in user_ids:
            # Obtenir les utilisateurs les plus similaires
            similar_users = similarity_df[user_id].sort_values(ascending=False)
            
            # Exclure l'utilisateur lui-même et filtrer par seuil
            top_similar = similar_users[similar_users.index != user_id]
            top_similar = top_similar[top_similar > 0.1]  # Seuil de similarité
            
            # Garder les 30 plus similaires
            top_30 = top_similar.head(30)
            
            # Convertir en dictionnaire
            similarities_dict = top_30.to_dict()
            
            # Mettre à jour dans MongoDB
            self.db.users.update_one(
                {'user_id': user_id},
                {
                    '$set': {
                        'similar_users': similarities_dict,
                        'similarity_updated_at': datetime.now()
                    }
                }
            )
        
        print(f"Similarités user-user mises à jour pour {len(user_ids)} utilisateurs")
    
    def get_item_similarities(self, movie_id, top_n=10):
        """Obtenir les films similaires à un film donné"""
        if self.item_similarity is None:
            return {}
        
        if movie_id not in self.item_similarity.index:
            return {}
        
        similar_movies = self.item_similarity[movie_id].sort_values(ascending=False)
        similar_movies = similar_movies[similar_movies.index != movie_id]
        
        return similar_movies.head(top_n).to_dict()
    
    def get_user_similarities(self, user_id, top_n=10):
        """Obtenir les utilisateurs similaires à un utilisateur donné"""
        if self.user_similarity is None:
            return {}
        
        if user_id not in self.user_similarity.index:
            return {}
        
        similar_users = self.user_similarity[user_id].sort_values(ascending=False)
        similar_users = similar_users[similar_users.index != user_id]
        
        return similar_users.head(top_n).to_dict()
    
    def calculate_content_based_similarity(self):
        """Calculer la similarité basée sur le contenu (genres)"""
        movies = list(self.db.movies.find(
            {},
            {'movie_id': 1, 'genres': 1, 'genre_vector': 1}
        ))
        
        if not movies:
            return None
        
        # Créer une matrice films x genres
        movie_data = []
        movie_ids = []
        
        for movie in movies:
            movie_ids.append(movie['movie_id'])
            
            # Utiliser le vecteur de genre s'il existe
            if 'genre_vector' in movie:
                genre_vector = movie['genre_vector']
                # Convertir le dictionnaire en liste ordonnée
                genres_ordered = ['unknown', 'action', 'adventure', 'animation', 
                                 'children', 'comedy', 'crime', 'documentary', 
                                 'drama', 'fantasy', 'film_noir', 'horror', 
                                 'musical', 'mystery', 'romance', 'sci_fi', 
                                 'thriller', 'war', 'western']
                vector = [genre_vector.get(genre, 0) for genre in genres_ordered]
                movie_data.append(vector)
            elif 'genres' in movie:
                # Encodage one-hot basé sur les genres
                all_genres = ['Action', 'Adventure', 'Animation', 'Children', 
                            'Comedy', 'Crime', 'Documentary', 'Drama', 
                            'Fantasy', 'Film-Noir', 'Horror', 'Musical', 
                            'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 
                            'War', 'Western']
                vector = [1 if genre in movie['genres'] else 0 for genre in all_genres]
                movie_data.append(vector)
            else:
                movie_data.append([0] * 18)  # Vecteur nul
        
        # Calculer la similarité cosinus
        movie_array = np.array(movie_data)
        content_similarity = cosine_similarity(movie_array)
        
        # Sauvegarder dans MongoDB
        for i, movie_id in enumerate(movie_ids):
            similarities = {}
            for j, other_id in enumerate(movie_ids):
                if i != j and content_similarity[i, j] > 0.1:
                    similarities[other_id] = float(content_similarity[i, j])
            
            # Garder les 20 plus similaires
            top_similar = dict(sorted(similarities.items(), 
                                     key=lambda x: x[1], 
                                     reverse=True)[:20])
            
            self.db.movies.update_one(
                {'movie_id': movie_id},
                {
                    '$set': {
                        'content_similarities': top_similar,
                        'content_similarity_updated_at': datetime.now()
                    }
                }
            )
        
        print(f"Similarités content-based mises à jour pour {len(movie_ids)} films")
        return content_similarity