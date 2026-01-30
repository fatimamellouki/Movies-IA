import React, { useState } from 'react'
import { Routes, Route, Link, useNavigate } from 'react-router-dom'
import Home from './pages/Home'
import Login from './pages/Login'
import Register from './pages/Register'
import SelectGenres from './pages/SelectGenres';
import Movies from './pages/Movies'
import MovieDetail from './pages/MovieDetail'
import Dashboard from './pages/Dashboard'
import Recommendations from './pages/Recommendations'
import Profile from './pages/Profile'
import UserRatings from './pages/UserRatings'
import Watchlist from './pages/Watchlist'
import Search from './pages/Search'
import { AuthProvider, useAuth } from './contexts/AuthContext'

function Header(){
  const navigate = useNavigate()
  const { token, logout } = useAuth()
  const [searchQuery, setSearchQuery] = useState('')

  function handleSearch(e){
    e.preventDefault()
    if(searchQuery.trim()){
      navigate(`/search?q=${encodeURIComponent(searchQuery)}`)
      setSearchQuery('')
    }
  }

  return (
    <header className="bg-gradient-to-r from-gray-900 via-purple-900 to-black text-white shadow-2xl border-b border-purple-500/20">
      <div className="max-w-7xl mx-auto flex items-center justify-between p-4 gap-4">
        <Link to={token ? "/dashboard" : "/"} className="text-3xl font-black bg-gradient-to-r from-yellow-400 to-pink-500 bg-clip-text text-transparent flex-shrink-0">🎬 MovieRecs</Link>
        
        {/* Search Bar - Center */}
        {token && (
          <form onSubmit={handleSearch} className="flex-1 max-w-sm">
            <div className="relative">
              <input
                type="text"
                value={searchQuery}
                onChange={(e)=> setSearchQuery(e.target.value)}
                placeholder="Rechercher un film..."
                className="w-full px-4 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:border-yellow-500 focus:outline-none transition-colors"
              />
              <button type="submit" className="absolute right-3 top-2.5 text-yellow-400">🔍</button>
            </div>
          </form>
        )}

        {/* Navigation */}
        <nav className="flex gap-4 items-center flex-wrap justify-center">
          <Link to="/movies" className="hover:text-yellow-400 font-semibold transition-colors">Films</Link>
          {token && <Link to="/dashboard" className="hover:text-yellow-400 font-semibold transition-colors">Tableau de bord</Link>}
          {token && <Link to="/watchlist" className="hover:text-yellow-400 font-semibold transition-colors">📋 Liste</Link>}
          {token && <Link to="/user-ratings" className="hover:text-yellow-400 font-semibold transition-colors">⭐ Notes</Link>}
        </nav>

        {/* Auth Buttons */}
        <div className="flex gap-2 items-center flex-shrink-0">
          {!token && (
            <>
              <Link to="/login" className="px-4 py-2 hover:text-yellow-400 font-bold transition-colors">Connexion</Link>
              <Link to="/register" className="px-4 py-2 bg-gradient-to-r from-yellow-500 to-orange-500 text-black font-bold rounded-lg hover:shadow-lg transition-all">Inscription</Link>
            </>
          )}
          {token && (
            <>
              <Link to="/profile" className="px-4 py-2 hover:text-yellow-400 font-bold transition-colors">👤 Profil</Link>
              <button onClick={()=> {logout(); navigate('/')}} className="px-4 py-2 bg-red-600 text-white font-bold rounded-lg hover:bg-red-700 transition-all">Déconnexion</button>
            </>
          )}
        </div>
      </div>
    </header>
  )
}

function AppRoutes(){
  return (
    <div className="min-h-screen flex flex-col bg-black">
      <Header />
      <main className="flex-1 w-full">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/select-genres" element={<SelectGenres />} />
          <Route path="/search" element={<Search />} />
          <Route path="/movies" element={<Movies />} />
          <Route path="/movies/:id" element={<MovieDetail />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/recommendations" element={<Recommendations />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/user-ratings" element={<UserRatings />} />
          <Route path="/watchlist" element={<Watchlist />} />
        </Routes>
      </main>
      <footer className="bg-gray-900 border-t border-gray-700 p-4 text-center text-sm text-gray-400">
        © 2026 MovieRecs - Découvrez vos films préférés
      </footer>
    </div>
  )
}

export default function App(){
  return (
    <AuthProvider>
      <AppRoutes />
    </AuthProvider>
  )
}

