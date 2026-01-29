# Documentation des Routes API - Movies Recommender Backend

## 🔐 Authentification

### 1. Inscription
**POST** `/api/register`
```json
{
  "email": "user@example.com",
  "password": "password123",
  "name": "John Doe",
  "age": 25,
  "gender": "M",
  "occupation": "engineer"
}
```
**Réponse:** `201 Created`
```json
{
  "message": "Utilisateur créé avec succès",
  "user_id": 1
}
```

### 2. Connexion
**POST** `/api/login`
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```
**Réponse:** `200 OK`
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": "ObjectId",
    "user_id": 1,
    "email": "user@example.com",
    "name": "John Doe",
    "age": 25,
    "gender": "M",
    "occupation": "engineer",
    "cluster_id": 1
  }
}
```

---

## 🎬 Films

### 3. Récupérer films populaires (Public)
**GET** `/api/movies/popular`
**Réponse:** `200 OK`
```json
[
  {
    "movie_id": 1,
    "title": "The Shawshank Redemption",
    "genres": ["Drama"],
    "year": 1994,
    "bayesian_rating": 4.8
  }
]
```

### 4. Récupérer liste des films (Paginations)
**GET** `/api/movies?page=1&limit=20`
**Authentification requise:** Bearer Token
**Réponse:** `200 OK`
```json
[
  {
    "movie_id": 1,
    "title": "The Shawshank Redemption",
    "genres": ["Drama"],
    "year": 1994,
    "bayesian_rating": 4.8
  }
]
```

### 5. Chercher des films
**GET** `/api/movies/search?q=dark`
**Authentification requise:** Bearer Token
**Réponse:** `200 OK`
```json
[
  {
    "movie_id": 3,
    "title": "The Dark Knight",
    "genres": ["Action", "Crime", "Drama"],
    "year": 2008
  }
]
```

### 6. Détails d'un film
**GET** `/api/movies/<movie_id>`
**Authentification requise:** Bearer Token
**Réponse:** `200 OK`
```json
{
  "movie_id": 1,
  "title": "The Shawshank Redemption",
  "year": 1994,
  "genres": ["Drama"],
  "imdb_url": "...",
  "average_rating": 4.5,
  "ratings_count": 100,
  "bayesian_rating": 4.8,
  "user_rating": 5,
  "in_watchlist": true
}
```

### 7. Statistiques de notes d'un film
**GET** `/api/movies/<movie_id>/ratings`
**Réponse:** `200 OK`
```json
{
  "movie_id": 1,
  "title": "The Shawshank Redemption",
  "average_rating": 4.5,
  "ratings_count": 100,
  "bayesian_rating": 4.8,
  "rating_distribution": {
    "1": 5,
    "2": 10,
    "3": 20,
    "4": 35,
    "5": 30
  }
}
```

---

## ⭐ Notations

### 8. Noter un film
**POST** `/api/rate`
**Authentification requise:** Bearer Token
```json
{
  "movie_id": 1,
  "rating": 5
}
```
**Réponse:** `200 OK`
```json
{
  "message": "Évaluation enregistrée",
  "movie_id": 1,
  "rating": 5
}
```

### 9. Récupérer les notes de l'utilisateur
**GET** `/api/user/ratings?page=1&limit=20`
**Authentification requise:** Bearer Token
**Réponse:** `200 OK`
```json
{
  "ratings": [
    {
      "movie_id": 1,
      "rating": 5,
      "timestamp": "2024-01-28T10:30:00",
      "movie_title": "The Shawshank Redemption",
      "movie_year": 1994,
      "movie_genres": ["Drama"]
    }
  ],
  "total": 5,
  "page": 1,
  "limit": 20
}
```

### 10. Supprimer une note
**DELETE** `/api/rate/<movie_id>`
**Authentification requise:** Bearer Token
**Réponse:** `200 OK`
```json
{
  "message": "Note supprimée avec succès"
}
```

---

## 📋 Watchlist

### 11. Récupérer la watchlist
**GET** `/api/watchlist?page=1&limit=20`
**Authentification requise:** Bearer Token
**Réponse:** `200 OK`
```json
{
  "watchlist": [
    {
      "movie_id": 2,
      "title": "The Godfather",
      "genres": ["Crime", "Drama"],
      "year": 1972,
      "bayesian_rating": 4.7,
      "added_at": "2024-01-28T10:30:00"
    }
  ],
  "total": 3,
  "page": 1,
  "limit": 20
}
```

### 12. Ajouter à la watchlist
**POST** `/api/watchlist`
**Authentification requise:** Bearer Token
```json
{
  "movie_id": 2
}
```
**Réponse:** `200 OK`
```json
{
  "message": "Film ajouté à la watchlist",
  "movie_id": 2
}
```

### 13. Supprimer de la watchlist
**DELETE** `/api/watchlist/<movie_id>`
**Authentification requise:** Bearer Token
**Réponse:** `200 OK`
```json
{
  "message": "Film supprimé de la watchlist"
}
```

---

## 👤 Profil Utilisateur

### 14. Récupérer le profil complet
**GET** `/api/user/profile`
**Authentification requise:** Bearer Token
**Réponse:** `200 OK`
```json
{
  "id": "ObjectId",
  "user_id": 1,
  "email": "user@example.com",
  "name": "John Doe",
  "age": 25,
  "gender": "M",
  "occupation": "engineer",
  "cluster_id": 1,
  "created_at": "2024-01-28T10:00:00",
  "ratings_count": 10,
  "preferences": {}
}
```

### 15. Mettre à jour le profil
**PUT** `/api/user/profile`
**Authentification requise:** Bearer Token
```json
{
  "name": "Jane Doe",
  "age": 26,
  "gender": "F",
  "occupation": "developer"
}
```
**Réponse:** `200 OK`
```json
{
  "message": "Profil mis à jour avec succès",
  "updates": {
    "name": "Jane Doe",
    "age": 26
  }
}
```

### 16. Récupérer les statistiques utilisateur
**GET** `/api/user/stats`
**Authentification requise:** Bearer Token
**Réponse:** `200 OK`
```json
{
  "user_id": 1,
  "name": "John Doe",
  "email": "user@example.com",
  "cluster_id": 1,
  "ratings_count": 10,
  "preferences": {}
}
```

### 17. Supprimer le compte
**DELETE** `/api/user/account`
**Authentification requise:** Bearer Token
**Réponse:** `200 OK`
```json
{
  "message": "Compte supprimé avec succès"
}
```

---

## 🤖 Recommandations

### 18. Recommandations pour première connexion
**GET** `/api/recommendations/first-time`
**Authentification requise:** Bearer Token
**Réponse:** `200 OK`
```json
{
  "recommendations": [
    {
      "movie_id": 1,
      "title": "The Shawshank Redemption",
      "score": 0.95,
      "explanation": "Recommandé basé sur votre cluster",
      "score_details": {},
      "genres": ["Drama"],
      "year": 1994
    }
  ],
  "user_type": "new",
  "ratings_count": 0
}
```

### 19. Recommandations personnalisées
**GET** `/api/recommendations/personalized`
**Authentification requise:** Bearer Token
**Réponse:** `200 OK`
```json
{
  "recommendations": [
    {
      "movie_id": 1,
      "title": "The Shawshank Redemption",
      "score": 0.95,
      "explanation": "Recommandé basé sur vos préférences",
      "score_details": {},
      "genres": ["Drama"],
      "year": 1994
    }
  ],
  "user_id": 1
}
```

---

## 🔧 Admin

### 20. Récupérer les statistiques globales
**GET** `/admin/stats`
**Token Admin:** Bearer <ADMIN_TOKEN>
**Réponse:** `200 OK`
```json
{
  "users_count": 50,
  "movies_count": 1000,
  "ratings_count": 500,
  "watchlist_count": 150,
  "top_movies": [
    {
      "movie_id": 1,
      "title": "The Shawshank Redemption",
      "ratings_count": 100,
      "bayesian_rating": 4.8
    }
  ]
}
```

### 21. Exécuter les calculs offline
**POST** `/admin/run-offline`
**Token Admin:** Bearer <ADMIN_TOKEN>
**Réponse:** `200 OK`
```json
{
  "message": "Calculs offline terminés"
}
```

### 22. Initialiser la base de données
**POST** `/admin/init-db`
**Token Admin:** Bearer <ADMIN_TOKEN>
**Réponse:** `200 OK`
```json
{
  "message": "Base de données initialisée avec des données de test",
  "movies_count": 5
}
```

### 23. Réinitialiser la watchlist
**POST** `/admin/reset-watchlist`
**Token Admin:** Bearer <ADMIN_TOKEN>
**Réponse:** `200 OK`
```json
{
  "message": "Watchlist réinitialisée",
  "deleted_count": 10
}
```

---

## ✅ Vérification

### 24. Health Check
**GET** `/api/health`
**Réponse:** `200 OK`
```json
{
  "status": "healthy",
  "timestamp": "2024-01-28T10:00:00"
}
```

---

## 📝 Notes Importantes

- **Authentification:** Toutes les routes sauf `/api/register`, `/api/login`, `/api/health`, `/api/movies/popular` et `/api/movies/<movie_id>/ratings` nécessitent un Bearer Token
- **Admin:** Les routes admin nécessitent un token admin dans le header `Authorization: Bearer <ADMIN_TOKEN>`
- **Pagination:** Utiliser `page` et `limit` pour les routes qui retournent des listes
- **Erreurs:** Les erreurs retournent un JSON avec un message descriptif et un code HTTP approprié

