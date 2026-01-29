import React, {useEffect, useState} from 'react'
import client from '../api/client'
import { Link, useNavigate } from 'react-router-dom'
import MovieCardWithVideo from '../components/MovieCardWithVideo'

function RecommendationCard({m, score}){
  return (
    <div className="group relative">
      <MovieCardWithVideo m={m} />
      <div className="absolute top-3 right-3 z-30">
        <div className="bg-gradient-to-r from-yellow-500 to-orange-500 text-black px-3 py-1 rounded-lg font-bold text-sm">
          {Number(score).toFixed(1)}
        </div>
      </div>
    </div>
  )
}

export default function Recommendations(){
  const [recs, setRecs] = useState([])
  const [status, setStatus] = useState('loading')
  const navigate = useNavigate()

  useEffect(()=>{
    const token = localStorage.getItem('access_token')
    if(!token){
      setStatus('noauth')
      return
    }
    client.get('/recommendations/first-time')
      .then(r=>{
        const recommendations = Array.isArray(r.data) ? r.data : r.data.recommendations || r.data || []
        setRecs(recommendations)
        setStatus(recommendations.length > 0 ? 'ok' : 'empty')
      })
      .catch(err=>{
        setStatus('error')
      })
  },[])

  if(status === 'loading') return (
    <div className="min-h-screen bg-black flex items-center justify-center">
      <div className="text-yellow-400 text-2xl font-bold animate-pulse">Chargement des recommandations…</div>
    </div>
  )

  if(status === 'noauth') return (
    <div className="min-h-screen bg-black text-white flex items-center justify-center">
      <div className="text-center">
        <p className="text-2xl font-bold mb-4">Connectez-vous pour voir vos recommandations</p>
        <button onClick={()=> navigate('/login')} className="px-8 py-3 bg-gradient-to-r from-yellow-500 to-orange-500 text-black font-bold rounded-lg">
          Se connecter
        </button>
      </div>
    </div>
  )

  if(status === 'error') return (
    <div className="min-h-screen bg-black text-white flex items-center justify-center">
      <div className="text-center">
        <p className="text-2xl font-bold mb-4">Impossible de charger vos recommandations</p>
        <p className="text-gray-400 mb-6">Notez quelques films pour améliorer nos recommandations</p>
        <button onClick={()=> navigate('/movies')} className="px-8 py-3 bg-gradient-to-r from-purple-600 to-indigo-600 text-white font-bold rounded-lg">
          Découvrir des films
        </button>
      </div>
    </div>
  )

  if(status === 'empty') return (
    <div className="min-h-screen bg-black text-white">
      <div className="max-w-7xl mx-auto px-4 py-12">
        <h1 className="text-4xl font-black bg-gradient-to-r from-purple-400 to-pink-500 bg-clip-text text-transparent mb-8">✨ Recommandations</h1>
        <div className="text-center py-12">
          <p className="text-gray-400 text-lg mb-4">Pas assez de données pour des recommandations</p>
          <p className="text-gray-500 mb-6">Commencez à noter des films pour recevoir des recommandations personnalisées</p>
          <Link to="/movies" className="inline-block px-8 py-3 bg-gradient-to-r from-yellow-500 to-orange-500 text-black font-bold rounded-lg hover:shadow-lg transition-all">
            Explorer et noter →
          </Link>
        </div>
      </div>
    </div>
  )

  return (
    <div className="min-h-screen bg-black text-white">
      <div className="max-w-7xl mx-auto px-4 py-12">
        <h1 className="text-4xl font-black bg-gradient-to-r from-purple-400 to-pink-500 bg-clip-text text-transparent mb-2">✨ Recommandations</h1>
        <p className="text-gray-400 mb-8">Films sélectionnés spécialement pour vous</p>

        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          {recs.map(r=> <RecommendationCard key={r.movie_id} m={r} score={r.score} />)}
        </div>

        <div className="text-center mt-12">
          <p className="text-gray-400 mb-4">Explorez plus de films pour affiner vos recommandations</p>
          <Link to="/movies" className="inline-block px-8 py-3 bg-gradient-to-r from-purple-600 to-indigo-600 text-white font-bold rounded-lg hover:shadow-lg transition-all">
            Découvrir d'autres films →
          </Link>
        </div>
      </div>
    </div>
  )
}
