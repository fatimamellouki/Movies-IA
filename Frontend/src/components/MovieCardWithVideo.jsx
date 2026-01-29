import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'

export default function MovieCardWithVideo({ m }) {
  const [videoId, setVideoId] = useState(null)
  const [showVideo, setShowVideo] = useState(false)
  const [loading, setLoading] = useState(false)

  const searchYouTubeTrailer = async () => {
    if (videoId) return // Already loaded
    
    setLoading(true)
    const apiKey = import.meta.env.VITE_YOUTUBE_API_KEY
    if (!apiKey) {
      setLoading(false)
      return
    }

    const searchQuery = `${m.title} ${m.year} bande-annonce trailer`
    const url = `https://www.googleapis.com/youtube/v3/search?part=snippet&q=${encodeURIComponent(searchQuery)}&type=video&key=${apiKey}&maxResults=1`

    try {
      const response = await fetch(url)
      const data = await response.json()
      if (data.items && data.items.length > 0) {
        setVideoId(data.items[0].id.videoId)
      }
    } catch (error) {
      console.error('Erreur YouTube:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <Link 
      to={`/movies/${m.movie_id}`} 
      className="group relative bg-gradient-to-br from-gray-900 to-gray-800 rounded-xl overflow-hidden shadow-xl hover:shadow-2xl transition-all duration-300 h-64"
      onMouseEnter={() => {
        setShowVideo(true)
        searchYouTubeTrailer()
      }}
      onMouseLeave={() => setShowVideo(false)}
    >
      {/* Video Preview on Hover */}
      {showVideo && videoId && (
        <iframe
          src={`https://www.youtube.com/embed/${videoId}?autoplay=1&mute=1`}
          title={m.title}
          frameBorder="0"
          allow="autoplay"
          className="absolute inset-0 w-full h-full z-20"
        />
      )}

      {/* Card Content */}
      {!showVideo && (
        <>
          <div className="absolute inset-0 bg-gradient-to-t from-black via-transparent to-transparent"></div>
          <div className="absolute inset-0 group-hover:bg-black/20 transition-colors">
           
          </div>
          <div className="absolute bottom-0 left-0 right-0 p-4 z-10">
            <h3 className="font-bold text-lg text-white group-hover:text-yellow-400 transition-colors line-clamp-2">
              {m.title}
            </h3>
            <div className="flex items-center gap-2 mt-2">
              <span className="text-xs bg-yellow-500 text-black px-2 py-1 rounded font-bold">
                ★ {m.bayesian_rating?.toFixed(1) || '?'}
              </span>
              <span className="text-xs text-gray-300">{m.year}</span>
            </div>
            <p className="text-xs text-gray-300 mt-2 line-clamp-1">
              {m.genres?.slice(0, 2).join(', ')}
            </p>
          </div>
        </>
      )}

      {/* Loading indicator */}
      {showVideo && loading && !videoId && (
        <div className="absolute inset-0 flex items-center justify-center bg-black/50 z-20">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-yellow-400"></div>
        </div>
      )}
    </Link>
  )
}
