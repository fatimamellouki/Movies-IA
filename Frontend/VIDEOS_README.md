# 🎬 Configuration Bande-Annonces

## Pour afficher les vidéos YouTube des bande-annonces:

1. **Obtenir une clé API YouTube:**
   - Allez sur: https://console.cloud.google.com/
   - Créez un nouveau projet
   - Activez "YouTube Data API v3"
   - Créez une clé API

2. **Configurez dans `Frontend/.env`:**
   ```
   VITE_YOUTUBE_API_KEY=votre_clé_ici
   ```

3. **Redémarrez le serveur:**
   ```bash
   cd Frontend
   npm run dev
   ```

Les vidéos s'afficheront maintenant dans la page de détail des films !
