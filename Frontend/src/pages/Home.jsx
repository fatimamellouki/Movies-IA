import React, {useEffect, useState} from 'react'
import client from '../api/client'
import { Link } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import MovieCardWithVideo from '../components/MovieCardWithVideo'

export default function Home(){
  const [popular, setPopular] = useState([])
  const { token } = useAuth()

  useEffect(()=>{
    client.get('/movies/popular').then(r=>setPopular(r.data)).catch(()=>{})
  },[])

  return (
    <div className="min-h-screen bg-black text-white">
      {/* Hero Section */}
      <div className="relative h-96 bg-gradient-to-r from-indigo-900 via-purple-900 to-black overflow-hidden">
        <div className="absolute inset-0 opacity-30">
          <div className="absolute top-0 left-1/4 w-96 h-96 bg-purple-500 rounded-full mix-blend-screen filter blur-3xl"></div>
          <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-indigo-500 rounded-full mix-blend-screen filter blur-3xl"></div>
        </div>
        
        <div className="relative z-10 h-full flex flex-col items-center justify-center text-center px-4">
          <h1 className="text-6xl font-black mb-4 bg-gradient-to-r from-yellow-400 via-pink-500 to-purple-500 bg-clip-text text-transparent">
            🎬 MovieRecs
          </h1>
          <p className="text-xl text-gray-300 mb-8 max-w-2xl">Découvrez vos films préférés grâce à l'IA</p>
          
          {!token && (
            <div className="flex gap-4">
              <Link to="/login" className="px-8 py-3 bg-yellow-500 text-black font-bold rounded-lg hover:bg-yellow-400 transition-all transform hover:scale-105">
                Se connecter
              </Link>
              <Link to="/register" className="px-8 py-3 bg-purple-600 text-white font-bold rounded-lg hover:bg-purple-700 transition-all transform hover:scale-105">
                S'inscrire
              </Link>
            </div>
          )}
          
          {token && (
            <Link to="/dashboard" className="px-8 py-3 bg-yellow-500 text-black font-bold rounded-lg hover:bg-yellow-400 transition-all transform hover:scale-105">
              Aller au Dashboard
            </Link>
          )}
        </div>
      </div>

      {/* Contenu Principal */}
      <div className="max-w-7xl mx-auto px-4 py-16">
        {/* Films Populaires */}
        <section className="mb-16">
          <div className="flex items-center justify-between mb-8">
            <h2 className="text-4xl font-black bg-gradient-to-r from-yellow-400 to-pink-500 bg-clip-text text-transparent">🔥 Films Populaires</h2>
            <Link to="/movies" className="text-yellow-400 hover:text-yellow-300 font-bold">Voir tous →</Link>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
            {popular.slice(0,8).map(m=> <MovieCardWithVideo key={m.movie_id} m={m} />)}
          </div>
        </section>

        {/* À Propos */}
        <section className="bg-gradient-to-r from-gray-900 to-gray-800 rounded-2xl p-12 border border-purple-500/20">
          <h2 className="text-3xl font-black text-white mb-4">À Propos de MovieRecs</h2>
          <p className="text-gray-300 text-lg leading-relaxed">
            MovieRecs utilise l'intelligence artificielle pour recommander les meilleurs films basés sur vos préférences.
            Notre système analyse vos notes, vos goûts et ceux d'utilisateurs similaires pour vous proposer des films que vous aimerez.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-8">
            <div className="text-center">
              <div className="text-4xl mb-2">🎯</div>
              <h3 className="font-bold text-yellow-400 mb-2">IA Intelligente</h3>
              <p className="text-gray-400">Algorithmes hybrides pour des recommandations précises</p>
            </div>
            <div className="text-center">
              <div className="text-4xl mb-2">⭐</div>
              <h3 className="font-bold text-yellow-400 mb-2">Vos Goûts</h3>
              <p className="text-gray-400">Notez et découvrez des films qui vous correspondent</p>
            </div>
            <div className="text-center">
              <div className="text-4xl mb-2">🎬</div>
              <h3 className="font-bold text-yellow-400 mb-2">Partage Social</h3>
              <p className="text-gray-400">Trouvez des films aimés par des gens comme vous</p>
            </div>
          </div>
        </section>
      </div>
    </div>
  )
}
