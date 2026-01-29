#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de vérification des prérequis du système
Vérifie que tout est configuré correctement avant de démarrer
"""

import sys
import os
from pathlib import Path


def check_python_version():
    """Vérifier la version de Python"""
    print("📍 Python version")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} (OK)")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor} (Minimum: 3.8)")
        return False


def check_pip():
    """Vérifier pip"""
    print("\n📍 pip")
    try:
        import pip
        print(f"   ✅ pip {pip.__version__} (OK)")
        return True
    except ImportError:
        print("   ❌ pip non trouvé")
        return False


def check_venv():
    """Vérifier l'environnement virtuel"""
    print("\n📍 Environnement virtuel")
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print(f"   ✅ Actif: {sys.prefix}")
        return True
    else:
        print("   ⚠️  Non actif (recommandé: créer avec 'python -m venv venv')")
        return True  # Non-bloquant


def check_required_packages():
    """Vérifier les packages requis"""
    print("\n📍 Packages requis")
    
    required = [
        'flask',
        'flask_cors',
        'flask_jwt_extended',
        'pymongo',
        'pandas',
        'numpy',
        'sklearn',
        'bcrypt'
    ]
    
    all_ok = True
    for package in required:
        try:
            __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - Installer avec: pip install -r Backend/requirements.txt")
            all_ok = False
    
    return all_ok


def check_env_file():
    """Vérifier le fichier .env"""
    print("\n📍 Fichier .env")
    
    project_root = Path(__file__).parent
    env_file = project_root / ".env"
    env_example = project_root / ".env.example"
    
    if env_file.exists():
        # Vérifier les variables importantes
        with open(env_file, 'r') as f:
            content = f.read()
        
        required_vars = ['MONGO_URI', 'JWT_SECRET_KEY']
        missing = []
        
        for var in required_vars:
            if var not in content or f"{var}=votre" in content:
                missing.append(var)
        
        if missing:
            print(f"   ⚠️  Fichier présent mais variables manquantes: {', '.join(missing)}")
            print(f"   → Éditer .env et ajouter les bonnes valeurs")
            return False
        else:
            print(f"   ✅ Fichier configuré")
            return True
    
    elif env_example.exists():
        print(f"   ⚠️  .env n'existe pas (existe .env.example)")
        print(f"   → Exécuter: cp .env.example .env")
        return False
    
    else:
        print(f"   ❌ Aucun fichier .env trouvé")
        return False


def check_mongodb():
    """Vérifier MongoDB"""
    print("\n📍 MongoDB")
    
    try:
        from pymongo import MongoClient
        
        mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/movie_recommender')
        
        try:
            client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
            client.admin.command('ping')
            client.close()
            print(f"   ✅ MongoDB accessible")
            return True
        except Exception as e:
            print(f"   ⚠️  MongoDB non accessible")
            print(f"   → Assurez-vous que MongoDB est en cours d'exécution")
            print(f"   → Ou configurez MONGO_URI dans .env")
            return False
    
    except ImportError:
        print(f"   ❌ pymongo non installé")
        return False


def check_flask_app():
    """Vérifier l'application Flask"""
    print("\n📍 Application Flask")
    
    backend_dir = Path(__file__).parent / "Backend"
    app_file = backend_dir / "app.py"
    
    if app_file.exists():
        print(f"   ✅ app.py trouvé")
        return True
    else:
        print(f"   ❌ app.py non trouvé")
        return False


def check_ports():
    """Vérifier les ports disponibles"""
    print("\n📍 Ports")
    
    import socket
    
    ports = {
        5000: "Backend Flask",
        5432: "PostgreSQL (optionnel)",
        3000: "Frontend React (optionnel)"
    }
    
    for port, service in ports.items():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('127.0.0.1', port))
            sock.close()
            
            if result == 0:
                print(f"   ⚠️  Port {port} ({service}): EN UTILISATION")
            else:
                print(f"   ✅ Port {port} ({service}): Disponible")
        except:
            print(f"   ✅ Port {port} ({service}): Disponible")


def main():
    """Fonction principale"""
    print("=" * 60)
    print("  🔍 Vérification des prérequis du système")
    print("=" * 60)
    
    checks = [
        ("Python version", check_python_version),
        ("pip", check_pip),
        ("Environnement virtuel", check_venv),
        ("Packages requis", check_required_packages),
        ("Fichier .env", check_env_file),
        ("MongoDB", check_mongodb),
        ("Application Flask", check_flask_app),
    ]
    
    results = []
    
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Erreur lors de la vérification {name}: {e}")
            results.append((name, False))
    
    # Vérifier les ports (non-bloquant)
    try:
        check_ports()
    except:
        pass
    
    # Rapport final
    print("\n" + "=" * 60)
    print("  📋 Résumé")
    print("=" * 60)
    
    critical = [r for n, r in results if "Python" in n or "pip" in n or "Packages" in n or "Flask" in n]
    warnings = [r for n, r in results if not r and n not in ["Python version", "pip", "Packages requis", "Application Flask"]]
    
    critical_ok = all(critical)
    
    if critical_ok:
        print("✅ Tous les éléments critiques sont en place")
        
        if any(not r for _, r in results):
            print("⚠️  Mais certains avertissements doivent être corrigés:")
            for name, result in results:
                if not result and name not in ["Python version", "pip", "Packages requis", "Application Flask"]:
                    print(f"   • {name}")
        
        print("\n🚀 Vous pouvez démarrer avec:")
        print("   cd Backend")
        print("   python run.py")
        
        return 0
    else:
        print("❌ Des éléments critiques manquent:")
        for name, result in results:
            if not result and name in ["Python version", "pip", "Packages requis", "Application Flask"]:
                print(f"   • {name}")
        
        print("\n💡 Conseil: Exécuter install.py pour une installation automatique")
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrompu par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
