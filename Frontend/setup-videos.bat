@echo off
REM setup-videos.bat - Script de configuration pour Windows

echo.
echo 🎬 Configuration MovieRecs - Videos et URLs
echo ===========================================
echo.

if not exist "Frontend\.env" (
    echo 📝 Creation du fichier Frontend\.env...
    (
        echo # YouTube API (pour bande-annonces YouTube^)
        echo # Obtenir une cle: https://console.cloud.google.com/
        echo VITE_YOUTUBE_API_KEY=votre_cle_youtube_ici
        echo.
        echo # TMDB API (Alternative recommandee^)
        echo # Obtenir une cle: https://www.themoviedb.org/api
        echo VITE_TMDB_API_KEY=votre_cle_tmdb_ici
        echo.
        echo # Backend API
        echo VITE_API_BASE=http://localhost:5000/api
    ) > Frontend\.env
    echo ✅ Fichier .env cree
) else (
    echo ✅ Fichier .env existe deja
)

echo.
echo 📚 Options de configuration:
echo.
echo Option 1: YouTube API (Bande-annonces YouTube^)
echo   1. Allez sur: https://console.cloud.google.com/
echo   2. Creez un nouveau projet
echo   3. Activez 'YouTube Data API v3'
echo   4. Creez une cle API
echo   5. Collez dans VITE_YOUTUBE_API_KEY
echo.

echo Option 2: TMDB API (Recommande - Plus simple^)
echo   1. Allez sur: https://www.themoviedb.org/api
echo   2. Creez un compte
echo   3. Generez une cle API
echo   4. Collez dans VITE_TMDB_API_KEY
echo.

echo Option 3: IMDb Link (Aucune configuration^)
echo   ✅ Deja fonctionnel - Lien vers page IMDb
echo.

echo 📝 Modifiez Frontend\.env avec vos cles API
echo Redemarrez le serveur apres modification:
echo.
echo   cd Frontend
echo   npm run dev
echo.

pause
