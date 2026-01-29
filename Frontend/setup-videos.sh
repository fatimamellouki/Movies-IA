#!/bin/bash
# setup-videos.sh - Script de configuration des vidéos

echo "🎬 Configuration MovieRecs - Videos et URLs"
echo "==========================================="
echo ""

# Créer le fichier .env s'il n'existe pas
if [ ! -f "Frontend/.env" ]; then
    echo "📝 Création du fichier Frontend/.env..."
    cat > Frontend/.env << 'EOF'
# YouTube API (pour bande-annonces YouTube)
# Obtenir une clé: https://console.cloud.google.com/
VITE_YOUTUBE_API_KEY=votre_clé_youtube_ici

# TMDB API (Alternative recommandée)
# Obtenir une clé: https://www.themoviedb.org/api
VITE_TMDB_API_KEY=votre_clé_tmdb_ici

# Backend API
VITE_API_BASE=http://localhost:5000/api
EOF
    echo "✅ Fichier .env créé"
else
    echo "✅ Fichier .env existe déjà"
fi

echo ""
echo "📚 Options de configuration:"
echo ""
echo "Option 1: YouTube API (Bande-annonces YouTube)"
echo "  1. Allez sur: https://console.cloud.google.com/"
echo "  2. Créez un nouveau projet"
echo "  3. Activez 'YouTube Data API v3'"
echo "  4. Créez une clé API"
echo "  5. Collez dans VITE_YOUTUBE_API_KEY"
echo ""

echo "Option 2: TMDB API (Recommandé - Plus simple)"
echo "  1. Allez sur: https://www.themoviedb.org/api"
echo "  2. Créez un compte"
echo "  3. Générez une clé API"
echo "  4. Collez dans VITE_TMDB_API_KEY"
echo ""

echo "Option 3: IMDb Link (Aucune configuration)"
echo "  ✅ Déjà fonctionnel - Lien vers page IMDb"
echo ""

echo "📝 Modifiez Frontend/.env avec vos clés API"
echo "Redémarrez le serveur après modification:"
echo ""
echo "  cd Frontend"
echo "  npm run dev"
echo ""
