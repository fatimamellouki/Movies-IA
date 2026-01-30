import React from 'react'
import { Link } from 'react-router-dom'
import noImage from "../assets/no_image_availible.jpg";

export default function MovieCard({ m }) {
  return (
    <Link 
      to={`/movies/${m.movie_id}`} 
      className="group relative bg-gradient-to-br from-gray-900 to-gray-800 rounded-xl overflow-hidden shadow-xl hover:shadow-2xl transition-all duration-300 h-64"
    >

      <img
        src={m.poster_url || noImage } 
        alt={m.title}
        className="absolute inset-0 w-full h-full object-cover z-0"
      />
      <div className="absolute inset-0 bg-gradient-to-t from-black via-transparent to-transparent z-10"></div>
      <div className="absolute bottom-0 left-0 right-0 p-4 z-20">
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
    </Link>
  )
}
