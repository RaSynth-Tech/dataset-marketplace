import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { datasetService } from '../services/api'

function Home() {
  const [recommendations, setRecommendations] = useState([])
  const [externalRecommendations, setExternalRecommendations] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // For demo, using user_id = 1
    datasetService.getRecommendations(1)
      .then(data => {
        setRecommendations(data.recommendations || [])
        setExternalRecommendations(data.external_recommendations || [])
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
                {dataset.category && (
                  <span className="inline-block bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 text-xs px-2 py-1 rounded mb-2">
                    {dataset.category}
                  </span>
                )}
                <div className="flex justify-between items-center mt-4">
                  <span className="text-2xl font-bold text-blue-600 dark:text-blue-400">${dataset.price}</span>
                  <span className="text-sm text-gray-500 dark:text-gray-400">
                    ⭐ {dataset.rating.toFixed(1)}
                  </span>
                </div>
              </Link>
            ))}
          </div>
        ) : (
          <div className="text-center py-12 text-gray-500 dark:text-gray-400">
            No recommendations available yet.
          </div>
        )}
      </div>

      {/* External Recommendations Section */}
      {externalRecommendations.length > 0 && (
        <div className="mt-12">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
            🌐 You Might Also Like (External Sources)
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {externalRecommendations.map((dataset, index) => (
              <a
                key={index}
                href={dataset.url}
                target="_blank"
                rel="noopener noreferrer"
                className="bg-gradient-to-br from-green-50 to-teal-50 dark:from-green-900/20 dark:to-teal-900/20 rounded-lg shadow-md hover:shadow-xl transition p-6 border-2 border-green-200 dark:border-green-700"
              >
                <div className="flex items-start justify-between mb-2">
                  <h3 className="text-xl font-semibold text-gray-900 dark:text-white flex-1">{dataset.title}</h3>
                  <svg className="w-5 h-5 text-green-600 dark:text-green-400 flex-shrink-0 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                  </svg>
                </div>
                <p className="text-gray-600 dark:text-gray-300 mb-4 text-sm line-clamp-3">{dataset.description}</p>
                <div className="flex flex-wrap gap-2 mb-3">
                  <span className="inline-block bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200 text-xs px-2 py-1 rounded">
                    {dataset.source}
                  </span>
                  <span className="inline-block bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200 text-xs px-2 py-1 rounded">
                    {dataset.format}
                  </span>
                  {dataset.relevance_score && (
                    <span className="inline-block bg-yellow-100 dark:bg-yellow-900 text-yellow-800 dark:text-yellow-200 text-xs px-2 py-1 rounded">
                      {dataset.relevance_score} Match
                    </span>
                  )}
                </div>
                <div className="text-xs text-green-600 dark:text-green-400 font-medium">
                  View on {dataset.source} →
                </div>
              </a>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default Home
