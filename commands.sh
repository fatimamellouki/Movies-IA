#!/bin/bash
# commands.sh - Commandes rapides pour le projet

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Header
print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
}

# Installation
install() {
    print_header "Installation du projet"
    python install.py
}

# Démarrage
start() {
    print_header "Démarrage de l'application"
    python start.py
}

# Backend seul
start_backend() {
    print_header "Démarrage du backend uniquement"
    cd Backend
    python run.py
}

# Vérification
check() {
    print_header "Vérification du système"
    python check_requirements.py
}

# Healthcheck
health() {
    print_header "Vérification de santé"
    cd Backend
    python healthcheck.py
}

# Tests
test() {
    print_header "Exécution des tests"
    cd Backend
    python -m pytest tests/ -v
}

# Initialiser BD
init_db() {
    print_header "Initialisation de la base de données"
    cd Backend
    python scripts/init_db.py
}

# Docker
docker_up() {
    print_header "Démarrage avec Docker Compose"
    docker-compose up -d
    echo -e "${GREEN}Services en cours de démarrage...${NC}"
    echo -e "${GREEN}API: http://localhost:5000${NC}"
    echo -e "${GREEN}Frontend: http://localhost:3000${NC}"
    echo -e "${GREEN}MongoDB: mongodb://localhost:27017${NC}"
}

docker_down() {
    print_header "Arrêt de Docker Compose"
    docker-compose down
    echo -e "${GREEN}Services arrêtés${NC}"
}

# API Health
api_health() {
    print_header "Santé de l'API"
    curl http://localhost:5000/api/health | python -m json.tool
}

# Register test user
register_test() {
    print_header "Inscription d'un utilisateur de test"
    curl -X POST http://localhost:5000/api/register \
      -H "Content-Type: application/json" \
      -d '{
        "email": "test@example.com",
        "password": "Test123!",
        "name": "Test User"
      }' | python -m json.tool
}

# Login test user
login_test() {
    print_header "Connexion de l'utilisateur de test"
    curl -X POST http://localhost:5000/api/login \
      -H "Content-Type: application/json" \
      -d '{
        "email": "test@example.com",
        "password": "Test123!"
      }' | python -m json.tool
}

# Get popular movies
popular_movies() {
    print_header "Films populaires"
    curl http://localhost:5000/api/movies/popular | python -m json.tool
}

# Aide
help() {
    cat << 'EOF'

🎬 Commandes disponibles pour le projet Movies Recommender:

📦 Installation et Configuration:
  ./commands.sh install        - Installer le projet automatiquement
  ./commands.sh check          - Vérifier les prérequis

🚀 Démarrage:
  ./commands.sh start          - Menu de démarrage interactif
  ./commands.sh start_backend  - Démarrer le backend uniquement

🐳 Docker:
  ./commands.sh docker_up      - Démarrer avec Docker Compose
  ./commands.sh docker_down    - Arrêter Docker Compose

🔍 Vérification:
  ./commands.sh health         - Vérification de santé du système
  ./commands.sh api_health     - Santé de l'API

🧪 Tests:
  ./commands.sh test           - Exécuter les tests unitaires

🗄️ Base de données:
  ./commands.sh init_db        - Initialiser la base de données

🧑‍💻 Tests API:
  ./commands.sh register_test  - Inscrire un utilisateur de test
  ./commands.sh login_test     - Se connecter (utilisateur test)
  ./commands.sh popular_movies - Afficher les films populaires

💡 Autres:
  ./commands.sh help           - Afficher cette aide

Exemples:
  # Installation complète (recommandée)
  ./commands.sh install
  
  # Vérifier que tout est en ordre
  ./commands.sh check
  
  # Démarrer l'application
  ./commands.sh start
  
  # Ou avec Docker
  ./commands.sh docker_up
  
  # Tester l'API
  ./commands.sh register_test
  ./commands.sh api_health

EOF
}

# Script principal
case "${1:-help}" in
    install)     install ;;
    start)       start ;;
    start_backend) start_backend ;;
    check)       check ;;
    health)      health ;;
    test)        test ;;
    init_db)     init_db ;;
    docker_up)   docker_up ;;
    docker_down) docker_down ;;
    api_health)  api_health ;;
    register_test) register_test ;;
    login_test)  login_test ;;
    popular_movies) popular_movies ;;
    help)        help ;;
    *)           echo -e "${RED}Commande inconnue: $1${NC}" && help ;;
esac
