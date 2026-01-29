# 🚀 MovieRecs Frontend - Quick Start Guide

## Prerequisites

- Node.js (v16+)
- npm or yarn
- Backend API running on `http://localhost:5000`

## Installation & Setup

### 1. Install Dependencies

```bash
cd Frontend
npm install
```

### 2. Start Development Server

```bash
npm run dev
```

The app will start on: **http://localhost:5173**

## Project Structure

```
Frontend/
├── src/
│   ├── api/
│   │   └── client.js                 # Axios HTTP client with JWT
│   ├── contexts/
│   │   └── AuthContext.jsx           # Authentication state management
│   ├── pages/
│   │   ├── Home.jsx                  # Landing page
│   │   ├── Login.jsx                 # Login form
│   │   ├── Register.jsx              # Registration with occupations
│   │   ├── Dashboard.jsx             # Main authenticated page
│   │   ├── Movies.jsx                # Movie catalog
│   │   ├── MovieDetail.jsx           # Film details + rating
│   │   ├── Search.jsx                # Search functionality
│   │   ├── Recommendations.jsx       # Personalized recommendations
│   │   ├── Watchlist.jsx             # User's watchlist
│   │   ├── UserRatings.jsx           # User's rated movies
│   │   └── Profile.jsx               # User profile
│   ├── App.jsx                       # Main router component
│   ├── main.jsx                      # React entry point
│   └── index.css                     # Tailwind imports
├── public/
│   └── index.html                    # HTML template
├── package.json                      # Dependencies & scripts
├── vite.config.js                    # Vite configuration
├── tailwind.config.cjs               # Tailwind configuration
├── postcss.config.cjs                # PostCSS configuration
└── README.md                         # Original docs
```

## Available Pages

| Path | Page | Auth Required | Description |
|------|------|---|---|
| `/` | Home | ❌ | Landing page with hero & popular films |
| `/login` | Login | ❌ | Authentication form |
| `/register` | Register | ❌ | Account creation |
| `/dashboard` | Dashboard | ✅ | Main authenticated page |
| `/movies` | Movies | ❌ | Movie catalog with pagination |
| `/movies/:id` | MovieDetail | ❌ | Film details & rating |
| `/search` | Search | ✅ | Search movies by title |
| `/recommendations` | Recommendations | ✅ | Personalized picks |
| `/watchlist` | Watchlist | ✅ | User's watchlist |
| `/user-ratings` | UserRatings | ✅ | User's rated movies |
| `/profile` | Profile | ✅ | User profile & settings |

## Features

### 🎨 UI/UX
- Cinema-themed design with gradients and animations
- Responsive grid layouts (mobile to desktop)
- Loading skeletons for better UX
- Error handling with user-friendly messages

### 🔐 Authentication
- JWT token management with localStorage
- Automatic Bearer token in all API requests
- Protected routes requiring login
- Auto-redirect to dashboard on login

### 🎬 Movie Management
- Browse all movies with pagination
- Search movies by title
- Rate movies (1-5 stars)
- Add/remove from watchlist
- View personalized recommendations

### 👤 User Management
- Register with 20 occupation options
- View/edit user profile
- Delete account (irreversible)
- Track rated movies and watchlist

## API Integration

The frontend communicates with backend at: `http://localhost:5000/api`

**Key Endpoints Used:**
- `GET /movies/popular` - Popular films
- `POST /login` - User authentication
- `POST /register` - Account creation
- `GET /movies` - Catalog (paginated)
- `GET /movies/search` - Search
- `GET /movies/:id` - Film details
- `POST /rate` - Submit rating
- `GET /user/ratings` - User's ratings
- `POST /watchlist` - Add to watchlist
- `GET /recommendations/first-time` - Personalized picks

## Development Commands

```bash
# Start dev server with hot reload
npm run dev

# Build for production
npm run build

# Preview production build locally
npm run preview

# Lint with ESLint (if configured)
npm run lint
```

## Configuration

### Environment Variables

Create a `.env` file in the `Frontend/` directory (optional):

```env
VITE_API_BASE=http://localhost:5000/api
```

Default is already set in `src/api/client.js`.

### Customization

**Change API Base URL:**
Edit `src/api/client.js`:
```javascript
const baseURL = import.meta.env.VITE_API_BASE || 'http://localhost:5000/api'
```

**Modify Tailwind Theme:**
Edit `tailwind.config.cjs` to customize colors, fonts, spacing, etc.

## Troubleshooting

### Port 5173 Already in Use
```bash
npm run dev -- --port 3000
```

### 401 Unauthorized Errors
- Token may have expired (24-hour TTL)
- Solution: Re-login via `/login`
- Check localStorage has `access_token` key

### CORS Errors
- Ensure backend is running on `http://localhost:5000`
- Check backend has CORS enabled
- Verify API endpoints match documentation

### Movies Not Loading
- Ensure backend database is populated (`python init_db.py`)
- Check `/api/movies/popular` returns data
- Verify API is running without errors

## Performance Tips

- Lazy-load pages using React Router code splitting
- Optimize images/assets
- Use browser DevTools to profile
- Check Network tab for slow API calls

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers (iOS Safari, Chrome Mobile)

## Deployment

### Build for Production

```bash
npm run build
```

Creates optimized build in `dist/` folder.

### Deploy to Hosting

**Vercel:**
```bash
npm install -g vercel
vercel
```

**Netlify:**
```bash
npm install -g netlify-cli
netlify deploy --prod --dir=dist
```

**Docker:**
```dockerfile
FROM node:16-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:16-alpine
RUN npm install -g serve
WORKDIR /app
COPY --from=build /app/dist ./dist
EXPOSE 3000
CMD ["serve", "-s", "dist", "-l", "3000"]
```

## Support & Documentation

- **Styling Guide**: See `STYLING_GUIDE.md`
- **Redesign Summary**: See `REDESIGN_SUMMARY.md`
- **API Docs**: Check backend `API_ROUTES.md`
- **Issue Tracking**: Use GitHub Issues

---

**Last Updated**: 2024  
**Status**: Production Ready ✅
