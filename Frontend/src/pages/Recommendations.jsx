import React, { useEffect, useState, useRef } from 'react'
import client from '../api/client'
import MovieCardWithVideo from '../components/MovieCardWithVideo'
import { Link } from 'react-router-dom'

export default function Recommendation() {
  const [movies, setMovies] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [userType, setUserType] = useState('existing')
  const [lastUpdated, setLastUpdated] = useState(null)
  const [recomputing, setRecomputing] = useState(false)

  const token = localStorage.getItem('access_token')
  const intervalRef = useRef(null)

  useEffect(() => {
    if (!token) {
      setLoading(false)
      return
    }

    const fetchRecs = async () => {
      try {
        const res = await client.get('/recommendations')
        const recs = Array.isArray(res.data.recommendations) ? res.data.recommendations : []
        setMovies(recs)
        setUserType(res.data.user_type || 'existing')
        setLastUpdated(res.data.updated_at || null)
        setRecomputing(!!res.data.recomputing)
      } catch (err) {
        console.error('Impossible de charger les recommandations', err)
        setError('Impossible de charger les recommandations')
      } finally {
        setLoading(false)
      }
    }

    fetchRecs()

    // Rafraîchissement automatique toutes les 10s pour cache serveur
    intervalRef.current = setInterval(fetchRecs, 10000)
    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current)
    }
  }, [token])

  if (!token) {
    return (
      <div className="min-h-screen bg-black text-white flex items-center justify-center">
        <div className="text-center max-w-md">
          <h1 className="text-3xl font-black mb-4">🎯 Recommandations personnalisées</h1>
          <p className="text-gray-400 mb-6">
            Connectez-vous pour recevoir des films adaptés à vos goûts.
          </p>
          <Link
            to="/login"
            className="px-6 py-3 bg-gradient-to-r from-yellow-400 to-pink-500 text-black font-bold rounded-lg"
          >
            Se connecter
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-black text-white">
      <div className="max-w-7xl mx-auto px-4 py-12">

        <h1 className="text-4xl font-black bg-gradient-to-r from-purple-400 to-pink-500 bg-clip-text text-transparent mb-2">
          {userType === 'new' ? '✨ Suggestions pour commencer' : '🤖 Recommandations pour vous'}
        </h1>
        <p className="text-gray-400 mb-4">
          Basées sur vos préférences, vos interactions et des similarités utilisateurs
        </p>

        <div className="flex items-center justify-between mb-6 text-sm text-gray-400">
          {recomputing ? 'Recalcul en cours…' : lastUpdated ? `Mis à jour: ${new Date(lastUpdated).toLocaleString()}` : ''}
        </div>

        {loading && (
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
            {[...Array(12)].map((_, i) => (
              <div key={i} className="bg-gray-800 rounded-xl h-80 animate-pulse" />
            ))}
          </div>
        )}

        {!loading && error && (
          <div className="text-center text-red-400 py-12">{error}</div>
        )}

        {!loading && !error && movies.length > 0 && (
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
            {movies.map(movie => (
              <MovieCardWithVideo key={movie.movie_id} m={movie} />
            ))}
          </div>
        )}

        {!loading && !error && movies.length === 0 && (
          <div className="text-center py-16 text-gray-400">
            <p className="text-lg mb-2">Aucune recommandation disponible</p>
            <p className="text-sm">Interagissez avec des films pour améliorer les suggestions</p>
          </div>
        )}

      </div>
    </div>
  )
}
