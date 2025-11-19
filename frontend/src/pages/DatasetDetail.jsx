import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { datasetService, purchaseService } from '../services/api'

function DatasetDetail() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [dataset, setDataset] = useState(null)
  const [loading, setLoading] = useState(true)
  const [purchasing, setPurchasing] = useState(false)
  const [message, setMessage] = useState('')

  useEffect(() => {
    datasetService.getById(id)
      .then(data => {
        setDataset(data)
        setLoading(false)
      })
      .catch(err => {
        console.error('Error fetching dataset:', err)
        setLoading(false)
      })
  }, [id])

  const handlePurchase = async () => {
    setPurchasing(true)
    setMessage('')
    try {
      await purchaseService.create(parseInt(id))
      setMessage('Purchase successful! Redirecting to your purchases...')
      setTimeout(() => {
        navigate('/purchases')
      }, 2000)
    } catch (error) {
      setMessage(error.response?.data?.detail || 'Purchase failed. Please try again.')
    } finally {
      setPurchasing(false)
    }
  }

  if (loading) {
    return <div className="text-center py-12">Loading...</div>
  }

  if (!dataset) {
    return <div className="text-center py-12">Dataset not found</div>
  }

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="bg-white rounded-lg shadow-lg p-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">{dataset.title}</h1>
        
        <div className="flex items-center space-x-4 mb-6">
          {dataset.category && (
            <span className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm">
              {dataset.category}
            </span>
          )}
          <span className="text-gray-600">
            ⭐ {dataset.rating.toFixed(1)} ({dataset.review_count} reviews)
          </span>
          <span className="text-gray-600">
            📥 {dataset.download_count} downloads
          </span>
        </div>

        <div className="mb-6">
          <h2 className="text-xl font-semibold mb-2">Description</h2>
          <p className="text-gray-700">{dataset.description}</p>
        </div>

        <div className="grid grid-cols-2 gap-4 mb-6">
          <div>
            <span className="text-gray-600">Size:</span>
            <span className="ml-2 font-semibold">{dataset.size_mb} MB</span>
          </div>
          <div>
            <span className="text-gray-600">Format:</span>
            <span className="ml-2 font-semibold">{dataset.format || 'N/A'}</span>
          </div>
          {dataset.row_count && (
            <div>
              <span className="text-gray-600">Rows:</span>
              <span className="ml-2 font-semibold">{dataset.row_count.toLocaleString()}</span>
            </div>
          )}
          {dataset.column_count && (
            <div>
              <span className="text-gray-600">Columns:</span>
              <span className="ml-2 font-semibold">{dataset.column_count}</span>
            </div>
          )}
        </div>

        {dataset.tags && dataset.tags.length > 0 && (
          <div className="mb-6">
            <h3 className="text-lg font-semibold mb-2">Tags</h3>
            <div className="flex flex-wrap gap-2">
              {dataset.tags.map((tag, index) => (
                <span
                  key={index}
                  className="bg-gray-100 text-gray-700 px-3 py-1 rounded-full text-sm"
                >
                  {tag}
                </span>
              ))}
            </div>
          </div>
        )}

        <div className="border-t pt-6 mt-6">
          <div className="flex justify-between items-center">
            <div>
              <span className="text-3xl font-bold text-blue-600">${dataset.price}</span>
            </div>
            <button
              onClick={handlePurchase}
              disabled={purchasing}
              className="bg-blue-600 text-white px-8 py-3 rounded-lg text-lg font-semibold hover:bg-blue-700 transition disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {purchasing ? 'Processing...' : 'Purchase Dataset'}
            </button>
          </div>
          {message && (
            <div className={`mt-4 p-3 rounded ${message.includes('successful') ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
              {message}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default DatasetDetail

