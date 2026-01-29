@echo off
REM commands.bat - Commandes rapides pour Windows

setlocal enabledelayedexpansion

REM Colors (Windows 10+ ou avec ANSI enabled)
set GREEN=[92m
set BLUE=[94m
set YELLOW=[93m
set RED=[91m
set NC=[0m

:main
if "%1"=="" (
    call :help
    goto :eof
)

if "%1"=="install" (
    call :install
    goto :eof
)

if "%1"=="start" (
    call :start
    goto :eof
)

if "%1"=="start_backend" (
    call :start_backend
    goto :eof
)

if "%1"=="check" (
    call :check
    goto :eof
)

if "%1"=="health" (
    call :health
    goto :eof
)

if "%1"=="test" (
    call :test
    goto :eof
)

if "%1"=="init_db" (
    call :init_db
    goto :eof
)

if "%1"=="docker_up" (
    call :docker_up
    goto :eof
)

if "%1"=="docker_down" (
    call :docker_down
    goto :eof
)

if "%1"=="api_health" (
    call :api_health
    goto :eof
)

if "%1"=="register_test" (
    call :register_test
    goto :eof
)

if "%1"=="login_test" (
    call :login_test
    goto :eof
)

if "%1"=="popular_movies" (
    call :popular_movies
    goto :eof
)

if "%1"=="help" (
    call :help
    goto :eof
)

echo Commande inconnue: %1
call :help
goto :eof

:install
echo.
echo Commandes pour installer:
echo.
echo   Etape 1: python install.py
echo   Etape 2: Editer .env avec votre MongoDB URI
echo   Etape 3: python check_requirements.py
echo   Etape 4: python start.py
echo.
python install.py
goto :eof

:start
echo.
echo Demarrage de l'application...
echo.
python start.py
goto :eof

:start_backend
echo.
echo Demarrage du backend uniquement...
echo.
cd Backend
python run.py
goto :eof

:check
echo.
echo Verification du systeme...
echo.
python check_requirements.py
goto :eof

:health
echo.
echo Verification de sante du systeme...
echo.
cd Backend
python healthcheck.py
goto :eof

:test
echo.
echo Execution des tests...
echo.
cd Backend
python -m pytest tests/ -v
goto :eof

:init_db
echo.
echo Initialisation de la base de donnees...
echo.
cd Backend
python scripts/init_db.py
goto :eof

:docker_up
echo.
echo Demarrage avec Docker Compose...
echo.
docker-compose up -d
echo.
echo Services en cours de demarrage:
echo.
echo   API: http://localhost:5000
echo   Frontend: http://localhost:3000
echo   MongoDB: mongodb://localhost:27017
echo.
goto :eof

:docker_down
echo.
echo Arret de Docker Compose...
echo.
docker-compose down
echo.
echo Services arretes.
echo.
goto :eof

:api_health
echo.
echo Sante de l'API...
echo.
curl http://localhost:5000/api/health
goto :eof

:register_test
echo.
echo Inscription d'un utilisateur de test...
echo.
curl -X POST http://localhost:5000/api/register ^
  -H "Content-Type: application/json" ^
  -d "{ \"email\": \"test@example.com\", \"password\": \"Test123!\", \"name\": \"Test User\" }"
echo.
goto :eof

:login_test
echo.
echo Connexion de l'utilisateur de test...
echo.
curl -X POST http://localhost:5000/api/login ^
  -H "Content-Type: application/json" ^
  -d "{ \"email\": \"test@example.com\", \"password\": \"Test123!\" }"
echo.
goto :eof

:popular_movies
echo.
echo Films populaires...
echo.
curl http://localhost:5000/api/movies/popular
echo.
goto :eof

:help
cls
echo.
echo ========================================
echo    MOVIES RECOMMENDER - COMMANDES
echo ========================================
echo.
echo INSTALLATION ET CONFIGURATION:
echo   commands install        - Installer le projet automatiquement
echo   commands check          - Verifier les prerequis
echo.
echo DEMARRAGE:
echo   commands start          - Menu de demarrage interactif
echo   commands start_backend  - Demarrer le backend uniquement
echo.
echo DOCKER:
echo   commands docker_up      - Demarrer avec Docker Compose
echo   commands docker_down    - Arreter Docker Compose
echo.
echo VERIFICATION:
echo   commands health         - Verification de sante
echo   commands api_health     - Sante de l'API
echo.
echo TESTS:
echo   commands test           - Executer les tests
echo.
echo BASE DE DONNEES:
echo   commands init_db        - Initialiser la BD
echo.
echo TESTS API:
echo   commands register_test  - Inscrire utilisateur test
echo   commands login_test     - Se connecter (test)
echo   commands popular_movies - Films populaires
echo.
echo AIDE:
echo   commands help           - Afficher cette aide
echo.
echo EXEMPLES:
echo   commands install        - Installation complète
echo   commands check          - Verifier l'installation
echo   commands start          - Demarrer l'appli
echo.
goto :eof
