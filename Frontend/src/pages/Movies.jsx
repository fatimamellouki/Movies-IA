import React, {useEffect, useState} from 'react'
import client from '../api/client'
import { Link } from 'react-router-dom'
import MovieCardWithVideo from '../components/MovieCardWithVideo'

export default function Movies(){
  const [movies, setMovies] = useState([])
  const [page, setPage] = useState(1)
  const [loading, setLoading] = useState(true)

  useEffect(()=>{
    setLoading(true)
    const token = localStorage.getItem('access_token')
    // Use protected endpoint if token exists
    const url = token ? `/movies?page=${page}&limit=20` : '/movies/popular'
    client.get(url)
      .then(r=> {
        const data = r.data
        if(Array.isArray(data)) setMovies(data)
        else if(data.data) setMovies(data.data)
        else setMovies([])
      })
      .catch(()=> setMovies([]))
      .finally(()=> setLoading(false))
  },[page])

  return (
    <div className="min-h-screen bg-black text-white">
      <div className="max-w-7xl mx-auto px-4 py-12">
        <h1 className="text-4xl font-black bg-gradient-to-r from-yellow-400 to-pink-500 bg-clip-text text-transparent mb-2">🎬 Catalogue Films</h1>
        <p className="text-gray-400 mb-8">Découvrez notre vaste collection de films</p>

        {loading && (
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 mb-8">
            {[...Array(12)].map((_, i)=> <div key={i} className="bg-gray-800 rounded-xl h-80 animate-pulse"></div>)}
          </div>
        )}

        {!loading && (
          <>
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 mb-12">
              {movies.map(m=> <MovieCardWithVideo key={m.movie_id} m={m} />)}
            </div>

            {movies.length === 0 && (
              <div className="text-center py-12">
                <p className="text-gray-400 text-lg">Aucun film trouvé</p>
              </div>
            )}

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
                className="px-6 py-2 bg-gradient-to-r from-yellow-500 to-orange-500 text-black font-bold rounded-lg hover:shadow-lg transition-all"
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
