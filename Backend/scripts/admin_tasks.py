#!/usr/bin/env python3
"""
Scripts d'administration pour le système de recommandation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pymongo import MongoClient
from offline.recommender import HybridRecommender
import argparse
from datetime import datetime
import time

def run_offline_computations(db):
    """Exécuter tous les calculs offline"""
    print("🔧 Début des calculs offline...")
    
    recommender = HybridRecommender(db)
    
    start_time = time.time()
    
    try:
        # 1. Clustering
        print("📊 Clustering des utilisateurs...")
        recommender.cluster_users()
        
        # 2. Popularité par cluster
        print("🏆 Calcul de la popularité bayésienne par cluster...")
        recommender.calculate_cluster_popularity()
        
        # 3. Similarités item-item
        print("🔗 Calcul des similarités item-item...")
        recommender.calculate_item_similarities()
        
        # 4. Similarités user-user
        print("👥 Calcul des similarités user-user...")
        recommender.calculate_user_similarities()
        
        # # 5. Similarités content-based
        # print("🎭 Calcul des similarités content-based...")
        # recommender.calculate_content_based_similarity()
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"✅ Calculs offline terminés en {duration:.2f} secondes")
        print(f"🕐 Terminé à: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except Exception as e:
        print(f"❌ Erreur lors des calculs offline: {e}")
        import traceback
        traceback.print_exc()
        raise

def update_single_user(user_id, db):
    """Mettre à jour les recommandations pour un seul utilisateur"""
    print(f"👤 Mise à jour des recommandations pour l'utilisateur {user_id}...")
    
    recommender = HybridRecommender(db)
    
    try:
        # Assigner/mettre à jour le cluster
        recommender.assign_user_cluster(user_id)
        user = db.users.find_one({'_id': user_id})
        if user:
            print(f"   Cluster assigné: {user.get('cluster_id')}")
        else:
            print("   Utilisateur non trouvé")
        
        # Mettre à jour les préférences
        recommender.update_user_preferences(user_id)
        print(f"   Préférences mises à jour")
        
        print(f"✅ Mise à jour terminée pour l'utilisateur {user_id}")
        
    except Exception as e:
        print(f"❌ Erreur lors de la mise à jour: {e}")
        import traceback
        traceback.print_exc()

def cleanup_database(db):
    """Nettoyer la base de données"""
    print("🧹 Nettoyage de la base de données...")
    
    try:
        # Supprimer les données temporaires (si la collection existe)
        if 'temp_data' in db.list_collection_names():
            result = db.temp_data.delete_many({})
            print(f"   Données temporaires supprimées: {result.deleted_count}")
        
        # Supprimer les anciennes sessions (si la collection existe)
        if 'sessions' in db.list_collection_names():
            cutoff_date = datetime.now().timestamp() - (30 * 24 * 60 * 60)  # 30 jours
            result = db.sessions.delete_many({'last_activity': {'$lt': cutoff_date}})
            print(f"   Sessions expirées supprimées: {result.deleted_count}")
        
        print("✅ Nettoyage terminé")
        
    except Exception as e:
        print(f"❌ Erreur lors du nettoyage: {e}")
        import traceback
        traceback.print_exc()

def show_stats(db):
    """Afficher les statistiques de la base de données"""
    print("📈 Statistiques de la base de données:")
    
    try:
        # Comptes des collections principales
        collections_to_check = ['users', 'movies', 'ratings']
        
        for collection_name in collections_to_check:
            if collection_name in db.list_collection_names():
                count = db[collection_name].count_documents({})
                icon = {
                    'users': '👥',
                    'movies': '🎬',
                    'ratings': '⭐'
                }.get(collection_name, '📊')
                
                label = {
                    'users': 'Utilisateurs',
                    'movies': 'Films',
                    'ratings': 'Évaluations'
                }.get(collection_name, collection_name)
                
                print(f"   {icon} {label}: {count}")
            else:
                print(f"   ⚠️ Collection '{collection_name}' non trouvée")
        
        # Statistiques des clusters
        if 'users' in db.list_collection_names():
            try:
                clusters = [c for c in db.users.distinct('cluster_id') if c is not None]
                print(f"   📊 Clusters actifs: {len(clusters)}")
                
                for cluster_id in sorted(clusters):
                    count = db.users.count_documents({'cluster_id': cluster_id})
                    print(f"      Cluster {cluster_id}: {count} utilisateurs")
            except Exception as e:
                print(f"   ⚠️ Erreur lors de la récupération des clusters: {e}")
        
        # Moyenne des notes
        if 'ratings' in db.list_collection_names():
            try:
                pipeline = [
                    {'$group': {'_id': None, 'avg_rating': {'$avg': '$rating'}}}
                ]
                avg_rating = list(db.ratings.aggregate(pipeline))
                if avg_rating and avg_rating[0].get('avg_rating') is not None:
                    print(f"   📊 Note moyenne: {avg_rating[0]['avg_rating']:.2f}")
            except Exception as e:
                print(f"   ⚠️ Erreur lors du calcul de la moyenne: {e}")
        
        # Films les mieux notés
        if 'movies' in db.list_collection_names():
            try:
                print(f"\n   🏆 Top 5 des films:")
                top_movies = db.movies.find().sort('bayesian_rating', -1).limit(5)
                for i, movie in enumerate(top_movies, 1):
                    title = movie.get('title', 'Inconnu')
                    rating = movie.get('bayesian_rating', 0)
                    print(f"      {i}. {title[:40]}... - {rating:.2f}")
            except Exception as e:
                print(f"   ⚠️ Erreur lors de la récupération des top films: {e}")
        
        # Statistiques des similarités
        if 'movies' in db.list_collection_names():
            try:
                movies_with_similarities = db.movies.count_documents({'item_similarities': {'$exists': True, '$ne': {}}})
                total_movies = db.movies.count_documents({})
                if total_movies > 0:
                    percentage = (movies_with_similarities / total_movies) * 100
                    print(f"   🔗 Films avec similarités: {movies_with_similarities}/{total_movies} ({percentage:.1f}%)")
            except Exception as e:
                print(f"   ⚠️ Erreur lors des statistiques de similarité: {e}")
        
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des statistiques: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(description='Scripts d\'administration du système de recommandation')
    parser.add_argument('--task', choices=['offline', 'cleanup', 'stats', 'update-user'], 
                       required=True, help='Tâche à exécuter')
    parser.add_argument('--user-id', help='ID utilisateur pour la tâche update-user')
    parser.add_argument('--mongo-uri', default='mongodb://localhost:27017/movie_recommender',
                       help='URI MongoDB (défaut: mongodb://localhost:27017/movie_recommender)')
    
    args = parser.parse_args()
    
    # Connexion à MongoDB
    try:
        client = MongoClient(args.mongo_uri)
        db = client.get_database()
        print(f"✅ Connecté à MongoDB")
        print(f"   Base de données: {db.name}")
        
        # Lister les collections disponibles
        collections = db.list_collection_names()
        print(f"   Collections disponibles: {', '.join(collections)}")
        
    except Exception as e:
        print(f"❌ Erreur de connexion à MongoDB: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Exécuter la tâche demandée
    try:
        if args.task == 'offline':
            run_offline_computations(db)
        elif args.task == 'cleanup':
            cleanup_database(db)
        elif args.task == 'stats':
            show_stats(db)
        elif args.task == 'update-user':
            if not args.user_id:
                print("❌ L'argument --user-id est requis pour la tâche update-user")
                return
            
            # Convertir user_id en ObjectId si nécessaire
            try:
                from bson import ObjectId
                user_id_obj = ObjectId(args.user_id)
                update_single_user(user_id_obj, db)
            except:
                print(f"⚠️ User ID '{args.user_id}' n'est pas un ObjectId valide, tentative avec string...")
                update_single_user(args.user_id, db)
    except KeyboardInterrupt:
        print("\n⏹️ Opération interrompue par l'utilisateur")
    except Exception as e:
        print(f"❌ Erreur lors de l'exécution de la tâche: {e}")
        import traceback
        traceback.print_exc()
    finally:
        try:
            client.close()
            print("🔌 Connexion MongoDB fermée")
        except:
            pass

if __name__ == '__main__':
    main()