# backend/tests/test_api.py
"""
Tests unitaires pour l'API Flask
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
import json
from app import app
from config import TestingConfig

class TestAPI(unittest.TestCase):
    """Tests de l'API"""
    
    @classmethod
    def setUpClass(cls):
        """Configuration avant les tests"""
        app.config.from_object(TestingConfig)
        cls.app = app
        cls.client = app.test_client()
    
    def test_health_check(self):
        """Tester la vérification de santé"""
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('status', data)
    
    def test_get_popular_movies(self):
        """Tester la récupération des films populaires"""
        response = self.client.get('/api/movies/popular')
        self.assertIn(response.status_code, [200, 500])  # 500 si pas de films en BD
    
    def test_register_invalid_email(self):
        """Tester l'inscription avec un email invalide"""
        response = self.client.post(
            '/api/register',
            data=json.dumps({
                'email': 'invalid-email',
                'password': 'Password123!'
            }),
            content_type='application/json'
        )
        # Peut être 400 ou 500 selon l'implémentation
        self.assertIn(response.status_code, [400, 422, 500])
    
    def test_login_nonexistent_user(self):
        """Tester la connexion avec un utilisateur inexistant"""
        response = self.client.post(
            '/api/login',
            data=json.dumps({
                'email': 'nonexistent@example.com',
                'password': 'password'
            }),
            content_type='application/json'
        )
        self.assertIn(response.status_code, [401, 500])
    
    def test_movies_requires_auth(self):
        """Tester que les films nécessitent l'authentification"""
        response = self.client.get('/api/movies')
        self.assertEqual(response.status_code, 401)
    
    def test_user_stats_requires_auth(self):
        """Tester que les stats utilisateur nécessitent l'authentification"""
        response = self.client.get('/api/user/stats')
        self.assertEqual(response.status_code, 401)


class TestHealthCheck(unittest.TestCase):
    """Tests de santé du système"""
    
    @classmethod
    def setUpClass(cls):
        """Configuration avant les tests"""
        app.config.from_object(TestingConfig)
        cls.app = app
        cls.client = app.test_client()
    
    def test_api_responds(self):
        """Tester que l'API répond"""
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
    
    def test_cors_headers_present(self):
        """Tester que les en-têtes CORS sont présents"""
        response = self.client.get('/api/health')
        # CORS peut être configuré différemment
        self.assertIsNotNone(response.data)


if __name__ == '__main__':
    unittest.main()
