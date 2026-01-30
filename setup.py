# setup.py
# probab supp
import subprocess
import sys

def install_requirements():
    """Installer les dépendances"""
    print("Installation des dépendances backend...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    print("\nInstallation des dépendances frontend...")
    subprocess.check_call(["npm", "install"], cwd="frontend")

def create_env_file():
    """Créer le fichier .env"""
    env_content = """# Backend Configuration
FLASK_APP=app.py
FLASK_ENV=development
JWT_SECRET_KEY=votre_cle_secrete_tres_longue_et_complexe
MONGO_URI=votre_uri_mongodb_atlas

# Frontend Configuration
REACT_APP_API_URL=http://localhost:5000
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("\nFichier .env créé. Veuillez remplir les valeurs appropriées.")

if __name__ == "__main__":
    print("=== Configuration du système de recommandation de films ===")
    
    # Créer la structure de dossiers
    import os
    folders = [
        'backend/offline',
        'backend/models',
        'backend/utils',
        'frontend/src/components/Auth',
        'frontend/src/components/Movies',
        'frontend/src/components/Recommendations',
        'frontend/src/components/Layout',
        'frontend/src/pages',
        'frontend/src/services',
        'frontend/src/context'
    ]
    
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
    
    # Installer les dépendances
    install_requirements()
    
    # Créer le fichier .env
    create_env_file()
    
    print("\n=== Configuration terminée ===")
    print("\nÉtapes suivantes:")
    print("1. Configurez MongoDB Atlas et mettez à jour MONGO_URI dans .env")
    print("2. Placez les fichiers u.data, u.user, u.item dans le dossier backend")
    print("3. Exécutez: python data_loader.py pour charger les données")
    print("4. Lancez le backend: python app.py")
    print("5. Lancez le frontend: npm start dans le dossier frontend")