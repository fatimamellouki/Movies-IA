# 🎬 Movies Recommendation System

Un système de recommandation de films basé sur le machine learning avec clustering d'utilisateurs et algorithmes hybrides.

## 📋 Fonctionnalités

- ✅ Authentification JWT
- ✅ Système de recommandation hybride (collaborative, content-based, cluster-based)
- ✅ Clustering automatique des utilisateurs
- ✅ Calculs offline optimisés
- ✅ API REST complète avec Flask
- ✅ Base de données MongoDB Atlas
- ✅ Support CORS

## 🚀 Installation

### Prérequis
- Python 3.8+
- MongoDB Atlas (ou instance MongoDB locale)
- Node.js 14+ (pour le frontend)

### 1. Cloner et installer le backend

```bash
# Cloner le repository
git clone <repository_url>
cd movies_app

# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
# Sur Windows:
venv\Scripts\activate
# Sur macOS/Linux:
source venv/bin/activate

# Installer les dépendances
cd Backend
pip install -r requirements.txt
```

### 2. Configuration de l'environnement

```bash
# Copier le fichier de configuration
cp ../.env.example ../.env

# Éditer le fichier .env avec vos paramètres
# - Ajouter votre URI MongoDB Atlas
# - Générer des clés JWT sécurisées
```

### 3. Démarrer le backend

```bash
# Depuis le dossier Backend
python run.py
```

Le serveur démarre sur `http://localhost:5000`

## 📚 API Endpoints

### Authentification
- `POST /api/register` - Créer un compte
- `POST /api/login` - Se connecter

### Films
- `GET /api/movies/popular` - Films populaires (public)
- `GET /api/movies` - Liste des films (authentifié)
- `GET /api/movies/search` - Rechercher des films (authentifié)

### Recommandations
- `GET /api/recommendations/first-time` - Recommandations première connexion
- `GET /api/recommendations/personalized` - Recommandations personnalisées

### Utilisateur
- `POST /api/rate` - Noter un film
- `GET /api/user/stats` - Statistiques de l'utilisateur

### Administration
- `POST /admin/init-db` - Initialiser la base de données
- `POST /admin/run-offline` - Exécuter les calculs offline

## 🏗️ Structure du projet

```
Backend/
├── app.py                 # Application Flask principale
├── config.py             # Configuration (dev, test, prod)
├── run.py               # Script de lancement
├── wsgi.py              # Entry point WSGI
├── requirements.txt     # Dépendances Python
├── models/
│   ├── __init__.py
│   └── user_model.py    # Modèles Pydantic
├── offline/
│   ├── recommender.py   # Moteur de recommandation hybride
│   ├── clustering.py    # Clustering des utilisateurs
│   └── similarity.py    # Calculs de similarité
├── utils/
│   ├── database.py      # Connexion MongoDB
│   ├── security.py      # Hachage et JWT
│   └── validators.py    # Validation des données
├── scripts/
│   ├── load_movies.py   # Charger les films
│   └── admin_tasks.py   # Tâches administratives
└── tests/
    └── test.py          # Tests
```

## 🔐 Configuration de production

Pour le déploiement en production:

```bash
# Utiliser gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app

# Ou avec Docker
docker build -t movies-app .
docker run -p 5000:5000 movies-app
```

## 🧪 Tests

```bash
# Depuis le dossier Backend
python -m pytest tests/
```

## 📊 Charger des données

```bash
# Charger les films depuis les fichiers de données
python scripts/load_movies.py

# Exécuter les calculs offline
curl -X POST http://localhost:5000/admin/run-offline \
  -H "Authorization: Bearer admin-secret-token" \
  -H "Content-Type: application/json"
```

## 🔍 Traçage des erreurs

Tous les logs sont affichés dans la console et incluent les traces complètes des erreurs.

## 📝 Variables d'environnement

| Variable | Description | Exemple |
|----------|-------------|---------|
| `FLASK_ENV` | Environnement (development/production) | `development` |
| `FLASK_DEBUG` | Mode debug | `1` |
| `MONGO_URI` | URI de connexion MongoDB | `mongodb+srv://...` |
| `JWT_SECRET_KEY` | Clé secrète JWT | (clé aléatoire) |
| `ADMIN_TOKEN` | Token pour les routes admin | (clé aléatoire) |
| `CORS_ORIGINS` | Origines autorisées pour CORS | `http://localhost:3000` |

## 🤝 Contribution

Les contributions sont les bienvenues! Merci de respecter les conventions de code existantes.

## 📄 License

MIT License - voir le fichier LICENSE pour plus de détails
