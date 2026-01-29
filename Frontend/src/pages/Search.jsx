import React, {useState, useEffect} from 'react'
import client from '../api/client'
import { Link, useSearchParams } from 'react-router-dom'
import MovieCardWithVideo from '../components/MovieCardWithVideo'

export default function Search(){
  const [searchParams, setSearchParams] = useSearchParams()
  const [query, setQuery] = useState(searchParams.get('q') || '')
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)
  const [searched, setSearched] = useState(!!searchParams.get('q'))

  useEffect(()=>{
    if(searchParams.get('q')){
      performSearch(searchParams.get('q'))
    }
  },[searchParams.get('q')])

  async function performSearch(searchQuery){
    if(!searchQuery.trim()) return
    setLoading(true)
    try{
      const res = await client.get(`/movies/search?q=${encodeURIComponent(searchQuery)}`)
      setResults(Array.isArray(res.data) ? res.data : res.data.results || [])
      setSearched(true)
    }catch(err){
      setResults([])
      setSearched(true)
    }finally{
      setLoading(false)
    }
  }

  async function handleSearch(e){
    e.preventDefault()
    if(!query.trim()) return
    setSearchParams({q: query})
  }

  return (
    <div className="min-h-screen bg-black text-white">
      <div className="max-w-7xl mx-auto px-4 py-12">
        <h1 className="text-4xl font-black bg-gradient-to-r from-yellow-400 to-pink-500 bg-clip-text text-transparent mb-8">🔍 Recherche Films</h1>

        {/* Search Form */}
        <form onSubmit={handleSearch} className="mb-12">
          <div className="flex gap-3">
            <input
              type="text"
              value={query}
              onChange={e=> setQuery(e.target.value)}
              placeholder="Cherchez un film, un réalisateur, un acteur…"
              className="flex-1 px-6 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:border-yellow-500 focus:outline-none transition-colors"
            />
            <button 
              type="submit" 
              className="px-8 py-3 bg-gradient-to-r from-yellow-500 to-orange-500 text-black font-bold rounded-lg hover:shadow-lg transition-all transform hover:scale-105"
            >
              🔎 Chercher
            </button>
          </div>
        </form>

        {/* Results */}
        {loading && (
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
            {[...Array(8)].map((_, i)=> <div key={i} className="bg-gray-800 rounded-xl h-64 animate-pulse"></div>)}
          </div>
        )}

        {!loading && searched && (
          <>
            {results.length === 0 ? (
              <div className="text-center py-16">
                <p className="text-gray-400 text-xl mb-4">
                  Aucun résultat pour "<span className="text-yellow-400 font-bold">{query}</span>"
                </p>
                <p className="text-gray-500">Essayez une autre recherche</p>
              </div>
            ) : (
              <>
                <p className="text-gray-400 mb-8">
                  <span className="text-yellow-400 font-bold">{results.length}</span> résultats trouvés
                </p>
                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
                  {results.map(m=> <MovieCardWithVideo key={m.movie_id} m={m} />)}
                </div>
              </>
            )}
          </>
        )}

        {!searched && (
          <div className="text-center py-16">
            <p className="text-gray-400 text-lg">Entrez le titre d'un film pour commencer votre recherche</p>
          </div>
        )}
      </div>
    </div>
  )
}
