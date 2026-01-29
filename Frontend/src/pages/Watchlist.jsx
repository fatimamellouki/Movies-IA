import React, {useEffect, useState} from 'react'
import client from '../api/client'
import { useNavigate, Link } from 'react-router-dom'

function MovieCard({m, onRemove}){
  return (
    <div className="group relative bg-gradient-to-br from-gray-900 to-gray-800 rounded-xl overflow-hidden shadow-xl hover:shadow-2xl transition-all duration-300">
      <Link to={`/movies/${m.movie_id}`} className="block relative h-48 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-t from-black via-transparent to-transparent"></div>
        <div className="absolute inset-0 group-hover:bg-black/20 transition-colors"></div>
      </Link>
      <div className="p-4">
        <Link to={`/movies/${m.movie_id}`} className="block">
          <h3 className="font-bold text-white group-hover:text-yellow-400 transition-colors line-clamp-2 mb-2">{m.title}</h3>
        </Link>
        <p className="text-xs text-gray-400 mb-3">{m.year} • {m.genres?.slice(0,2).join(', ')}</p>
        <button
          onClick={()=> onRemove(m.movie_id)}
          className="w-full px-3 py-2 bg-red-600 hover:bg-red-700 text-white font-bold rounded-lg transition-all text-sm"
        >
          ✕ Supprimer
        </button>
      </div>
    </div>
  )
}

export default function Watchlist(){
  const [watchlist, setWatchlist] = useState([])
  const [page, setPage] = useState(1)
  const [total, setTotal] = useState(0)
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  const token = localStorage.getItem('access_token')

  useEffect(()=>{
    if(!token) return navigate('/login')
    setLoading(true)
    client.get(`/watchlist?page=${page}&limit=20`)
      .then(r=> {
        setWatchlist(r.data.watchlist || [])
        setTotal(r.data.total || 0)
      })
      .catch(()=> {})
      .finally(()=> setLoading(false))
  },[page, token, navigate])

  async function removeFromWatchlist(movieId){
    try{
      await client.delete(`/watchlist/${movieId}`)
      setWatchlist(prev=> prev.filter(m=> m.movie_id !== movieId))
    }catch(err){
      alert('Erreur lors de la suppression')
    }
  }

  return (
    <div className="min-h-screen bg-black text-white">
      <div className="max-w-7xl mx-auto px-4 py-12">
        <h1 className="text-4xl font-black bg-gradient-to-r from-purple-400 to-pink-500 bg-clip-text text-transparent mb-2">📋 Ma Watchlist</h1>
        <p className="text-gray-400 mb-8">Films à regarder ({total})</p>

        {loading && (
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
            {[...Array(12)].map((_, i)=> <div key={i} className="bg-gray-800 rounded-xl h-64 animate-pulse"></div>)}
          </div>
        )}

        {!loading && watchlist.length === 0 && (
          <div className="text-center py-12">
            <p className="text-gray-400 text-lg mb-4">Votre watchlist est vide</p>
            <Link to="/movies" className="text-yellow-400 hover:text-yellow-300 font-bold">
              Découvrir des films →
            </Link>
          </div>
        )}

        {!loading && watchlist.length > 0 && (
          <>
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 mb-12">
              {watchlist.map(m=> <MovieCard key={m.movie_id} m={m} onRemove={removeFromWatchlist} />)}
            </div>

            <div className="flex justify-between items-center pt-8 border-t border-gray-700">
              <button
                onClick={()=> setPage(p=> Math.max(1, p-1))}
                disabled={page === 1}
                className="px-6 py-2 bg-gradient-to-r from-purple-600 to-indigo-600 text-white font-bold rounded-lg hover:shadow-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed"
              >
                ← Précédent
              </button>
              <span className="text-lg font-bold text-yellow-400">Page {page}</span>
              <button
                onClick={()=> setPage(p=> p+1)}
                disabled={page * 20 >= total}
                className="px-6 py-2 bg-gradient-to-r from-yellow-500 to-orange-500 text-black font-bold rounded-lg hover:shadow-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Suivant →
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  )
}
