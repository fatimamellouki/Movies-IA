# DEPLOYMENT.md

## Guide de déploiement

Ce document explique comment déployer le système de recommandation de films en production.

## 📋 Prérequis

- Docker et Docker Compose (optionnel)
- Heroku CLI (pour Heroku)
- MongoDB Atlas (ou serveur MongoDB)
- Variables d'environnement configurées

## 🚀 Déploiement avec Heroku

### 1. Installer Heroku CLI

```bash
# Windows
choco install heroku-cli

# macOS
brew tap heroku/brew && brew install heroku

# Linux
curl https://cli.heroku.com/install.sh | sh
```

### 2. Créer l'application

```bash
heroku login
heroku create movies-recommendation-app
```

### 3. Configurer les variables d'environnement

```bash
heroku config:set FLASK_ENV=production
heroku config:set JWT_SECRET_KEY=<clé_secrète_long_aléatoire>
heroku config:set MONGO_URI=<uri_mongodb_atlas>
heroku config:set ADMIN_TOKEN=<token_admin_sécurisé>
heroku config:set CORS_ORIGINS=https://votreappfrontend.com
```

### 4. Déployer

```bash
# Avec Git
git push heroku main

# Ou avec Docker
heroku container:login
heroku container:push web
heroku container:release web
```

### 5. Vérifier le déploiement

```bash
heroku logs --tail
heroku open
```

## 🐳 Déploiement avec Docker

### 1. Construire l'image

```bash
docker build -t movies-app:latest .
```

### 2. Exécuter le conteneur

```bash
docker run -d \
  -p 5000:5000 \
  -e MONGO_URI=<uri_mongodb> \
  -e JWT_SECRET_KEY=<secret_key> \
  -e FLASK_ENV=production \
  --name movies-app \
  movies-app:latest
```

### 3. Avec Docker Compose

```bash
docker-compose -f docker-compose.yml up -d
```

## ☁️ Déploiement sur Azure

### 1. Créer une App Service

```bash
az group create --name movies-rg --location eastus
az appservice plan create --name movies-plan --resource-group movies-rg
az webapp create --name movies-app --resource-group movies-rg --plan movies-plan --runtime "PYTHON:3.10"
```

### 2. Configurer les variables d'environnement

```bash
az webapp config appsettings set --resource-group movies-rg --name movies-app \
  --settings FLASK_ENV=production \
  JWT_SECRET_KEY=<secret_key> \
  MONGO_URI=<uri_mongodb> \
  WEBSITES_PORT=5000
```

### 3. Déployer

```bash
git subtree push --prefix Backend azure main
```

## ☁️ Déploiement sur AWS

### 1. Avec Elastic Beanstalk

```bash
# Installer EB CLI
pip install awsebcli

# Initialiser
eb init -p "Python 3.10" movies-app

# Créer l'environnement
eb create movies-env

# Déployer
eb deploy
```

### 2. Avec EC2

```bash
# Créer une instance EC2
# Installer Python, pip, Git
ssh ec2-user@<instance-ip>

# Cloner et installer
git clone <repository>
cd movies_app/Backend
pip install -r requirements.txt

# Démarrer avec gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
```

## 🔒 Configuration de sécurité pour la production

### 1. Variables d'environnement

```env
FLASK_ENV=production
JWT_SECRET_KEY=<clé_très_longue_aléatoire>
ADMIN_TOKEN=<token_admin_sécurisé>
SECRET_KEY=<clé_secrète_sécurisée>
```

### 2. Base de données

- Utiliser MongoDB Atlas avec authentification
- Activer le chiffrement en transit
- Utiliser une liste blanche d'IP

### 3. API

- Configurer CORS correctement
- Utiliser HTTPS
- Limiter les taux de requête
- Valider toutes les entrées

### 4. En-têtes de sécurité

```python
# Dans app.py, ajouter:
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response
```

## 📊 Monitoring

### 1. Logs

```bash
# Heroku
heroku logs --tail

# Docker
docker logs -f movies-app

# Fichier
tail -f logs/app.log
```

### 2. Métriques

- Utiliser CloudWatch (AWS)
- Utiliser Application Insights (Azure)
- Utiliser Stackdriver (GCP)

## 🔄 Mise à jour continue (CI/CD)

### GitHub Actions

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Heroku
        uses: akhileshns/heroku-deploy@v3.12.12
        with:
          heroku_api_key: ${{ secrets.HEROKU_API_KEY }}
          heroku_app_name: "movies-app"
```

## 🆘 Dépannage

### Problème: Base de données non accessible

```bash
# Vérifier la connexion MongoDB
python Backend/healthcheck.py

# Vérifier l'URI
echo $MONGO_URI
```

### Problème: Application ne démarre pas

```bash
# Vérifier les logs
heroku logs --tail

# Vérifier la santé
curl https://movies-app.herokuapp.com/api/health
```

### Problème: Authentification JWT échoue

```bash
# Vérifier le token
echo $JWT_SECRET_KEY

# Tester la registration
curl -X POST https://movies-app.herokuapp.com/api/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!"}'
```

## 📝 Checklist de déploiement

- [ ] Variables d'environnement configurées
- [ ] MongoDB Atlas configuré et accessible
- [ ] HTTPS activé
- [ ] CORS configuré correctement
- [ ] Tests passés localement
- [ ] Logs activés
- [ ] Sauvegardes de base de données configurées
- [ ] Monitoring activé
- [ ] Alertes configurées
- [ ] Documentation mise à jour

## 🔗 Ressources utiles

- [Flask Production Deployment](https://flask.palletsprojects.com/deployment/)
- [Heroku Python Deployment](https://devcenter.heroku.com/articles/python-support)
- [MongoDB Atlas Security](https://docs.atlas.mongodb.com/security/)
- [Azure App Service Deployment](https://docs.microsoft.com/azure/app-service/deploy-continuous-deployment)
