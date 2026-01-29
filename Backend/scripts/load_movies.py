#!/usr/bin/env python
# backend/scripts/load_movies.py
"""
Script pour charger les films MovieLens depuis u.item dans MongoDB
Alternative à init_db.py si tu veux charger UNIQUEMENT les films
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()


def load_movies():
    """Charger les films depuis u.item"""
    
    mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/movie_recommender')
    
    print("🎬 Chargement des films MovieLens...")
    
    try:
        client = MongoClient(mongo_uri)
        db = client.get_database()
        
        # Tester la connexion
        client.admin.command('ping')
        print("✅ Connexion à MongoDB réussie")
        
        # Vérifier les films existants
        existing = db.movies.count_documents({})
        if existing > 0:
            print(f"\n⚠️  {existing} films déjà en base. Continuer? (y/n): ", end="")
            if input().lower() != 'y':
                print("Annulé.")
                client.close()
                return True
            print("Suppression des films existants...")
            db.movies.delete_many({})
        
        # Trouver le fichier u.item
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(script_dir))
        item_file = os.path.join(project_root, 'u.item')
        
        if not os.path.exists(item_file):
            print(f"❌ Fichier u.item non trouvé à: {item_file}")
            client.close()
            return False
        
        print(f"\n📂 Fichier: {item_file}")
        print("📝 Format: movie_id|title|date|...|genres")
        
        # Noms des genres (indices 5-23)
        GENRES = [
            'Unknown', 'Action', 'Adventure', 'Animation', 'Children',
            'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy',
            'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance',
            'Sci-Fi', 'Thriller', 'War', 'Western'
        ]
        
        movies = []
        errors = 0
        
        with open(item_file, 'r', encoding='latin-1') as f:
            for line_num, line in enumerate(f, 1):
                try:
                    parts = line.strip().split('|')
                    
                    if len(parts) < 24:
                        errors += 1
                        continue
                    
                    movie_id = int(parts[0])
                    title = parts[1]
                    
                    # Extraire les genres (colonnes 5-23)
                    genres = [GENRES[i] for i in range(5, 24) if i < len(parts) and parts[i] == '1']
                    if not genres:
                        genres = ['Unknown']
                    
                    movies.append({
                        'movie_id': movie_id,
                        'title': title,
                        'genres': genres,
                        'bayesian_rating': 3.0,
                        'average_rating': 3.0,
                        'ratings_count': 0
                    })
                    
                    if len(movies) % 100 == 0:
                        print(f"   Traité {len(movies)} films...", end='\r')
                
                except Exception as e:
                    errors += 1
                    if errors <= 5:  # Afficher les 5 premiers erreurs
                        print(f"   ⚠️  Ligne {line_num}: {e}")
        
        if movies:
            db.movies.insert_many(movies)
            print(f"\n✅ {len(movies)} films chargés avec succès")
            
            # Créer les index
            print("\n📊 Création des index...")
            db.movies.create_index([('movie_id', 1)], unique=True)
            db.movies.create_index([('title', 'text')])
            db.movies.create_index([('genres', 1)])
            db.movies.create_index([('bayesian_rating', -1)])
            print("   ✓ Index créés")
            
            # Statistiques
            print("\n📈 Statistiques:")
            print(f"   • Films chargés: {len(movies)}")
            if errors > 0:
                print(f"   • Lignes ignorées: {errors}")
            
            # Afficher quelques exemples
            sample = db.movies.find_one()
            if sample:
                print(f"\n📌 Exemple de film:")
                print(f"   ID: {sample['movie_id']}")
                print(f"   Titre: {sample['title']}")
                print(f"   Genres: {sample['genres']}")
        else:
            print("❌ Aucun film n'a pu être chargé")
            client.close()
            return False
        
        client.close()
        print("\n✅ Opération terminée!")
        return True
    
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = load_movies()
    sys.exit(0 if success else 1)
