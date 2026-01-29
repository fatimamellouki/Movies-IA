# 🎬 Configuration - URLs IMDB et Vidéos

## Options pour Afficher les Vidéos

Vous avez 3 options pour afficher les bandes-annonces:

### **Option 1: Lien IMDB Simple** ✅ (Sans configuration)
- Affiche un lien cliquable vers la page IMDb du film
- **Avantages**: Pas de configuration, rapide, lien officiel
- **Inconvénient**: Redirige vers IMDb externe

**Déjà implémenté dans MovieDetail.jsx** - Bouton "Voir sur IMDb"

---

### **Option 2: Vidéo YouTube (Bande-annonce)** 🎥 (Recommandé)
- Cherche automatiquement la bande-annonce sur YouTube
- Affiche la vidéo en embed directement dans le site
- **Avantages**: Meilleure UX, vidéo intégrée, recherche auto
- **Inconvénient**: Nécessite une clé API YouTube (gratuite)

#### Configuration:

**1. Obtenez une clé API YouTube:**
- Allez sur [Google Cloud Console](https://console.cloud.google.com/)
- Créez un nouveau projet
- Activez YouTube Data API v3
- Créez une clé API (type: Clé API simple)

**2. Configurez la variable d'environnement:**

Créez un fichier `.env` dans le dossier `Frontend/`:
```env
VITE_YOUTUBE_API_KEY=votre_clé_api_ici
```

**3. Redémarrez le serveur dev:**
```bash
npm run dev
```

**Exemple avec clé:**
```env
VITE_YOUTUBE_API_KEY=AIzaSyDfXKYXYXYXYXYXYXYXYXYXYXYXYX
```

---

### **Option 3: Base de données locale de vidéos** 📁
Stockez les URLs YouTube/vidéo dans la base de données

#### Modifiez le schéma MongoDB:

```javascript
// Dans data_loader.py, ajouter à movie_record:
movie_record = {
  // ... champs existants ...
  'imdb_url': str(row['imdb_url']),
  'youtube_trailer_id': None,  // À remplir manuellement
  'poster_url': None,
  'backdrop_url': None,
  'video_url': None  // URL personnalisée
}
```

#### Complétez avec des URLs:

```bash
# Script pour ajouter les videos (Optional)
db.movies.updateMany(
  { movie_id: 1 },
  { $set: { youtube_trailer_id: "dQw4w9WgXcQ" } }
)
```

---

## Structure Fichiers

```
Frontend/src/
├── components/
│   └── VideoPlayer.jsx          # Composant vidéo (nouveau)
├── pages/
│   └── MovieDetail.jsx          # Affiche la vidéo + IMDB link
```

---

## Utilisation dans le Code

### **Dans MovieDetail.jsx:**

```jsx
import VideoPlayer from '../components/VideoPlayer'

// Dans le rendu:
<VideoPlayer 
  movieTitle={movie.title}           // "Toy Story"
  movieYear={movie.year}             // 1995
  imdbUrl={movie.imdb_url}           // "http://us.imdb.com/M/..."
  onVideoFound={(url) => console.log(url)}  // Callback optionnel
/>
```

### **VideoPlayer Props:**

| Prop | Type | Requis | Description |
|------|------|--------|---|
| `movieTitle` | string | ✅ | Titre du film |
| `movieYear` | number | ✅ | Année de sortie |
| `imdbUrl` | string | ❌ | URL IMDb du film |
| `onVideoFound` | function | ❌ | Callback quand vidéo trouvée |

---

## Résultats Attendus

### Avec API YouTube (Option 2):
```
┌─────────────────────────────────┐
│  🎬 Toy Story (1995)            │
│  ┌───────────────────────────┐  │
│  │ [Vidéo YouTube intégrée]  │  │ ← Bande-annonce
│  │ (33 min)                  │  │
│  └───────────────────────────┘  │
│  ⭐ 8.5/5 (500 évaluations)      │
│  [Voir sur IMDb] [⭐ Noter]      │
└─────────────────────────────────┘
```

### Sans API YouTube (Fallback):
```
┌─────────────────────────────────┐
│  🎬 Toy Story (1995)            │
│  ┌───────────────────────────┐  │
│  │ Aucune vidéo disponible   │  │
│  └───────────────────────────┘  │
│  ⭐ 8.5/5 (500 évaluations)      │
│  [Voir sur IMDb] [⭐ Noter]      │
└─────────────────────────────────┘
```

---

## Alternatives Gratuites

Si pas d'API YouTube:

### 1. **IMDb Embed** (Officiel)
```html
<iframe src="https://www.imdb.com/title/tt0114709/" width="100%" height="500"></iframe>
```

### 2. **JustWatch**
Lien vers où regarder légalement:
```javascript
`https://www.justwatch.com/search?q=${encodeURIComponent(movieTitle)}`
```

### 3. **The Movie Database (TMDB)**
API gratuite avec vidéos:
```bash
# Obtenir clé: https://www.themoviedb.org/api
GET https://api.themoviedb.org/3/search/movie?query={query}&api_key={key}
```

---

## Résumé des Options

| Option | Coût | Effort | UX | Recommandé |
|--------|------|--------|----|----|
| IMDb Link | Gratuit | ⚡ Facile | ⭐⭐ | ✓ Initial |
| YouTube API | Gratuit | ⭐ Normal | ⭐⭐⭐⭐⭐ | ✓ Meilleur |
| BD Locale | Gratuit | ⭐⭐ Moyen | ⭐⭐⭐ | ✓ Pour scale |
| TMDB API | Gratuit | ⭐ Normal | ⭐⭐⭐⭐ | ✓ Alternative |

---

## Dépannage

**Erreur: "VITE_YOUTUBE_API_KEY not configured"**
- Créez `.env` dans `Frontend/`
- Redémarrez `npm run dev`

**Vidéo ne s'affiche pas**
- Vérifiez la clé API YouTube
- Vérifiez les quotas API (100 req/jour gratuit)
- Regardez la console pour erreurs

**Trop lent**
- Cachéz les résultats en BD
- Utilisez Web Workers
- Chargez les vidéos à la demande

---

**Status**: ✅ Prêt à utiliser  
**Recommandation**: Commencez avec Option 1 (lien IMDb), puis ajoutez YouTube API pour meilleure UX
