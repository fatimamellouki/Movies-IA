# backend/healthcheck.py
"""
Script de vérification de santé du système
Vérifie la connectivité à MongoDB et la disponibilité de l'API
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pymongo import MongoClient
from dotenv import load_dotenv
import json

load_dotenv()

def check_mongodb():
    """Vérifier la connexion à MongoDB"""
    print("🔍 Vérification de MongoDB...")
    
    try:
        mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/movie_recommender')
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        
        # Tester la connexion
        client.admin.command('ping')
        
        db = client.get_database()
        
        # Vérifier les collections
        collections = db.list_collection_names()
        
        print(f"✅ MongoDB connecté")
        print(f"   Base de données: {db.name}")
        print(f"   Collections: {', '.join(collections) if collections else 'Aucune'}")
        
        # Statistiques
        try:
            users_count = db.users.count_documents({})
            movies_count = db.movies.count_documents({})
            ratings_count = db.ratings.count_documents({})
            
            print(f"   Utilisateurs: {users_count}")
            print(f"   Films: {movies_count}")
            print(f"   Évaluations: {ratings_count}")
        except:
            pass
        
        return True
    
    except Exception as e:
        print(f"❌ Erreur MongoDB: {e}")
        print(f"   URI tentée: {mongo_uri}")
        return False

def check_api():
    """Vérifier l'API"""
    print("\n🔍 Vérification de l'API...")
    
    try:
        import requests
        
        response = requests.get('http://localhost:5000/api/health', timeout=5)
        
        if response.status_code == 200:
            print(f"✅ API disponible")
            print(f"   Réponse: {response.json()}")
            return True
        else:
            print(f"⚠️  API répond avec le code {response.status_code}")
            return False
    
    except requests.ConnectionError:
        print(f"⚠️  API non disponible (serveur non démarré)")
        return False
    except Exception as e:
        print(f"❌ Erreur lors de la vérification de l'API: {e}")
        return False

def check_requirements():
    """Vérifier les imports de base"""
    print("\n🔍 Vérification des dépendances...")
    
    required_modules = [
        'flask',
        'flask_cors',
        'flask_jwt_extended',
        'pymongo',
        'pandas',
        'numpy',
        'sklearn',
        'bcrypt'
    ]
    
    missing = []
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module}")
            missing.append(module)
    
    if missing:
        print(f"\n⚠️  Modules manquants: {', '.join(missing)}")
        return False
    
    return True

def main():
    """Fonction principale"""
    print("=" * 60)
    print("  🏥 Vérification de santé du système")
    print("=" * 60)
    
    checks = [
        ("Dépendances Python", check_requirements),
        ("MongoDB", check_mongodb),
        ("API", check_api),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append(result)
        except Exception as e:
            print(f"❌ Erreur lors de la vérification {name}: {e}")
            results.append(False)
    
    # Rapport final
    print("\n" + "=" * 60)
    print("  📊 Rapport final")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Tests réussis: {passed}/{total}")
    
    if all(results):
        print("\n✅ Tout est en ordre! Le système est prêt.")
        return 0
    else:
        print("\n⚠️  Certains tests ont échoué. Veuillez vérifier la configuration.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
