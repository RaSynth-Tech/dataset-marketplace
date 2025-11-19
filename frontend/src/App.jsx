import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Home from './pages/Home'
import Search from './pages/Search'
import DatasetDetail from './pages/DatasetDetail'
import MyPurchases from './pages/MyPurchases'
import './App.css'

import { AuthProvider } from './context/AuthContext'
import LoginCallback from './components/LoginCallback'
import Login from './pages/Login'
import Support from './pages/Support'

function App() {
  return (
    <Router>
      <AuthProvider>
        <div className="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-200">
          <Navbar />
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/search" element={<Search />} />
            <Route path="/dataset/:id" element={<DatasetDetail />} />
            <Route path="/purchases" element={<MyPurchases />} />
            <Route path="/support" element={<Support />} />
            <Route path="/login" element={<Login />} />
            <Route path="/auth/callback" element={<LoginCallback />} />
          </Routes>
        </div>
      </AuthProvider>
    </Router>
  )
}

export default App

