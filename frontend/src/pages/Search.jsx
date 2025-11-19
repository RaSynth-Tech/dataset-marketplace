import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { datasetService } from '../services/api'

function Search() {
  const [datasets, setDatasets] = useState([])
  const [loading, setLoading] = useState(false)
  const [searchParams, setSearchParams] = useState({
    query: '',
    category: '',
    min_price: '',
    max_price: '',
    min_rating: '',
    sort_by: 'relevance',
    page: 1,
    page_size: 20,
  })
  const [total, setTotal] = useState(0)

  const handleSearch = async () => {
    setLoading(true)
    try {
      const params = {
        ...searchParams,
        min_price: searchParams.min_price ? parseFloat(searchParams.min_price) : null,
        max_price: searchParams.max_price ? parseFloat(searchParams.max_price) : null,
        min_rating: searchParams.min_rating ? parseFloat(searchParams.min_rating) : null,
      }
      const data = await datasetService.search(params)
      setDatasets(data.datasets || [])
      setTotal(data.total || 0)
    } catch (error) {
      console.error('Search error:', error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    handleSearch()
  }, [])

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-6">Search Datasets</h1>

      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-6 transition-colors duration-200">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <input
            type="text"
            placeholder="Search..."
            value={searchParams.query}
            onChange={(e) => setSearchParams({ ...searchParams, query: e.target.value })}
            className="border dark:border-gray-600 rounded-lg px-4 py-2 bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 outline-none"
            onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
          />
          <input
            type="text"
            placeholder="Category"
            value={searchParams.category}
            onChange={(e) => setSearchParams({ ...searchParams, category: e.target.value })}
            className="border dark:border-gray-600 rounded-lg px-4 py-2 bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 outline-none"
          />
          <input
            type="number"
            placeholder="Min Price"
            value={searchParams.min_price}
            onChange={(e) => setSearchParams({ ...searchParams, min_price: e.target.value })}
            className="border dark:border-gray-600 rounded-lg px-4 py-2 bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 outline-none"
          />
          <input
            type="number"
            placeholder="Max Price"
            value={searchParams.max_price}
            onChange={(e) => setSearchParams({ ...searchParams, max_price: e.target.value })}
            className="border dark:border-gray-600 rounded-lg px-4 py-2 bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 outline-none"
          />
          <select
            value={searchParams.sort_by}
            onChange={(e) => setSearchParams({ ...searchParams, sort_by: e.target.value })}
            className="border dark:border-gray-600 rounded-lg px-4 py-2 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 outline-none"
          >
            <option value="relevance">Relevance</option>
            <option value="price">Price: Low to High</option>
            <option value="rating">Rating</option>
            <option value="date">Newest</option>
          </select>
        </div>
        <button
          onClick={handleSearch}
          className="mt-4 bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition"
        >
          Search
        </button>
      </div>

      {loading ? (
        <div className="text-center py-12 dark:text-gray-300">Loading...</div>
      ) : (
        <>
          <div className="mb-4 text-gray-600 dark:text-gray-400">
            Found {total} dataset{total !== 1 ? 's' : ''}
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {datasets.map((dataset) => (
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
                    ⭐ {dataset.rating.toFixed(1)} ({dataset.review_count})
                  </span>
                </div>
              </Link>
            ))}
          </div>
          {datasets.length === 0 && !loading && (
            <div className="text-center py-12 text-gray-500 dark:text-gray-400">
              No datasets found. Try adjusting your search criteria.
            </div>
          )}
        </>
      )}
    </div>
  )
}

export default Search

