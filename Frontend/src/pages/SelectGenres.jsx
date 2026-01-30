// src/pages/SelectGenres.jsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import client from '../api/client';
import { useAuth } from '../contexts/AuthContext';

const GENRES = [
  'Action', 'Adventure', 'Animation', 'Children', 'Comedy',
  'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir',
  'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi',
  'Thriller', 'War', 'Western'
];

export default function SelectGenres() {
  const [selected, setSelected] = useState({});
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const { user } = useAuth();

  const handleToggle = (genre) => {
    setSelected(prev => ({ ...prev, [genre]: !prev[genre] }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    const genreWeights = Object.entries(selected).reduce((acc, [genre, isSelected]) => ({
      ...acc,
      [genre]: isSelected ? 4.0 : 2.5
    }), {});

    try {
      await client.post('/user/preferences', { genre_weights: genreWeights });
      // Le backend récupère l’utilisateur via le JWT, pas via l’URL
      // user._id n’est ni nécessaire, ni utilisé
      navigate('/dashboard');
    } catch (err) {
      setError(err?.response?.data?.message || "Erreur lors de la sauvegarde");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-gray-900 to-black flex items-center justify-center px-4">
      <div className="w-full max-w-2xl">
        <div className="bg-gray-800/50 backdrop-blur border border-purple-500/10 rounded-2xl p-8">
          <h1 className="text-4xl font-bold bg-gradient-to-r from-yellow-400 to-pink-500 bg-clip-text text-transparent mb-2">
            Vos genres préférés
          </h1>
          <p className="text-gray-400 mb-8">Sélectionnez pour affiner vos recommandations</p>

          <form onSubmit={handleSubmit}>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-3 mb-6">
              {GENRES.map(genre => (
                <button
                  key={genre}
                  type="button"
                  onClick={() => handleToggle(genre)}
                  className={`px-4 py-3 rounded-lg font-medium transition-all ${
                    selected[genre]
                      ? 'bg-gradient-to-r from-yellow-500 to-orange-500 text-black shadow-lg shadow-yellow-500/20'
                      : 'bg-gray-700/50 text-gray-300 hover:bg-gray-600'
                  }`}
                >
                  {genre}
                </button>
              ))}
            </div>

            {error && (
              <div className="mb-6 p-4 bg-red-500/10 border border-red-500/30 rounded-lg text-red-400 text-sm">
                {error}
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-gradient-to-r from-yellow-500 to-orange-500 text-black font-semibold py-3 rounded-lg hover:shadow-lg hover:shadow-yellow-500/30 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Enregistrement...' : 'Enregistrer'}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}