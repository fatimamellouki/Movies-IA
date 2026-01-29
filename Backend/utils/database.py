# backend/utils/database.py
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import ConnectionFailure, OperationFailure
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.init_connection()
        return cls._instance
    
    def init_connection(self):
        """Initialiser la connexion MongoDB"""
        try:
            mongo_uri = os.getenv('MONGO_URI')
            if not mongo_uri:
                raise ValueError("MONGO_URI n'est pas défini dans les variables d'environnement")
            
            self.client = MongoClient(mongo_uri)
            self.db = self.client.get_database()
            
            # Tester la connexion
            self.client.admin.command('ping')
            print("✅ Connecté à MongoDB avec succès")
            
            # Créer les index
            self.create_indexes()
            
        except ConnectionFailure as e:
            print(f"❌ Échec de connexion à MongoDB: {e}")
            raise
        except Exception as e:
            print(f"❌ Erreur lors de l'initialisation de la base de données: {e}")
            raise
    
    def create_indexes(self):
        """Créer les index pour optimiser les performances"""
        try:
            # Index pour les utilisateurs
            self.db.users.create_index([('email', ASCENDING)], unique=True)
            self.db.users.create_index([('user_id', ASCENDING)], unique=True)
            self.db.users.create_index([('cluster_id', ASCENDING)])
            
            # Index pour les films
            self.db.movies.create_index([('movie_id', ASCENDING)], unique=True)
            self.db.movies.create_index([('title', 'text')])
            self.db.movies.create_index([('genres', ASCENDING)])
            self.db.movies.create_index([('bayesian_rating', DESCENDING)])
            
            # Index pour les évaluations
            self.db.ratings.create_index([('user_id', ASCENDING), ('movie_id', ASCENDING)], unique=True)
            self.db.ratings.create_index([('user_id', ASCENDING)])
            self.db.ratings.create_index([('movie_id', ASCENDING)])
            self.db.ratings.create_index([('timestamp', DESCENDING)])
            
            print("✅ Index MongoDB créés avec succès")
            
        except OperationFailure as e:
            print(f"⚠️ Erreur lors de la création des index: {e}")
    
    def get_collection(self, collection_name):
        """Obtenir une collection par son nom"""
        return getattr(self.db, collection_name, None)
    
    def close_connection(self):
        """Fermer la connexion MongoDB"""
        if hasattr(self, 'client'):
            self.client.close()
            print("✅ Connexion MongoDB fermée")

# Fonctions d'accès globales
db_instance = None

def get_db():
    """Obtenir l'instance de base de données"""
    global db_instance
    if db_instance is None:
        db_instance = Database()
    return db_instance.db

def init_db():
    """Initialiser la base de données"""
    return get_db()

def close_db():
    """Fermer la connexion à la base de données"""
    global db_instance
    if db_instance:
        db_instance.close_connection()
        db_instance = None