import React, {useEffect, useState} from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import client from '../api/client'
import VideoPlayer from '../components/VideoPlayer'

export default function MovieDetail(){
  const {id} = useParams()
  const [movie, setMovie] = useState(null)
  const [stats, setStats] = useState(null)
  const [userRating, setUserRating] = useState(null)
  const [inWatchlist, setInWatchlist] = useState(false)
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  const token = localStorage.getItem('access_token')

  useEffect(()=>{
    setLoading(true)
    async function load(){
      try{
        if(token){
          const r = await client.get(`/movies/${id}`)
          setMovie(r.data)
          setUserRating(r.data.user_rating)
          setInWatchlist(r.data.in_watchlist)
          // also try to fetch stats (public)
          try{ const s = await client.get(`/movies/${id}/ratings`); setStats(s.data) }catch(e){}
        } else {
          // No token: movie details endpoint is protected. Fetch public ratings endpoint for minimal info.
          const r = await client.get(`/movies/${id}/ratings`)
          setMovie({ title: r.data.title })
          setStats(r.data)
        }
      }catch(err){
        // If unauthorized, try to fetch public ratings as fallback
        if(err?.response?.status === 401){
          try{
            const r = await client.get(`/movies/${id}/ratings`)
            setMovie({ title: r.data.title })
            setStats(r.data)
          }catch(e){
            setMovie(null)
          }
        }else{
          setMovie(null)
        }
      }finally{
        setLoading(false)
      }
    }

    load()
  },[id, token])

  async function submitRating(rating){
    if(!token) return navigate('/login')
    try{
      await client.post('/rate', {movie_id: parseInt(id), rating: parseFloat(rating)})
      setUserRating(parseFloat(rating))
    }catch(err){
      alert('Erreur lors de la note')
    }
  }

  async function deleteRating(){
    try{
      await client.delete(`/rate/${id}`)
      setUserRating(null)
    }catch(err){
      alert('Erreur')
    }
  }

  async function toggleWatchlist(){
    if(!token) return navigate('/login')
    try{
      if(inWatchlist){
        await client.delete(`/watchlist/${id}`)
        setInWatchlist(false)
      }else{
        await client.post('/watchlist', {movie_id: parseInt(id)})
        setInWatchlist(true)
      }
    }catch(err){
      alert('Erreur')
    }
  }

  if(loading) return (
    <div className="min-h-screen bg-black flex items-center justify-center">
      <div className="text-yellow-400 text-2xl font-bold animate-pulse">Chargement…</div>
    </div>
  )
  if(!movie) return (
    <div className="min-h-screen bg-black text-gray-400 flex items-center justify-center">
      <div className="text-center">
        <p className="text-2xl font-bold mb-4">Film non trouvé</p>
        <button onClick={()=> navigate('/movies')} className="text-yellow-400 hover:text-yellow-300">
          ← Retour aux films
        </button>
      </div>
    </div>
  )

  return (
    <div className="min-h-screen bg-black text-white">
      <div className="max-w-4xl mx-auto px-4 py-12">
        {/* Header */}
        <button onClick={()=> navigate('/movies')} className="text-yellow-400 hover:text-yellow-300 font-bold mb-6">
          ← Retour
        </button>

        {/* Main Content */}
        <div className="bg-gradient-to-br from-gray-900 to-gray-800 rounded-2xl p-8 border border-purple-500/20 shadow-2xl">
          <h1 className="text-5xl font-black text-white mb-2">{movie.title}</h1>
          <div className="flex items-center gap-4 text-gray-400 mb-6">
            <span className="text-lg font-bold text-yellow-400">{movie.year}</span>
            <span>•</span>
            <span>{movie.genres?.slice(0, 3).join(', ')}</span>
          </div>

          {/* Video Player */}
          <div className="mb-8">
            <VideoPlayer 
              movieTitle={movie.title}
              movieYear={movie.year}
              imdbUrl={movie.imdb_url}
            />
          </div>
          {stats && (
            <div className="bg-gradient-to-r from-yellow-600 to-orange-600 rounded-xl p-6 mb-8">
              <div className="grid grid-cols-2 gap-6">
                <div>
                  <p className="text-white/80 text-sm">Note moyenne</p>
                  <p className="text-4xl font-black text-white">{stats.average_rating?.toFixed(2) || '?'}/5</p>
                </div>
                <div>
                  <p className="text-white/80 text-sm">Évaluations</p>
                  <p className="text-4xl font-black text-white">{stats.ratings_count || 0}</p>
                </div>
              </div>
            </div>
          )}

          {/* Description */}
          <div className="mb-8">
            <h3 className="text-2xl font-bold text-yellow-400 mb-3">Synopsis</h3>
            <p className="text-gray-300 leading-relaxed text-lg">
              {movie.overview || 'Aucune description disponible.'}
            </p>
          </div>

          {/* User Actions */}
          {token && (
            <div className="border-t border-gray-700 pt-8 space-y-6">
              {/* Rating Section */}
              <div>
                <h3 className="text-2xl font-bold text-yellow-400 mb-4">Votre évaluation</h3>
                {userRating ? (
                  <div className="flex items-center gap-4">
                    <div className="bg-gradient-to-r from-yellow-500 to-orange-500 px-6 py-4 rounded-lg">
                      <p className="text-5xl font-black text-black">{userRating}⭐</p>
                    </div>
                    <button
                      onClick={deleteRating}
                      className="px-6 py-3 bg-red-600 text-white rounded-lg hover:bg-red-700 font-bold transition-all"
                    >
                      Supprimer ma note
                    </button>
                  </div>
                ) : (
                  <div className="flex gap-2 flex-wrap">
                    {[1,2,3,4,5].map(r=> (
                      <button
                        key={r}
                        onClick={()=> submitRating(r)}
                        className="w-16 h-16 bg-gradient-to-r from-gray-700 to-gray-800 border border-gray-600 rounded-lg hover:from-yellow-600 hover:to-orange-600 hover:border-yellow-400 text-white text-2xl font-black transition-all transform hover:scale-110"
                      >
                        {r}
                      </button>
                    ))}
                  </div>
                )}
              </div>

              {/* Watchlist Button */}
              <button
                onClick={toggleWatchlist}
                className={`w-full py-4 rounded-lg font-bold text-lg transition-all transform hover:scale-105 ${
                  inWatchlist
                    ? 'bg-gradient-to-r from-red-600 to-pink-600 hover:shadow-lg hover:shadow-red-500/50'
                    : 'bg-gradient-to-r from-purple-600 to-indigo-600 hover:shadow-lg hover:shadow-purple-500/50'
                }`}
              >
                {inWatchlist ? '✓ Dans ma watchlist' : '+ Ajouter à ma watchlist'}
              </button>
            </div>
          )}

          {/* Login CTA */}
          {!token && (
            <div className="border-t border-gray-700 pt-8 text-center">
              <p className="text-gray-400 mb-4">Connectez-vous pour noter ce film et ajouter à votre liste</p>
              <button 
                onClick={()=> navigate('/login')}
                className="px-8 py-3 bg-gradient-to-r from-yellow-500 to-orange-500 text-black font-bold rounded-lg hover:shadow-lg transition-all"
              >
                Se connecter
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
