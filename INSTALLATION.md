# INSTALLATION.md

## Guide d'installation détaillé

Ce guide vous montre comment configurer et démarrer le système de recommandation de films.

## 📋 Prérequis

- **Python 3.8+** - [Télécharger](https://www.python.org/downloads/)
- **MongoDB** - [Atlas Cloud](https://www.mongodb.com/cloud/atlas) ou [Installation locale](https://docs.mongodb.com/manual/installation/)
- **Node.js 14+** (optionnel, pour le frontend) - [Télécharger](https://nodejs.org/)
- **Git** - [Télécharger](https://git-scm.com/)

## 🔧 Installation Rapide (3 étapes)

### Étape 1: Cloner et installer

```bash
# Cloner le repository
git clone <repository_url>
cd movies_app

# Exécuter le script d'installation
python install.py
```

### Étape 2: Configurer

```bash
# Copier le fichier de configuration
cp .env.example .env

# Éditer .env avec vos paramètres MongoDB et clés JWT
# (Utiliser un éditeur de texte)
```

### Étape 3: Démarrer

```bash
# Option 1: Script de démarrage automatique
python start.py

# Option 2: Démarrage manuel
cd Backend
python run.py
```

## 📖 Installation Détaillée

### 1. Cloner le repository

```bash
git clone <repository_url>
cd movies_app
```

### 2. Créer un environnement virtuel Python

#### Windows:
```cmd
python -m venv venv
venv\Scripts\activate
```

#### macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Installer les dépendances

```bash
# Backend
cd Backend
pip install -r requirements.txt

# Frontend (optionnel)
cd ../frontend
npm install
```

### 4. Configuration MongoDB

#### Option A: MongoDB Atlas (Recommandé pour production)

1. Créer un compte sur [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Créer un cluster gratuit
3. Créer un utilisateur database
4. Obtenir la chaîne de connexion:
   ```
   mongodb+srv://username:password@cluster.mongodb.net/movie_recommender?retryWrites=true&w=majority
   ```

#### Option B: MongoDB Local

```bash
# Installation Windows
choco install mongodb-community

# Installation macOS
brew tap mongodb/brew
brew install mongodb-community

# Installation Linux (Ubuntu)
sudo apt-get install -y mongodb

# Démarrer le service
# Windows: mongo
# macOS/Linux: mongod
```

### 5. Configurer les variables d'environnement

```bash
# Copier le fichier exemple
cp .env.example .env

# Éditer .env (utiliser un éditeur de texte)
nano .env  # ou vim, code, etc.
```

**Variables essentielles à configurer:**

```env
# MongoDB
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/movie_recommender

# Sécurité (générer des valeurs aléatoires)
JWT_SECRET_KEY=votre_clé_très_longue_et_aléatoire_minimum_32_caractères
ADMIN_TOKEN=votre_token_admin_sécurisé

# Flask
FLASK_ENV=development
FLASK_DEBUG=1
```

### 6. Initialiser la base de données

```bash
cd Backend

# Option 1: Avec le script d'initialisation
python scripts/init_db.py

# Option 2: Avec la route API (après démarrage)
curl -X POST http://localhost:5000/admin/init-db \
  -H "Authorization: Bearer admin-secret-token" \
  -H "Content-Type: application/json"
```

### 7. Vérifier la santé du système

```bash
cd Backend
python healthcheck.py
```

Vous devriez voir:
```
✅ MongoDB connecté
✅ API disponible
✅ Tout est en ordre!
```

### 8. Démarrer le serveur

```bash
cd Backend
python run.py
```

Vous devriez voir:
```
==================================================
  🚀 Démarrage du serveur Flask
==================================================
📍 Adresse: 127.0.0.1:5000
🔧 Environnement: development
🐛 Debug: True
==================================================
```

L'API est maintenant disponible sur: **http://localhost:5000**

## 🚀 Démarrage du Frontend (Optionnel)

```bash
cd frontend
npm start
```

Le frontend sera disponible sur: **http://localhost:3000**

## 🐳 Déploiement avec Docker

### Sans Docker Compose:

```bash
# Construire l'image
docker build -t movies-app .

# Exécuter le conteneur
docker run -d -p 5000:5000 \
  -e MONGO_URI=<uri_mongodb> \
  -e JWT_SECRET_KEY=<secret_key> \
  --name movies-app \
  movies-app
```

### Avec Docker Compose:

```bash
# Démarrer tous les services
docker-compose up -d

# Voir les logs
docker-compose logs -f

# Arrêter
docker-compose down
```

## ✅ Tests de vérification

### 1. Santé de l'API

```bash
curl http://localhost:5000/api/health
```

Réponse attendue:
```json
{"status": "healthy", "timestamp": "..."}
```

### 2. Films populaires

```bash
curl http://localhost:5000/api/movies/popular
```

### 3. Inscription

```bash
curl -X POST http://localhost:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test123!",
    "name": "Test User"
  }'
```

### 4. Connexion

```bash
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test123!"
  }'
```

## 🔧 Configuration avancée

### Variables d'environnement supplémentaires

```env
# Base de données
MONGO_URI_DEV=mongodb://localhost:27017/movie_recommender_dev
MONGO_URI_TEST=mongodb://localhost:27017/movie_recommender_test

# Recommandations
RECOMMENDATION_N_CLUSTERS=5
RECOMMENDATION_SIMILARITY_THRESHOLD=0.1
RECOMMENDATION_MIN_RATINGS=5

# Chemins
MODEL_SAVE_PATH=./models
DATA_SAVE_PATH=./data

# Frontend
REACT_APP_API_URL=http://localhost:5000
REACT_APP_API_TIMEOUT=30000

# Port et Host
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
```

### Configuration des dépendances supplémentaires

```bash
# Linting et formatage du code
pip install pylint black flake8

# Tests
pip install pytest pytest-cov

# Déploiement
pip install gunicorn
```

## 🆘 Dépannage

### Problème: "Module not found"

```bash
# Réinstaller les dépendances
pip install --upgrade -r Backend/requirements.txt
```

### Problème: "Connection refused" (MongoDB)

```bash
# Vérifier que MongoDB est en cours d'exécution
mongosh  # ou mongo

# Ou pour le service:
# Windows: net start MongoDB
# macOS: brew services start mongodb-community
# Linux: sudo systemctl start mongod
```

### Problème: "Port already in use"

```bash
# Changer le port dans .env
FLASK_PORT=5001

# Ou libérer le port existant
# Windows: netstat -ano | findstr :5000
# macOS/Linux: lsof -i :5000
```

### Problème: Variables d'environnement non chargées

```bash
# Windows: Redémarrer l'invite de commande/PowerShell
# macOS/Linux: Fermer et rouvrir le terminal

# Ou recharger manuellement:
source venv/bin/activate
```

## 📚 Ressources utiles

- [Flask Documentation](https://flask.palletsprojects.com/)
- [MongoDB Documentation](https://docs.mongodb.com/)
- [JWT Documentation](https://jwt.io/)
- [scikit-learn Documentation](https://scikit-learn.org/)
- [Python-dotenv Documentation](https://github.com/theskumar/python-dotenv)

## 🎓 Prochaines étapes

1. ✅ Installer et configurer le backend
2. 📚 Lire la [Documentation API](Backend/API_ROUTES.md)
3. 📱 Installer et configurer le [Frontend](frontend/README.md)
4. 🧪 Exécuter les tests: `pytest Backend/tests/`
5. 🚀 Déployer en production: [Guide de déploiement](DEPLOYMENT.md)

## 💡 Conseils

- Utilisez toujours un environnement virtuel Python
- Ne commitez jamais votre fichier `.env` sur Git
- Générez de nouvelles clés JWT pour la production
- Testez localement avant de déployer
- Activez HTTPS en production
- Configurez les sauvegardes de base de données

## 📞 Support

Pour des questions ou des problèmes:
1. Vérifiez le fichier de logs: `Backend/logs/app.log`
2. Consultez la section Dépannage
3. Créez une issue sur GitHub
4. Contactez le support technique
