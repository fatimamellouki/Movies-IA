# QUICKSTART.md

## 🚀 Démarrage Rapide (5 minutes)

Mettez en place et lancez le système en quelques commandes.

## ⚡ Option 1: Installation Automatique (Recommandée)

```bash
# 1. Installer et configurer
python install.py

# 2. Éditer le fichier .env
# Ajouter votre URI MongoDB et générer des clés JWT

# 3. Démarrer l'application
python start.py

# Choisir l'option 1 pour le backend uniquement
```

**Durée: 5-10 minutes**

---

## 🐳 Option 2: Docker (La plus simple)

```bash
# 1. Démarrer tous les services (MongoDB + Backend + Frontend)
docker-compose up -d

# 2. Attendre 30 secondes pour que MongoDB démarre

# 3. Initialiser la base de données
docker-compose exec backend python scripts/init_db.py
```

**L'API est disponible sur: http://localhost:5000**
**Le Frontend est disponible sur: http://localhost:3000**

---

## 📝 Option 3: Installation Manuelle

### Étape 1: Configuration

```bash
# Cloner le projet
git clone <url>
cd movies_app

# Copier le fichier d'environnement
cp .env.example .env

# Éditer .env (ajouter votre MongoDB URI)
# Exemples:
# MONGO_URI=mongodb+srv://user:pass@cluster.mongodb.net/movie_recommender
# JWT_SECRET_KEY=your_secret_key_min_32_chars
```

### Étape 2: Python

```bash
# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement (Windows)
venv\Scripts\activate
# Ou (macOS/Linux)
source venv/bin/activate

# Installer les dépendances
cd Backend
pip install -r requirements.txt
```

### Étape 3: Base de données

```bash
# Initialiser MongoDB
python scripts/init_db.py
```

### Étape 4: Démarrer

```bash
# Démarrer le serveur
python run.py
```

**L'API est maintenant sur: http://localhost:5000**

---

## ✅ Vérification du fonctionnement

### 1. Santé du système

```bash
curl http://localhost:5000/api/health
```

Réponse attendue:
```json
{"status": "healthy", "timestamp": "2024-01-01T10:00:00"}
```

### 2. Films populaires

```bash
curl http://localhost:5000/api/movies/popular
```

### 3. Test d'inscription

```bash
curl -X POST http://localhost:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test123!",
    "name": "Test User"
  }'
```

Réponse attendue:
```json
{"message": "Utilisateur créé avec succès", "user_id": 1}
```

---

## 🔐 Configuration MongoDB Atlas (Gratuit)

1. **Aller sur** https://www.mongodb.com/cloud/atlas
2. **Créer un compte** (gratuit)
3. **Créer un cluster** (M0 gratuit)
4. **Ajouter un utilisateur** database
5. **Obtenir la chaîne de connexion:**
   ```
   mongodb+srv://username:password@cluster.mongodb.net/movie_recommender
   ```
6. **Ajouter dans .env:**
   ```env
   MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/movie_recommender
   ```

---

## 🌐 Accéder à l'application

### Backend API
- **URL**: http://localhost:5000
- **Health check**: http://localhost:5000/api/health
- **Documentation API**: Voir `Backend/API_ROUTES.md`

### Frontend (optionnel)
- **URL**: http://localhost:3000
- **Démarrer**: `cd frontend && npm start`

---

## 🐛 Débogage

### L'API ne démarre pas?

```bash
# Vérifier la santé du système
python Backend/healthcheck.py

# Voir les logs détaillés
cd Backend
python run.py  # Affiche tous les logs en temps réel
```

### MongoDB n'est pas accessible?

```bash
# Vérifier l'URI
echo $MONGO_URI

# Test de connexion
mongosh "mongodb+srv://user:pass@cluster.mongodb.net/"
```

### Port déjà utilisé?

```bash
# Changer le port dans .env
echo "FLASK_PORT=5001" >> .env

# Ou libérer le port (Windows)
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

---

## 📚 Documentation complète

- **Installation détaillée**: Lire [INSTALLATION.md](INSTALLATION.md)
- **Déploiement**: Lire [DEPLOYMENT.md](DEPLOYMENT.md)
- **Documentation API**: Lire [Backend/API_ROUTES.md](Backend/API_ROUTES.md)
- **Résumé des changements**: Lire [SUMMARY.md](SUMMARY.md)

---

## 🎯 Prochaines étapes

### Pour développer:
1. Familiarisez-vous avec la [documentation API](Backend/API_ROUTES.md)
2. Lancez les [tests](Backend/tests/)
3. Explorez le code dans le dossier `Backend/`

### Pour déployer:
1. Lisez [DEPLOYMENT.md](DEPLOYMENT.md)
2. Configurez vos variables d'environnement de production
3. Déployez sur votre plateforme (Heroku, AWS, Azure, etc.)

### Pour ajouter des fonctionnalités:
1. Créez une nouvelle branche: `git checkout -b feature/ma-feature`
2. Ajoutez votre code et testez
3. Créez une pull request

---

## 💡 Commandes utiles

```bash
# Vérification de santé
python Backend/healthcheck.py

# Tests
pytest Backend/tests/ -v

# Initialiser la BD
python Backend/scripts/init_db.py

# Voir les logs en temps réel
tail -f Backend/logs/app.log

# Exécuter les calculs offline (clustering)
curl -X POST http://localhost:5000/admin/run-offline \
  -H "Authorization: Bearer admin-secret-token"

# Récupérer les statistiques
curl -X GET http://localhost:5000/admin/stats \
  -H "Authorization: Bearer admin-secret-token"
```

---

## 🆘 Besoin d'aide?

1. **Consultez la documentation**:
   - [INSTALLATION.md](INSTALLATION.md) - Résolution des problèmes
   - [DEPLOYMENT.md](DEPLOYMENT.md) - Erreurs de déploiement
   - [Backend/API_ROUTES.md](Backend/API_ROUTES.md) - Utilisation de l'API

2. **Exécutez le healthcheck**:
   ```bash
   python Backend/healthcheck.py
   ```

3. **Vérifiez les logs**:
   ```bash
   tail -f Backend/logs/app.log
   ```

---

## 🎉 Vous êtes prêt!

Le système de recommandation de films est maintenant en cours d'exécution.

Explorez l'API, créez un utilisateur, notez des films et découvrez les recommandations!

**Amusez-vous! 🎬**
