#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script d'installation et de configuration du système de recommandation de films
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


class Installer:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.backend_dir = self.project_root / "Backend"
        self.frontend_dir = self.project_root / "frontend"

    def print_header(self, text):
        """Afficher un en-tête"""
        print("\n" + "=" * 60)
        print(f"  {text}")
        print("=" * 60)

    def print_success(self, text):
        """Afficher un message de succès"""
        print(f"✅ {text}")

    def print_error(self, text):
        """Afficher une erreur"""
        print(f"❌ {text}")

    def print_info(self, text):
        """Afficher une information"""
        print(f"ℹ️  {text}")

    def run_command(self, command, cwd=None):
        """Exécuter une commande"""
        try:
            result = subprocess.run(
                command,
                cwd=cwd,
            )
            return result.returncode == 0
        except Exception as e:
            self.print_error(f"Erreur lors de l'exécution: {e}")
            return False

    def create_venv(self):
        """Créer l'environnement virtuel"""
        self.print_header("Création de l'environnement virtuel Python")
        
        venv_path = self.project_root / "venv"
        
        if venv_path.exists():
            self.print_info("L'environnement virtuel existe déjà")
            return True
        
        self.print_info("Création de l'environnement virtuel...")
        result = self.run_command("py -3.11 -m venv venv")

        if result:
            self.print_success("Environnement virtuel créé")
        else:
            self.print_error("Impossible de créer l'environnement virtuel")
        
        return result

    def install_backend_dependencies(self):
        """Installer les dépendances du backend"""
        self.print_header("Installation des dépendances Backend")
        
        requirements_file = self.backend_dir / "requirements.txt"
        
        if not requirements_file.exists():
            self.print_error(f"Fichier requirements.txt introuvable: {requirements_file}")
            return False
        
        self.print_info(f"Installation depuis {requirements_file}")
        
        # Déterminer la commande pip
        if sys.platform == "win32":
            pip_cmd = str(self.project_root / "venv" / "Scripts" / "pip.exe")
        else:
            pip_cmd = str(self.project_root / "venv" / "bin" / "pip")
        
        result = self.run_command(f"{pip_cmd} install -r {requirements_file}")
        
        if result:
            self.print_success("Dépendances backend installées")
        else:
            self.print_error("Erreur lors de l'installation des dépendances")
        
        return result

    def install_frontend_dependencies(self):
        """Installer les dépendances du frontend"""
        self.print_header("Installation des dépendances Frontend")
        
        if not self.frontend_dir.exists():
            self.print_error(f"Dossier frontend introuvable: {self.frontend_dir}")
            return False
        
        if not shutil.which("npm"):
            self.print_error("npm n'est pas installé. Veuillez installer Node.js")
            return False
        
        self.print_info("Installation des dépendances npm...")
        result = self.run_command("npm install", cwd=self.frontend_dir)
        
        if result:
            self.print_success("Dépendances frontend installées")
        else:
            self.print_error("Erreur lors de l'installation des dépendances frontend")
        
        return result

    def create_env_file(self):
        """Créer le fichier .env"""
        self.print_header("Configuration des variables d'environnement")
        
        env_file = self.project_root / ".env"
        env_example = self.project_root / ".env.example"
        
        if env_file.exists():
            self.print_info("Le fichier .env existe déjà")
            return True
        
        if env_example.exists():
            self.print_info("Copie de .env.example vers .env...")
            shutil.copy(env_example, env_file)
            self.print_success("Fichier .env créé")
            self.print_info("⚠️  Veuillez éditer .env et ajouter vos paramètres MongoDB et les clés JWT")
        else:
            self.print_error("Fichier .env.example introuvable")
            return False
        
        return True

    def create_directories(self):
        """Créer les répertoires nécessaires"""
        self.print_header("Création des répertoires")
        
        directories = [
            self.project_root / "models",
            self.project_root / "data",
            self.project_root / "logs",
            self.backend_dir / "models",
            self.backend_dir / "offline",
            self.backend_dir / "utils",
            self.backend_dir / "scripts",
            self.backend_dir / "tests"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            self.print_info(f"Dossier créé: {directory.relative_to(self.project_root)}")
        
        self.print_success("Tous les répertoires ont été créés")
        return True

    def show_next_steps(self):
        """Afficher les prochaines étapes"""
        self.print_header("Installation terminée! 🎉")
        
        print("""
Les prochaines étapes:

1. ✅ Éditer le fichier .env avec vos paramètres:
   - MONGO_URI: Votre URI de connexion MongoDB Atlas
   - JWT_SECRET_KEY: Générer une clé secrète (min 32 caractères)
   - ADMIN_TOKEN: Générer un token admin

2. 📚 Charger les données de films:
   cd Backend
   python scripts/load_movies.py

3. 🚀 Démarrer le serveur:
   cd Backend
   python run.py

4. 📱 Démarrer le frontend:
   cd frontend
   npm start

5. 🌐 Accéder à l'application:
   Frontend: http://localhost:3000
   Backend API: http://localhost:5000

Pour plus d'informations, consultez le README.md
""")

    def run_installation(self):
        """Exécuter l'installation complète"""
        self.print_header("🎬 Installation du Système de Recommandation de Films")
        
        steps = [
            ("Création de l'environnement virtuel", self.create_venv),
            ("Installation des dépendances backend", self.install_backend_dependencies),
            ("Création des répertoires", self.create_directories),
            ("Configuration de l'environnement", self.create_env_file),
        ]
        
        for step_name, step_func in steps:
            try:
                if not step_func():
                    self.print_error(f"Étape échouée: {step_name}")
                    return False
            except Exception as e:
                self.print_error(f"Erreur lors de {step_name}: {e}")
                return False
        
        self.show_next_steps()
        return True


def main():
    """Fonction principale"""
    installer = Installer()
    
    try:
        success = installer.run_installation()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Installation annulée par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erreur non gérée: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
