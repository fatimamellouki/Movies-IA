# backend/wsgi.py
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

from app import app
from config import get_config

# Charger la configuration pour la production
config_name = os.getenv('FLASK_ENV', 'production')
config = get_config(config_name)
app.config.from_object(config)

# Pour les déploiements avec gunicorn
if __name__ == "__main__":
    app.run()