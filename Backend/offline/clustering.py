# backend/offline/clustering.py
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import pandas as pd
from datetime import datetime

class UserClustering:
    def __init__(self, db, n_clusters=5):
        self.db = db
        self.n_clusters = n_clusters
        self.kmeans = None
        self.scaler = StandardScaler()
        
    def prepare_user_features(self):
        """Préparer les caractéristiques des utilisateurs pour le clustering"""
        users = list(self.db.users.find(
            {},
            {'user_id': 1, 'age': 1, 'gender': 1, 'occupation': 1}
        ))
        
        if not users:
            return None, None
        
        # Convertir en DataFrame
        df = pd.DataFrame(users)
        
        # Encoder les caractéristiques catégorielles
        df_encoded = pd.get_dummies(df, columns=['gender', 'occupation'])
        
        # Sélectionner les colonnes numériques
        feature_columns = ['age'] + [col for col in df_encoded.columns 
                                    if col.startswith(('gender_', 'occupation_'))]
        
        features = df_encoded[feature_columns].values
        user_ids = df['user_id'].values
        
        return features, user_ids
    
    def fit(self):
        """Entraîner le modèle de clustering"""
        features, user_ids = self.prepare_user_features()
        
        if features is None:
            return
        
        # Normaliser les caractéristiques
        features_scaled = self.scaler.fit_transform(features)
        
        # Appliquer K-Means
        self.kmeans = KMeans(
            n_clusters=self.n_clusters,
            random_state=42,
            n_init=10,
            max_iter=300
        )
        
        cluster_labels = self.kmeans.fit_predict(features_scaled)
        
        # Mettre à jour les clusters dans la base de données
        for user_id, cluster_id in zip(user_ids, cluster_labels):
            self.db.users.update_one(
                {'user_id': user_id},
                {
                    '$set': {
                        'cluster_id': int(cluster_id),
                        'cluster_updated_at': datetime.now()
                    }
                }
            )
        
        # Calculer les centroïdes
        self.centroids = self.kmeans.cluster_centers_
        
        return cluster_labels
    
    def predict(self, user_features):
        """Prédire le cluster pour de nouvelles caractéristiques"""
        if self.kmeans is None:
            return None
        
        features_scaled = self.scaler.transform([user_features])
        return self.kmeans.predict(features_scaled)[0]
    
    def get_cluster_stats(self):
        """Obtenir les statistiques des clusters"""
        stats = {}
        
        for cluster_id in range(self.n_clusters):
            users_in_cluster = list(self.db.users.find(
                {'cluster_id': cluster_id},
                {'user_id': 1, 'age': 1, 'gender': 1, 'occupation': 1}
            ))
            
            if users_in_cluster:
                df_cluster = pd.DataFrame(users_in_cluster)
                
                stats[cluster_id] = {
                    'count': len(users_in_cluster),
                    'avg_age': df_cluster['age'].mean(),
                    'gender_dist': df_cluster['gender'].value_counts().to_dict(),
                    'occupation_dist': df_cluster['occupation'].value_counts().to_dict()
                }
        
        return stats
    
    def update_user_cluster(self, user_id):
        """Mettre à jour le cluster d'un utilisateur spécifique"""
        user = self.db.users.find_one({'user_id': user_id})
        
        if not user or self.kmeans is None:
            return None
        
        # Préparer les caractéristiques de l'utilisateur
        features = self._prepare_single_user_features(user)
        
        if features is None:
            return None
        
        # Prédire le cluster
        features_scaled = self.scaler.transform([features])
        cluster_id = self.kmeans.predict(features_scaled)[0]
        
        # Mettre à jour dans la base de données
        self.db.users.update_one(
            {'user_id': user_id},
            {
                '$set': {
                    'cluster_id': int(cluster_id),
                    'cluster_updated_at': datetime.now()
                }
            }
        )
        
        return cluster_id
    
    def _prepare_single_user_features(self, user):
        """Préparer les caractéristiques pour un seul utilisateur"""
        # Cette méthode serait plus complète si on avait l'encodeur sauvegardé
        # Pour simplifier, on va recréer les features de manière simplifiée
        try:
            age = user.get('age', 25)
            gender = user.get('gender', 'M')
            occupation = user.get('occupation', 'other')
            
            # Encodage simplifié
            gender_encoded = 1 if gender == 'M' else 0
            
            # Liste des occupations possibles (doit correspondre à l'entraînement)
            occupations = [
                'administrator', 'artist', 'doctor', 'educator', 'engineer',
                'entertainment', 'executive', 'healthcare', 'homemaker', 'lawyer',
                'librarian', 'marketing', 'none', 'other', 'programmer',
                'retired', 'salesman', 'scientist', 'student', 'technician', 'writer'
            ]
            
            occupation_encoded = [0] * len(occupations)
            if occupation in occupations:
                occupation_encoded[occupations.index(occupation)] = 1
            
            # Combiner toutes les caractéristiques
            features = [age, gender_encoded] + occupation_encoded
            return features
            
        except Exception as e:
            print(f"Erreur lors de la préparation des features: {e}")
            return None