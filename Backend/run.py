# backend/run.py
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from config import get_config
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

if __name__ == '__main__':
    # Charger la configuration basée sur l'environnement
    config_name = os.getenv('FLASK_ENV', 'development')
    config = get_config(config_name)
    app.config.from_object(config)
    
    # Démarrer l'application
    port = int(os.getenv('FLASK_PORT', 5000))
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    
    print("=" * 50)
    print("🚀 Démarrage du serveur Flask")
    print("=" * 50)
    print(f"📍 Adresse: {host}:{port}")
    print(f"🔧 Environnement: {config_name}")
    print(f"🐛 Debug: {config.DEBUG}")
    print("=" * 50)
    
    app.run(host=host, port=port, debug=config.DEBUG)