# backend/tests/test_recommender.py
import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pymongo import MongoClient
from offline.recommender import HybridRecommender
from config import get_config

class TestRecommender(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Configuration initiale pour les tests"""
        config = get_config('testing')
        cls.client = MongoClient(config.MONGO_URI)
        cls.db = cls.client.get_database()
        cls.recommender = HybridRecommender(cls.db)
        
        # Créer des données de test
        cls.setup_test_data()
    
    @classmethod
    def setup_test_data(cls):
        """Créer des données de test"""
        # Nettoyer les collections de test
        cls.db.users.delete_many({})
        cls.db.movies.delete_many({})
        cls.db.ratings.delete_many({})
        
        # Créer des utilisateurs de test
        test_users = [
            {
                'user_id': 99991,
                'age': 25,
                'gender': 'M',
                'occupation': 'student',
                'email': 'test1@example.com',
                'preferences': {'genre_weights': {}}
            },
            {
                'user_id': 99992,
                'age': 30,
                'gender': 'F',
                'occupation': 'engineer',
                'email': 'test2@example.com',
                'preferences': {'genre_weights': {}}
            }
        ]
        cls.db.users.insert_many(test_users)
        
        # Créer des films de test
        test_movies = [
            {
                'movie_id': 99991,
                'title': 'Test Movie 1',
                'genres': ['Action', 'Adventure'],
                'genre_vector': {'action': 1, 'adventure': 1},
                'bayesian_rating': 4.5
            },
            {
                'movie_id': 99992,
                'title': 'Test Movie 2',
                'genres': ['Drama', 'Romance'],
                'genre_vector': {'drama': 1, 'romance': 1},
                'bayesian_rating': 3.8
            }
        ]
        cls.db.movies.insert_many(test_movies)
        
        # Créer des évaluations de test
        test_ratings = [
            {'user_id': 99991, 'movie_id': 99991, 'rating': 5.0},
            {'user_id': 99992, 'movie_id': 99992, 'rating': 4.0}
        ]
        cls.db.ratings.insert_many(test_ratings)
    
    def test_cluster_users(self):
        """Tester le clustering des utilisateurs"""
        self.recommender.cluster_users()
        
        # Vérifier que les utilisateurs ont un cluster
        users = list(self.db.users.find({'user_id': {'$in': [99991, 99992]}}))
        for user in users:
            self.assertIsNotNone(user.get('cluster_id'))
    
    def test_calculate_cluster_popularity(self):
        """Tester le calcul de la popularité par cluster"""
        self.recommender.calculate_cluster_popularity()
        
        # Vérifier que les films ont des données de popularité
        movies = list(self.db.movies.find({'movie_id': {'$in': [99991, 99992]}}))
        for movie in movies:
            self.assertIsNotNone(movie.get('cluster_popularity'))
    
    def test_recommend_for_new_user(self):
        """Tester les recommandations pour un nouvel utilisateur"""
        # Créer un nouvel utilisateur
        new_user = {
            'user_id': 99993,
            'age': 28,
            'gender': 'M',
            'occupation': 'programmer',
            'email': 'newuser@example.com',
            'preferences': {'genre_weights': {}}
        }
        self.db.users.insert_one(new_user)
        
        # Obtenir des recommandations
        recommendations = self.recommender.recommend_for_new_user(new_user['user_id'], top_n=5)
        
        # Vérifier que des recommandations sont retournées
        self.assertIsInstance(recommendations, list)
        if recommendations:
            self.assertIn('movie_id', recommendations[0])
            self.assertIn('score', recommendations[0])
    
    def test_update_user_preferences(self):
        """Tester la mise à jour des préférences utilisateur"""
        self.recommender.update_user_preferences(99991)
        
        # Vérifier que les préférences ont été mises à jour
        user = self.db.users.find_one({'user_id': 99991})
        self.assertIsNotNone(user.get('preferences', {}).get('genre_weights'))
    
    @classmethod
    def tearDownClass(cls):
        """Nettoyage après les tests"""
        # Supprimer les données de test
        cls.db.users.delete_many({'user_id': {'$gte': 99990}})
        cls.db.movies.delete_many({'movie_id': {'$gte': 99990}})
        cls.db.ratings.delete_many({'user_id': {'$gte': 99990}})
        
        # Fermer la connexion
        cls.client.close()

if __name__ == '__main__':
    unittest.main()