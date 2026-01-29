import React, {useEffect, useState} from 'react'
import client from '../api/client'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'

const OCCUPATIONS = [
  'administrator', 'artist', 'doctor', 'educator', 'engineer',
  'entertainment', 'executive', 'healthcare', 'homemaker', 'lawyer',
  'librarian', 'marketing', 'none', 'other', 'programmer',
  'retired', 'salesman', 'scientist', 'student', 'technician', 'writer'
]

export default function Profile(){
  const [profile, setProfile] = useState(null)
  const [edit, setEdit] = useState(false)
  const [form, setForm] = useState({})
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()
  const { logout } = useAuth()

  const token = localStorage.getItem('access_token')

  useEffect(()=>{
    if(!token) return navigate('/login')
    setLoading(true)
    client.get('/user/profile')
      .then(r=> {
        setProfile(r.data)
        setForm(r.data)
      })
      .catch(err=> setError('Impossible de charger le profil'))
      .finally(()=> setLoading(false))
  },[token, navigate])

  async function handleUpdate(e){
    e.preventDefault()
    setError(null)
    try{
      await client.put('/user/profile', form)
      setProfile(form)
      setEdit(false)
    }catch(err){
      setError(err?.response?.data?.message || 'Erreur lors de la mise à jour')
    }
  }

  async function handleDelete(){
    if(!window.confirm('Êtes-vous sûr? Cette action est irréversible et supprimera tous vos données.')) return
    try{
      await client.delete('/user/account')
      logout()
      navigate('/')
    }catch(err){
      setError('Erreur lors de la suppression')
    }
  }

  if(loading) return (
    <div className="min-h-screen bg-black flex items-center justify-center">
      <div className="text-yellow-400 text-2xl font-bold animate-pulse">Chargement…</div>
    </div>
  )

  if(!profile) return (
    <div className="min-h-screen bg-black text-white flex items-center justify-center">
      <div className="text-center">
        <p className="text-2xl font-bold mb-4">Impossible de charger votre profil</p>
      </div>
    </div>
  )

  return (
    <div className="min-h-screen bg-black text-white">
      <div className="max-w-4xl mx-auto px-4 py-12">
        <h1 className="text-4xl font-black bg-gradient-to-r from-purple-400 to-pink-500 bg-clip-text text-transparent mb-8">👤 Mon Profil</h1>

        {error && <div className="bg-red-900/30 text-red-300 border border-red-500/30 p-4 rounded-lg mb-8">{error}</div>}

        {!edit ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {/* Profile Info */}
            <div className="bg-gradient-to-br from-gray-900 to-gray-800 p-8 rounded-xl border border-purple-500/20 shadow-xl">
              <h2 className="text-2xl font-bold text-yellow-400 mb-6">Informations</h2>
              <div className="space-y-4">
                <div>
                  <label className="text-gray-400 text-sm">Email</label>
                  <p className="text-white text-lg font-semibold">{profile.email}</p>
                </div>
                <div>
                  <label className="text-gray-400 text-sm">Nom</label>
                  <p className="text-white text-lg font-semibold">{profile.name || 'Non renseigné'}</p>
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="text-gray-400 text-sm">Âge</label>
                    <p className="text-white text-lg font-semibold">{profile.age}</p>
                  </div>
                  <div>
                    <label className="text-gray-400 text-sm">Genre</label>
                    <p className="text-white text-lg font-semibold">{profile.gender === 'M' ? 'Homme' : profile.gender === 'F' ? 'Femme' : 'Autre'}</p>
                  </div>
                </div>
                <div>
                  <label className="text-gray-400 text-sm">Profession</label>
                  <p className="text-white text-lg font-semibold capitalize">{profile.occupation}</p>
                </div>
              </div>
            </div>

            {/* Stats */}
            <div className="space-y-6">
              <div className="bg-gradient-to-br from-yellow-600 to-orange-600 p-6 rounded-xl shadow-xl">
                <p className="text-white/80 text-sm">Films notés</p>
                <p className="text-5xl font-black text-white">{profile.ratings_count || 0}</p>
              </div>
              <div className="bg-gradient-to-br from-purple-600 to-indigo-600 p-6 rounded-xl shadow-xl">
                <p className="text-white/80 text-sm">Cluster ID</p>
                <p className="text-4xl font-black text-white">{profile.cluster_id || '—'}</p>
              </div>
              
              {/* Edit Button */}
              <button
                onClick={()=> setEdit(true)}
                className="w-full px-6 py-3 bg-gradient-to-r from-blue-600 to-cyan-600 text-white font-bold rounded-lg hover:shadow-lg transition-all transform hover:scale-105"
              >
                ✏️ Éditer le profil
              </button>
            </div>
          </div>
        ) : (
          <div className="max-w-2xl bg-gradient-to-br from-gray-900 to-gray-800 p-8 rounded-xl border border-purple-500/20 shadow-xl">
            <h2 className="text-2xl font-bold text-yellow-400 mb-6">Modifier le profil</h2>
            <form onSubmit={handleUpdate} className="space-y-5">
              <div>
                <label className="text-sm font-semibold text-gray-300">Nom complet</label>
                <input
                  type="text"
                  value={form.name || ''}
                  onChange={e=> setForm(prev=> ({...prev, name: e.target.value}))}
                  placeholder="Jean Dupont"
                  className="w-full mt-1 p-3 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:border-yellow-500 focus:outline-none transition-colors"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-sm font-semibold text-gray-300">Âge</label>
                  <input
                    type="number"
                    value={form.age || 25}
                    onChange={e=> setForm(prev=> ({...prev, age: parseInt(e.target.value)}))}
                    placeholder="25"
                    min="1"
                    max="120"
                    className="w-full mt-1 p-3 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:border-yellow-500 focus:outline-none transition-colors"
                  />
                </div>
                <div>
                  <label className="text-sm font-semibold text-gray-300">Genre</label>
                  <select
                    value={form.gender || 'M'}
                    onChange={e=> setForm(prev=> ({...prev, gender: e.target.value}))}
                    className="w-full mt-1 p-3 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-yellow-500 focus:outline-none transition-colors"
                  >
                    <option value="M">Homme</option>
                    <option value="F">Femme</option>
                    <option value="O">Autre</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="text-sm font-semibold text-gray-300">Profession</label>
                <select
                  value={form.occupation || 'other'}
                  onChange={e=> setForm(prev=> ({...prev, occupation: e.target.value}))}
                  className="w-full mt-1 p-3 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-yellow-500 focus:outline-none transition-colors"
                >
                  {OCCUPATIONS.map(occ=> (
                    <option key={occ} value={occ}>
                      {occ.charAt(0).toUpperCase() + occ.slice(1)}
                    </option>
                  ))}
                </select>
              </div>

              <div className="flex gap-3 pt-4">
                <button 
                  type="submit" 
                  className="flex-1 px-6 py-3 bg-gradient-to-r from-green-600 to-emerald-600 text-white font-bold rounded-lg hover:shadow-lg transition-all transform hover:scale-105"
                >
                  ✓ Sauvegarder
                </button>
                <button 
                  type="button" 
                  onClick={()=> setEdit(false)} 
                  className="flex-1 px-6 py-3 bg-gradient-to-r from-gray-700 to-gray-600 text-white font-bold rounded-lg hover:shadow-lg transition-all"
                >
                  ✕ Annuler
                </button>
              </div>
            </form>
          </div>
        )}

        {/* Danger Zone */}
        <div className="mt-12 p-6 border-2 border-red-500/30 rounded-xl bg-red-900/10">
          <h3 className="text-xl font-bold text-red-400 mb-3">⚠️ Zone dangereuse</h3>
          <p className="text-gray-400 mb-4">La suppression de votre compte est permanente et irréversible.</p>
          <button
            onClick={handleDelete}
            className="px-6 py-2 bg-red-600 hover:bg-red-700 text-white font-bold rounded-lg transition-all"
          >
            Supprimer le compte
          </button>
        </div>
      </div>
    </div>
  )
}
