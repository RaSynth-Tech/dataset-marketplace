import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Home from './pages/Home'
import Search from './pages/Search'
import DatasetDetail from './pages/DatasetDetail'
import MyPurchases from './pages/MyPurchases'
import './App.css'

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/search" element={<Search />} />
          <Route path="/dataset/:id" element={<DatasetDetail />} />
          <Route path="/purchases" element={<MyPurchases />} />
        </Routes>
      </div>
    </Router>
  )
}

export default App

