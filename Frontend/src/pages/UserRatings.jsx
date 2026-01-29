import React, {useEffect, useState} from 'react'
import client from '../api/client'
import { useNavigate, Link } from 'react-router-dom'

function RatingCard({r, onDelete}){
  return (
    <div className="bg-gradient-to-r from-gray-900 to-gray-800 p-6 rounded-xl border border-gray-700 hover:border-yellow-500/50 transition-all shadow-xl">
      <div className="flex items-center justify-between mb-4">
        <Link to={`/movies/${r.movie_id}`} className="flex-1">
          <h3 className="font-bold text-white text-lg hover:text-yellow-400 transition-colors">{r.movie_title}</h3>
        </Link>
        <div className="text-right">
          <div className="text-4xl font-black text-yellow-400">{r.rating}</div>
          <p className="text-xs text-gray-400">/ 5</p>
        </div>
      </div>
      <p className="text-gray-400 text-sm mb-4">{r.movie_year} • {r.movie_genres?.slice(0, 3).join(', ')}</p>
      <button
        onClick={()=> onDelete(r.movie_id)}
        className="w-full px-4 py-2 bg-red-600 hover:bg-red-700 text-white font-bold rounded-lg transition-all text-sm"
      >
        ✕ Supprimer l'évaluation
      </button>
    </div>
  )
}

export default function UserRatings(){
  const [ratings, setRatings] = useState([])
  const [page, setPage] = useState(1)
  const [total, setTotal] = useState(0)
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  const token = localStorage.getItem('access_token')

  useEffect(()=>{
    if(!token) return navigate('/login')
    setLoading(true)
    client.get(`/user/ratings?page=${page}&limit=20`)
      .then(r=> {
        setRatings(r.data.ratings || [])
        setTotal(r.data.total || 0)
      })
      .catch(()=> {})
      .finally(()=> setLoading(false))
  },[page, token, navigate])

  async function deleteRating(movieId){
    try{
      await client.delete(`/rate/${movieId}`)
      setRatings(prev=> prev.filter(r=> r.movie_id !== movieId))
    }catch(err){
      alert('Erreur lors de la suppression')
    }
  }

  return (
    <div className="min-h-screen bg-black text-white">
      <div className="max-w-7xl mx-auto px-4 py-12">
        <h1 className="text-4xl font-black bg-gradient-to-r from-yellow-400 to-orange-500 bg-clip-text text-transparent mb-2">⭐ Mes Évaluations</h1>
        <p className="text-gray-400 mb-8">Films que vous avez notés ({total})</p>

        {loading && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[...Array(6)].map((_, i)=> <div key={i} className="bg-gray-800 rounded-xl h-40 animate-pulse"></div>)}
          </div>
        )}

        {!loading && ratings.length === 0 && (
          <div className="text-center py-12">
            <p className="text-gray-400 text-lg mb-4">Vous n'avez pas encore noté de films</p>
            <Link to="/movies" className="text-yellow-400 hover:text-yellow-300 font-bold">
              Découvrir et noter des films →
            </Link>
          </div>
        )}

        {!loading && ratings.length > 0 && (
          <>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
              {ratings.map(r=> <RatingCard key={r.movie_id} r={r} onDelete={deleteRating} />)}
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
