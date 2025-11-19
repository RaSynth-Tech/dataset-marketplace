import React from 'react'
import { Link } from 'react-router-dom'

function Navbar() {
  return (
    <nav className="bg-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex">
            <Link to="/" className="flex items-center">
              <span className="text-2xl font-bold text-blue-600">Dataset Marketplace</span>
            </Link>
          </div>
          <div className="flex items-center space-x-4">
            <Link
              to="/search"
              className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium"
            >
              Browse
            </Link>
            <Link
              to="/purchases"
              className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium"
            >
              My Purchases
            </Link>
          </div>
        </div>
      </div>
    </nav>
  )
}

export default Navbar

