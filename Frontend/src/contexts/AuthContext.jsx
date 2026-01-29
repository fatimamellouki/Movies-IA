import React, { createContext, useState, useContext, useEffect } from 'react'
import { setAuthToken } from '../api/client'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [token, setToken] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const t = localStorage.getItem('access_token')
    if (t) {
      setToken(t)
      setAuthToken(t)
    }
    setLoading(false)
  }, [])

  function login(newToken) {
    localStorage.setItem('access_token', newToken)
    setAuthToken(newToken)
    setToken(newToken)
  }

  function logout() {
    localStorage.removeItem('access_token')
    setAuthToken(null)
    setToken(null)
  }

  return (
    <AuthContext.Provider value={{ token, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}
