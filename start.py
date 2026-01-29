#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de démarrage rapide pour le système de recommandation de films
"""

import os
import sys
import subprocess
from pathlib import Path


def print_header(text):
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)


def print_success(text):
    print(f"✅ {text}")


def print_error(text):
    print(f"❌ {text}")


def print_info(text):
    print(f"ℹ️  {text}")


def main():
    project_root = Path(__file__).parent
    backend_dir = project_root / "Backend"
    
    print_header("🎬 Démarrage du Système de Recommandation")
    
    # Vérifier l'existence du fichier .env
    env_file = project_root / ".env"
    if not env_file.exists():
        print_error("Le fichier .env n'existe pas!")
        print_info("Créez-le en copiant .env.example et en le configurant")
        sys.exit(1)
    
    # Vérifier l'existence du Backend
    if not backend_dir.exists():
        print_error("Le dossier Backend n'existe pas!")
        sys.exit(1)
    
    # Déterminer la commande Python à utiliser
    if sys.platform == "win32":
        python_cmd = str(project_root / "venv" / "Scripts" / "python.exe")
        if not Path(python_cmd).exists():
            python_cmd = sys.executable
    else:
        python_cmd = str(project_root / "venv" / "bin" / "python")
        if not Path(python_cmd).exists():
            python_cmd = sys.executable
    
    print_info(f"Utilisation de Python: {python_cmd}")
    
    # Options de démarrage
    print_header("Options de démarrage")
    print("""
    1. Démarrer le backend uniquement
    2. Démarrer avec Docker Compose
    3. Développement complet (backend + frontend)
    0. Quitter
    """)
    
    choice = input("Sélectionnez une option (0-3): ").strip()
    
    if choice == "1":
        print_header("Démarrage du backend")
        print_info("Assurez-vous que MongoDB est accessible...")
        print_info(f"API disponible sur: http://localhost:5000")
        
        os.chdir(backend_dir)
        result = subprocess.run([python_cmd, "run.py"])
        sys.exit(result.returncode)
    
    elif choice == "2":
        print_header("Démarrage avec Docker Compose")
        print_info("Assurez-vous que Docker est installé...")
        
        os.chdir(project_root)
        result = subprocess.run(["docker-compose", "up"])
        sys.exit(result.returncode)
    
    elif choice == "3":
        print_header("Mode développement complet")
        print_info("Démarrage du backend...")
        
        os.chdir(backend_dir)
        backend_process = subprocess.Popen([python_cmd, "run.py"])
        
        print_success("Backend en cours de démarrage...")
        print_info("Frontend: npm start (dans un autre terminal)")
        
        try:
            backend_process.wait()
        except KeyboardInterrupt:
            print_info("\nArrêt du backend...")
            backend_process.terminate()
            backend_process.wait()
    
    elif choice == "0":
        print_info("Annulé")
        sys.exit(0)
    
    else:
        print_error("Option invalide")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Arrêt")
        sys.exit(0)
