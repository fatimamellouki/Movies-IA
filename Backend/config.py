# backend/config.py
import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration de base"""
    # Sécurité
    SECRET_KEY = os.getenv('SECRET_KEY', 'votre_cle_secrete_dev')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'votre_jwt_secret_dev')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # MongoDB
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/movie_recommender')
    
    # Configuration de l'application
    DEBUG = os.getenv('FLASK_ENV') == 'development'
    TESTING = False
    
    # CORS
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')
    
    # Configuration du système de recommandation
    RECOMMENDATION_SETTINGS = {
        'n_clusters': 5,
        'similarity_threshold': 0.1,
        'min_ratings_for_recommendation': 5,
        'hybrid_weights': {
            'item_based': 0.35,
            'user_based': 0.25,
            'content_based': 0.25,
            'cluster': 0.15
        },
        'new_user_weights': {
            'cluster': 0.7,
            'content_based': 0.3
        }
    }
    
    # Chemins de sauvegarde
    MODEL_SAVE_PATH = os.getenv('MODEL_SAVE_PATH', './models')
    DATA_SAVE_PATH = os.getenv('DATA_SAVE_PATH', './data')

class DevelopmentConfig(Config):
    """Configuration de développement"""
    DEBUG = True
    MONGO_URI = os.getenv('MONGO_URI_DEV', 'mongodb://localhost:27017/movie_recommender_dev')

class TestingConfig(Config):
    """Configuration de test"""
    TESTING = True
    MONGO_URI = os.getenv('MONGO_URI_TEST', 'mongodb://localhost:27017/movie_recommender_test')

class ProductionConfig(Config):
    """Configuration de production"""
    DEBUG = False
    MONGO_URI = os.getenv('MONGO_URI_PROD')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    
    # Désactiver les informations détaillées d'erreur
    PROPAGATE_EXCEPTIONS = False

# Mapping des configurations
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

def get_config(config_name=None):
    """Obtenir la configuration par nom"""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'default')
    return config.get(config_name, config['default'])