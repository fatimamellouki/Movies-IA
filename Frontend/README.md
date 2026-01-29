# Frontend (React + Vite + Tailwind CSS)

Application React moderne consommant l'API Movie Recommender.

## Fonctionnalités

- **Accueil**: Films populaires et aperçu des recommandations
- **Authentification**: Inscription et connexion
- **Catalogue**: Liste de tous les films avec pagination
- **Détails**: Info complète d'un film, notation, ajout à la watchlist
- **Recommandations**: Suggestions personnalisées basées sur le profil utilisateur
- **Profil**: Affichage et édition du profil utilisateur
- **Mes notes**: Historique des films notés
- **Ma liste**: Watchlist personnalisée
- **Recherche**: Recherche par titre de film

## Prérequis

- Node.js 18+
- Backend API en cours d'exécution (port 5000)

## Installation et lancement

```bash
cd Frontend
npm install
npm run dev
```

L'app sera accessible sur **http://localhost:5173**.

## Configuration

Par défaut, le frontend accède à `http://localhost:5000/api`.
Pour personnaliser, créez un fichier `.env` à la racine de `Frontend`:

```env
VITE_API_BASE=http://localhost:5000/api
```

## Structure des fichiers

```
Frontend/
├── src/
│   ├── api/
│   │   └── client.js           # Client Axios + gestion du token
│   ├── pages/
│   │   ├── Home.jsx            # Page d'accueil
│   │   ├── Login.jsx           # Connexion
│   │   ├── Register.jsx        # Inscription
│   │   ├── Movies.jsx          # Liste des films
│   │   ├── MovieDetail.jsx     # Détails + rating + watchlist
│   │   ├── Recommendations.jsx # Recommandations personnalisées
│   │   ├── Profile.jsx         # Profil utilisateur
│   │   ├── UserRatings.jsx     # Mes notes
│   │   ├── Watchlist.jsx       # Ma liste de suivi
│   │   └── Search.jsx          # Recherche
│   ├── App.jsx                 # Routeur principal
│   ├── index.css               # Styles Tailwind
│   └── main.jsx                # Point d'entrée
├── index.html
├── vite.config.js
├── tailwind.config.cjs
├── postcss.config.cjs
└── package.json
```

## Design

- **Tailwind CSS** pour un style professionnel et responsive
- Couleurs: Indigo/Purple gradient pour le header
- Composants réutilisables et flexibles

## Routes disponibles

| Route | Description |
|-------|-------------|
| `/` | Accueil |
| `/login` | Connexion |
| `/register` | Inscription |
| `/movies` | Catalogue complet |
| `/movies/:id` | Détails d'un film |
| `/recommendations` | Recommandations personnalisées |
| `/search` | Recherche |
| `/profile` | Mon profil |
| `/ratings` | Mes notes |
| `/watchlist` | Ma liste de suivi |

## API utilisée

- POST `/api/register` - Créer un compte
- POST `/api/login` - Se connecter
- GET `/api/movies/popular` - Films populaires
- GET `/api/movies` - Liste pagée des films
- GET `/api/movies/search` - Rechercher des films
- GET `/api/movies/:id` - Détails d'un film
- GET `/api/movies/:id/ratings` - Stats des notes
- POST `/api/rate` - Noter un film
- DELETE `/api/rate/:id` - Supprimer une note
- GET `/api/user/profile` - Mon profil
- PUT `/api/user/profile` - Éditer le profil
- DELETE `/api/user/account` - Supprimer le compte
- GET `/api/user/ratings` - Mes notes
- GET `/api/recommendations/first-time` - Recommandations
- GET `/api/watchlist` - Ma liste
- POST `/api/watchlist` - Ajouter à la liste
- DELETE `/api/watchlist/:id` - Retirer de la liste

