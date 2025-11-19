import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { datasetService } from '../services/api'

function Home() {
  const [recommendations, setRecommendations] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // For demo, using user_id = 1
    datasetService.getRecommendations(1)
      .then(data => {
        setRecommendations(data.recommendations || [])
        setLoading(false)
      })
      .catch(err => {
        console.error('Error fetching recommendations:', err)
        setLoading(false)
      })
  }, [])

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
          Find and Buy Quality Datasets
        </h1>
        <p className="text-xl text-gray-600 dark:text-gray-300 mb-8">
          Discover datasets from various categories and domains
        </p>
        <Link
          to="/search"
          className="inline-block bg-blue-600 text-white px-8 py-3 rounded-lg text-lg font-semibold hover:bg-blue-700 transition"
        >
          Browse Datasets
        </Link>
      </div>

      <div className="mb-8">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">Recommended for You</h2>
        {loading ? (
          <div className="text-center py-12 dark:text-gray-300">Loading recommendations...</div>
        ) : recommendations.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {recommendations.map((dataset) => (
              <Link
                key={dataset.id}
                to={`/dataset/${dataset.id}`}
                className="bg-white dark:bg-gray-800 rounded-lg shadow-md hover:shadow-xl transition p-6"
              >
                <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">{dataset.title}</h3>
                <p className="text-gray-600 dark:text-gray-300 mb-4 line-clamp-2">{dataset.description}</p>
                <div className="flex justify-between items-center">
                  <span className="text-2xl font-bold text-blue-600 dark:text-blue-400">${dataset.price}</span>
                  <span className="text-sm text-gray-500 dark:text-gray-400">
                    ⭐ {dataset.rating.toFixed(1)} ({dataset.review_count})
                  </span>
                </div>
              </Link>
            ))}
          </div>
        ) : (
          <div className="text-center py-12 text-gray-500 dark:text-gray-400">
            No recommendations available. Start browsing datasets!
          </div>
        )}
      </div>
    </div>
  )
}

export default Home

