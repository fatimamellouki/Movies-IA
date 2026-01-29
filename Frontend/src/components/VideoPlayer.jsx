import React, { useState, useEffect } from 'react'

/**
 * Composant pour afficher une vidéo YouTube ou IMDb
 * Cherche automatiquement la bande-annonce sur YouTube
 */
export default function VideoPlayer({ movieTitle, movieYear, imdbUrl, onVideoFound }) {
  const [videoUrl, setVideoUrl] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    // Chercher la bande-annonce YouTube au chargement
    if (movieTitle && movieYear) {
      searchYouTubeTrailer()
    }
  }, [movieTitle, movieYear])

  /**
   * Cherche la bande-annonce sur YouTube
   * Note: Nécessite une clé API YouTube
   */
  async function searchYouTubeTrailer() {
    setLoading(true)
    setError(null)
    
    try {
      const query = `${movieTitle} ${movieYear} bande-annonce trailer`
      const apiKey = import.meta.env.VITE_YOUTUBE_API_KEY
      
      if (!apiKey) {
        console.warn('VITE_YOUTUBE_API_KEY non configurée - utiliser fallback')
        setVideoUrl(generateFallbackVideo())
        setLoading(false)
        return
      }

      const response = await fetch(
        `https://www.googleapis.com/youtube/v3/search?part=snippet&q=${encodeURIComponent(query)}&type=video&maxResults=1&key=${apiKey}`
      )
      
      if (!response.ok) throw new Error('YouTube API error')
      
      const data = await response.json()
      
      if (data.items && data.items.length > 0) {
        const videoId = data.items[0].id.videoId
        setVideoUrl(`https://www.youtube.com/embed/${videoId}`)
        if (onVideoFound) onVideoFound(`https://youtube.com/watch?v=${videoId}`)
      } else {
        setError('Bande-annonce non trouvée')
        setVideoUrl(null)
      }
    } catch (err) {
      console.error('Erreur recherche YouTube:', err)
      setError('Impossible de chercher la vidéo')
      setVideoUrl(null)
    } finally {
      setLoading(false)
    }
  }

  /**
   * Génère une URL de secours sans API YouTube
   */
  function generateFallbackVideo() {
    // Utilisez une recherche simple ou un lecteur personnalisé
    // Pour maintenant, on retourne null pour afficher un message
    return null
  }

  return (
    <div className="w-full bg-black rounded-xl overflow-hidden shadow-2xl">
      {loading && (
        <div className="aspect-video bg-gray-800 flex items-center justify-center">
          <div className="text-yellow-400 font-bold animate-pulse">🎬 Recherche de la bande-annonce...</div>
        </div>
      )}

      {videoUrl && !loading && (
        <div className="aspect-video">
          <iframe
            width="100%"
            height="100%"
            src={videoUrl}
            title="Bande-annonce"
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
            <p className="text-gray-500 text-sm">La bande-annonce n'est pas disponible</p>
          </div>
        </div>
      )}

      {!loading && !videoUrl && !error && (
        <div className="aspect-video bg-gray-800 flex items-center justify-center">
          <p className="text-gray-400">Aucune vidéo disponible</p>
        </div>
      )}
    </div>
  )
}
