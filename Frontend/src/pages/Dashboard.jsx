import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import client from '../api/client'
import MovieCardWithVideo from '../components/MovieCardWithVideo'

export default function Dashboard() {
  const [recommendations, setRecommendations] = useState([])
  const [popular, setPopular] = useState([])
  const [discover, setDiscover] = useState([])

  const [loadingRecs, setLoadingRecs] = useState(true)
  const [loadingPop, setLoadingPop] = useState(true)
  const [loadingDisc, setLoadingDisc] = useState(true)

  const [userType, setUserType] = useState('existing')
  const [ratingsCount, setRatingsCount] = useState(0)

  // Fonction pour récupérer recommandations depuis backend
  const fetchRecommendations = async () => {
    try {
      const res = await client.get('/recommendations')
      setRecommendations(res.data?.recommendations || [])
      setUserType(res.data?.user_type || 'existing')
      setRatingsCount(res.data?.ratings_count || 0)
    } catch (err) {
      setRecommendations([])
    } finally {
      setLoadingRecs(false)
    }
  }

  useEffect(() => {
    // 🎯 Recommandations
    fetchRecommendations()

    // 🔥 Films populaires
    client.get('/movies/popular')
      .then(r => setPopular(r.data || []))
      .catch(() => setPopular([]))
      .finally(() => setLoadingPop(false))

    // 🎬 Découvrir
    client.get('/movies?page=1&limit=20')
      .then(r => setDiscover(r.data?.data || []))
      .catch(() => setDiscover([]))
      .finally(() => setLoadingDisc(false))

    // 🔄 Polling léger pour vérifier si cache recommandations a été mis à jour
    const interval = setInterval(fetchRecommendations, 10000)
    return () => clearInterval(interval)
  }, [])

  const MovieSkeleton = () => (
    <div className="bg-gray-800 rounded-xl h-64 animate-pulse"></div>
  )

  return (
    <div className="min-h-screen bg-black text-white">
      <div className="max-w-7xl mx-auto px-4 py-8">

        {/* ===================== */}
        {/* Recommandations */}
        {/* ===================== */}
        <section className="mb-16">
          <div className="flex items-center justify-between mb-8">
            <h2 className="text-3xl font-black bg-gradient-to-r from-purple-400 to-pink-500 bg-clip-text text-transparent flex items-center gap-2">
              {userType === 'new' ? '✨ Suggestions pour commencer' : '✨ Pour Vous'}
            </h2>
            <Link
              to="/recommendations"
              className="text-yellow-400 hover:text-yellow-300 font-bold"
            >
              Plus →
            </Link>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
            {loadingRecs &&
              [...Array(4)].map((_, i) => <MovieSkeleton key={i} />)
            }

            {!loadingRecs && recommendations.length > 0 &&
              recommendations.slice(0, 8).map(m => (
                <MovieCardWithVideo key={m.movie_id} m={m} />
              ))
            }

            {!loadingRecs && recommendations.length === 0 && (
              <div className="col-span-full text-center py-12 text-gray-400">
                <p className="mb-4">Aucune recommandation disponible</p>
                <Link
                  to="/user-ratings"
                  className="text-yellow-400 hover:text-yellow-300"
                >
                  Allez noter des films →
                </Link>
              </div>
            )}
          </div>
        </section>

        {/* ===================== */}
        {/* Films populaires */}
        {/* ===================== */}
        <section className="mb-16">
          <div className="flex items-center justify-between mb-8">
            <h2 className="text-3xl font-black bg-gradient-to-r from-yellow-400 to-orange-500 bg-clip-text text-transparent flex items-center gap-2">
              🔥 Tendances
            </h2>
            <Link
              to="/movies"
              className="text-yellow-400 hover:text-yellow-300 font-bold"
            >
              Plus →
            </Link>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
            {loadingPop &&
              [...Array(4)].map((_, i) => <MovieSkeleton key={i} />)
            }

            {!loadingPop &&
              popular.slice(0, 8).map(m => (
                <MovieCardWithVideo key={m.movie_id} m={m} />
              ))
            }
          </div>
        </section>

        {/* ===================== */}
        {/* Découvrir */}
        {/* ===================== */}
        <section className="mb-16">
          <div className="flex items-center justify-between mb-8">
            <h2 className="text-3xl font-black bg-gradient-to-r from-indigo-400 to-blue-500 bg-clip-text text-transparent flex items-center gap-2">
              🎬 Découvrir
            </h2>
            <Link
              to="/movies"
              className="text-yellow-400 hover:text-yellow-300 font-bold"
            >
              Tous →
            </Link>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
            {loadingDisc &&
              [...Array(4)].map((_, i) => <MovieSkeleton key={i} />)
            }

            {!loadingDisc &&
              discover.slice(0, 8).map(m => (
                <MovieCardWithVideo key={m.movie_id} m={m} />
              ))
            }
          </div>
        </section>

        {/* ===================== */}
        {/* Actions rapides */}
        {/* ===================== */}
        <section className="bg-gradient-to-r from-gray-900 to-gray-800 rounded-2xl p-8 border border-purple-500/20">
          <h3 className="text-2xl font-bold text-white mb-6">
            Actions rapides
          </h3>

          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
            <Link
              to="/watchlist"
              className="bg-gradient-to-r from-indigo-600 to-purple-600 p-6 rounded-xl hover:shadow-lg transition-all transform hover:scale-105 text-center"
            >
              <div className="text-3xl mb-2">📋</div>
              <h4 className="font-bold">Ma Watchlist</h4>
              <p className="text-sm text-gray-300">Films à regarder</p>
            </Link>

            <Link
              to="/user-ratings"
              className="bg-gradient-to-r from-yellow-600 to-orange-600 p-6 rounded-xl hover:shadow-lg transition-all transform hover:scale-105 text-center"
            >
              <div className="text-3xl mb-2">⭐</div>
              <h4 className="font-bold">Mes Évaluations</h4>
              <p className="text-sm text-gray-300">Films notés</p>
            </Link>

            <Link
              to="/profile"
              className="bg-gradient-to-r from-pink-600 to-red-600 p-6 rounded-xl hover:shadow-lg transition-all transform hover:scale-105 text-center"
            >
              <div className="text-3xl mb-2">👤</div>
              <h4 className="font-bold">Mon Profil</h4>
              <p className="text-sm text-gray-300">Paramètres</p>
            </Link>
          </div>
        </section>

      </div>
    </div>
  )
}
