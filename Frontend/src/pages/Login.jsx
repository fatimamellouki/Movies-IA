import React, {useState} from 'react'
import client from '../api/client'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'

export default function Login(){
  const [email,setEmail] = useState('')
  const [password,setPassword] = useState('')
  const [error,setError] = useState(null)
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()
  const { login } = useAuth()

  async function submit(e){
    e.preventDefault()
    setLoading(true)
    try{
      const res = await client.post('/login', {email, password})
      const token = res.data.access_token
      login(token)
      navigate('/dashboard')
    }catch(err){
      setError(err?.response?.data?.message || 'Erreur lors de la connexion')
    }finally{
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-gray-900 to-black flex items-center justify-center px-4 py-8">
      <div className="w-full max-w-md bg-gradient-to-br from-gray-900 to-gray-800 p-8 rounded-2xl shadow-2xl border border-purple-500/20">
        <div className="text-center mb-8">
          <h2 className="text-4xl font-black bg-gradient-to-r from-yellow-400 to-pink-500 bg-clip-text text-transparent mb-2">Se connecter</h2>
          <p className="text-gray-400">Bienvenue sur MovieRecs</p>
        </div>

        <form onSubmit={submit} className="space-y-4">
          <div>
            <label className="text-sm font-semibold text-gray-300">Email</label>
            <input
              type="email"
              value={email}
              onChange={e=>setEmail(e.target.value)}
              placeholder="vous@exemple.com"
              className="w-full mt-1 p-3 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:border-yellow-500 focus:outline-none transition-colors"
              required
            />
          </div>

          <div>
            <label className="text-sm font-semibold text-gray-300">Mot de passe</label>
            <input
              type="password"
              value={password}
              onChange={e=>setPassword(e.target.value)}
              placeholder="••••••••"
              className="w-full mt-1 p-3 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:border-yellow-500 focus:outline-none transition-colors"
              required
            />
          </div>

          {error && <div className="text-sm text-red-400 bg-red-900/20 p-3 rounded-lg border border-red-500/30">{error}</div>}
          
          <button 
            type="submit" 
            disabled={loading}
            className="w-full bg-gradient-to-r from-yellow-500 to-orange-500 text-black font-bold py-3 rounded-lg hover:shadow-lg hover:shadow-yellow-500/50 transition-all transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed mt-6"
          >
            {loading ? 'Connexion en cours...' : 'Se connecter'}
          </button>
        </form>

        <p className="text-sm text-gray-400 mt-6 text-center">
          Pas encore inscrit? <Link to="/register" className="text-yellow-400 hover:text-yellow-300 font-bold">Créer un compte</Link>
        </p>
      </div>
    </div>
  )
}
