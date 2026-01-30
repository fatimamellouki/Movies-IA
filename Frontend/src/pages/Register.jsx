import React, {useState} from 'react'
import client from '../api/client'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'

const OCCUPATIONS = [
  'administrator', 'artist', 'doctor', 'educator', 'engineer',
  'entertainment', 'executive', 'healthcare', 'homemaker', 'lawyer',
  'librarian', 'marketing', 'none', 'other', 'programmer',
  'retired', 'salesman', 'scientist', 'student', 'technician', 'writer'
]

export default function Register(){
  const [form, setForm] = useState({
    email: '',
    password: '',
    name: '',
    age: 25,
    gender: 'M',
    occupation: 'other'
  })
  const [error, setError] = useState(null)
  const navigate = useNavigate()
  const { login } = useAuth()

  function handleChange(e){
    const {name, value} = e.target
    setForm(prev=> ({...prev, [name]: value}))
  }

  async function submit(e){
    e.preventDefault()
    setError(null)
    try{
      const res = await client.post('/register', form)
      // Auto-login after registration
      const loginRes = await client.post('/login', {
        email: form.email,
        password: form.password
      })
      const token = loginRes.data.access_token
      login(token)
      navigate('/select-genres')
    }catch(err){
      setError(err?.response?.data?.message || 'Erreur lors de l\'inscription')
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-gray-900 to-black flex items-center justify-center px-4 py-8">
      <div className="w-full max-w-md bg-gradient-to-br from-gray-900 to-gray-800 p-8 rounded-2xl shadow-2xl border border-purple-500/20">
        <h2 className="text-3xl font-black bg-gradient-to-r from-yellow-400 to-pink-500 bg-clip-text text-transparent mb-2">Créer un compte</h2>
        <p className="text-gray-400 mb-8">Rejoignez MovieRecs et découvrez vos films préférés</p>
        
        <form onSubmit={submit} className="space-y-4">
          <div>
            <label className="text-sm font-semibold text-gray-300">Email</label>
            <input
              type="email"
              name="email"
              value={form.email}
              onChange={handleChange}
              placeholder="vous@exemple.com"
              className="w-full mt-1 p-3 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:border-yellow-500 focus:outline-none transition-colors"
              required
            />
          </div>

          <div>
            <label className="text-sm font-semibold text-gray-300">Mot de passe</label>
            <input
              type="password"
              name="password"
              value={form.password}
              onChange={handleChange}
              placeholder="••••••••"
              className="w-full mt-1 p-3 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:border-yellow-500 focus:outline-none transition-colors"
              required
            />
          </div>

          <div>
            <label className="text-sm font-semibold text-gray-300">Nom complet</label>
            <input
              type="text"
              name="name"
              value={form.name}
              onChange={handleChange}
              placeholder="Jean Dupont"
              className="w-full mt-1 p-3 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:border-yellow-500 focus:outline-none transition-colors"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="text-sm font-semibold text-gray-300">Âge</label>
              <input
                type="number"
                name="age"
                value={form.age}
                onChange={handleChange}
                placeholder="25"
                min="1"
                max="120"
                className="w-full mt-1 p-3 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:border-yellow-500 focus:outline-none transition-colors"
              />
            </div>

            <div>
              <label className="text-sm font-semibold text-gray-300">Genre</label>
              <select name="gender" value={form.gender} onChange={handleChange} className="w-full mt-1 p-3 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-yellow-500 focus:outline-none transition-colors">
                <option value="M">Homme</option>
                <option value="F">Femme</option>
                <option value="O">Autre</option>
              </select>
            </div>
          </div>

          <div>
            <label className="text-sm font-semibold text-gray-300">Profession</label>
            <select 
              name="occupation" 
              value={form.occupation} 
              onChange={handleChange} 
              className="w-full mt-1 p-3 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-yellow-500 focus:outline-none transition-colors"
            >
              {OCCUPATIONS.map(occ=> (
                <option key={occ} value={occ}>
                  {occ.charAt(0).toUpperCase() + occ.slice(1)}
                </option>
              ))}
            </select>
          </div>

          {error && <div className="text-sm text-red-400 bg-red-900/20 p-3 rounded-lg border border-red-500/30">{error}</div>}
          
          <button type="submit" className="w-full bg-gradient-to-r from-yellow-500 to-orange-500 text-black font-bold py-3 rounded-lg hover:shadow-lg hover:shadow-yellow-500/50 transition-all transform hover:scale-105 mt-6">
            S'inscrire
          </button>
        </form>

        <p className="text-sm text-gray-400 mt-6 text-center">
          Déjà inscrit? <Link to="/login" className="text-yellow-400 hover:text-yellow-300 font-bold">Se connecter</Link>
        </p>
      </div>
    </div>
  )
   
}
