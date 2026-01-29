import React, { useState, useEffect } from 'react'

/**
 * Alternative VideoPlayer avec TMDB API
 * Plus facile que YouTube et inclut poster + backdrop
 */
export default function VideoPlayerTMDB({ movieTitle, movieYear, imdbUrl }) {
  const [trailer, setTrailer] = useState(null)
  const [poster, setPoster] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    if (movieTitle && movieYear) {
      searchTMDB()
    }
  }, [movieTitle, movieYear])

  /**
   * Cherche sur The Movie Database (TMDB)
   * Gratuit, pas de quota restrictif
   */
  async function searchTMDB() {
    setLoading(true)
    setError(null)
    
    try {
      const apiKey = import.meta.env.VITE_TMDB_API_KEY
      
      if (!apiKey) {
        console.warn('VITE_TMDB_API_KEY non configurée')
        setError('Clé TMDB non configurée')
        setLoading(false)
        return
      }

      // 1. Chercher le film
      const searchResponse = await fetch(
        `https://api.themoviedb.org/3/search/movie?api_key=${apiKey}&query=${encodeURIComponent(movieTitle)}&year=${movieYear}`
      )
      
      if (!searchResponse.ok) throw new Error('TMDB search error')
      
      const searchData = await searchResponse.json()
      
      if (!searchData.results || searchData.results.length === 0) {
        setError('Film non trouvé sur TMDB')
        setLoading(false)
        return
      }

      const movieId = searchData.results[0].id
      const posterPath = searchData.results[0].poster_path
      
      if (posterPath) {
        setPoster(`https://image.tmdb.org/t/p/w500${posterPath}`)
      }

      // 2. Obtenir les vidéos
      const videoResponse = await fetch(
        `https://api.themoviedb.org/3/movie/${movieId}/videos?api_key=${apiKey}`
      )
      
      if (!videoResponse.ok) throw new Error('TMDB videos error')
      
      const videoData = await videoResponse.json()
      
      // Chercher le trailer officiel
      const trailerVideo = videoData.results?.find(v => 
        v.type === 'Trailer' && v.site === 'YouTube'
      ) || videoData.results?.[0]
      
      if (trailerVideo) {
        setTrailer({
          id: trailerVideo.id,
          key: trailerVideo.key,
          name: trailerVideo.name,
          type: trailerVideo.type
        })
      } else {
        setError('Aucun trailer disponible')
      }
      
    } catch (err) {
      console.error('Erreur TMDB:', err)
      setError('Impossible de charger les données')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="w-full space-y-4">
      {/* Video */}
      <div className="w-full bg-black rounded-xl overflow-hidden shadow-2xl">
        {loading && (
          <div className="aspect-video bg-gray-800 flex items-center justify-center">
            <div className="text-yellow-400 font-bold animate-pulse">🎬 Chargement...</div>
          </div>
        )}

        {trailer && !loading && (
          <div className="aspect-video">
            <iframe
              width="100%"
              height="100%"
              src={`https://www.youtube.com/embed/${trailer.key}`}
              title={trailer.name}
              frameBorder="0"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowFullScreen
              className="w-full h-full"
            ></iframe>
          </div>
        )}

        {error && !loading && (
          <div className="aspect-video bg-gray-800 flex items-center justify-center">
            <div className="text-center">
              <p className="text-gray-400 mb-2">⚠️ {error}</p>
              {imdbUrl && (
                <a href={imdbUrl} target="_blank" rel="noopener noreferrer"
                   className="text-yellow-400 hover:text-yellow-300 text-sm">
                  Voir sur IMDb →
                </a>
              )}
            </div>
          </div>
        )}

        {!loading && !trailer && !error && (
          <div className="aspect-video bg-gray-800 flex items-center justify-center">
            <p className="text-gray-400">Aucune vidéo disponible</p>
          </div>
        )}
      </div>

      {/* Poster + IMDb Link */}
      <div className="flex gap-4">
        {poster && (
          <div className="hidden sm:block">
            <img 
              src={poster} 
              alt="Poster" 
              className="h-40 rounded-lg shadow-lg object-cover"
            />
          </div>
        )}
        
        <div className="flex-1 flex flex-col justify-between">
          {trailer && (
            <div>
              <p className="text-gray-400 text-sm">
                <span className="text-yellow-400 font-bold">🎬 {trailer.type}</span>
                {" "}{trailer.name}
              </p>
            </div>
          )}
          
          {imdbUrl && (
            <a 
              href={imdbUrl} 
              target="_blank" 
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-yellow-500 to-orange-500 text-black font-bold rounded-lg hover:shadow-lg transition-all w-fit"
            >
              🎬 Plus d'infos sur IMDb
            </a>
          )}
        </div>
      </div>
    </div>
  )
}
