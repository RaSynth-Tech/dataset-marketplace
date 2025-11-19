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
  const [showDataPreview, setShowDataPreview] = useState(false)
  const [showMetadata, setShowMetadata] = useState(false)

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

  const formatValue = (value) => {
    if (value === null || value === undefined) return '—'
    if (typeof value === 'boolean') return value ? 'Yes' : 'No'
    if (typeof value === 'object') return JSON.stringify(value, null, 2)
    return value
  }

  const renderKeyValueGrid = (dataObject) => (
    <dl className="grid grid-cols-1 md:grid-cols-2 gap-4">
      {Object.entries(dataObject).map(([key, value]) => (
        <div key={key} className="bg-gray-50 rounded-lg p-3 border border-gray-100">
          <dt className="text-xs font-medium text-gray-500 uppercase tracking-wide">{key.replace(/_/g, ' ')}</dt>
          <dd className="mt-1 text-sm text-gray-900 whitespace-pre-wrap">{formatValue(value)}</dd>
        </div>
      ))}
    </dl>
  )

  const buildSampleTableData = (sample) => {
    if (!sample) return null

    // Already structured as { columns: [], rows: [] }
    if (sample.columns && Array.isArray(sample.rows)) {
      const columns = sample.columns.length
        ? sample.columns
        : Array.from({ length: sample.rows[0]?.length || 0 }, (_, idx) => `Column ${idx + 1}`)
      return { columns, rows: sample.rows }
    }

    // Array of objects (list of rows)
    if (Array.isArray(sample) && sample.length && typeof sample[0] === 'object') {
      const columns = Array.from(
        sample.reduce((set, row) => {
          Object.keys(row).forEach(key => set.add(key))
          return set
        }, new Set())
      )
      return { columns, rows: sample }
    }

    // Array of arrays
    if (Array.isArray(sample) && Array.isArray(sample[0])) {
      const columns = Array.from({ length: sample[0].length }, (_, idx) => `Column ${idx + 1}`)
      return { columns, rows: sample }
    }

    // Generic object -> use Field / Value table
    if (typeof sample === 'object') {
      const rows = Object.entries(sample).map(([key, value]) => ({
        Field: key,
        Value: typeof value === 'object' ? JSON.stringify(value, null, 2) : value
      }))
      return { columns: ['Field', 'Value'], rows }
    }

    // Primitive fallback
    return {
      columns: ['Value'],
      rows: [{ Value: sample }]
    }
  }

  const renderSampleTable = (sample) => {
    const tableData = buildSampleTableData(sample)

    if (!tableData || !tableData.rows?.length) {
      return <p className="text-sm text-gray-500">No preview available.</p>
    }

    const { columns, rows } = tableData

    return (
      <div className="mt-3 border border-gray-200 rounded-lg overflow-auto">
        <table className="min-w-full divide-y divide-gray-200 text-sm">
          <thead className="bg-gray-50">
            <tr>
              {columns.map(column => (
                <th
                  key={column}
                  className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  {column}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-100">
            {rows.map((row, rowIndex) => {
              const values = Array.isArray(row)
                ? row
                : columns.map(column => (Array.isArray(row) ? row[column] : row[column]))

              return (
                <tr key={rowIndex}>
                  {values.map((value, colIndex) => (
                    <td key={`${rowIndex}-${colIndex}`} className="px-4 py-2 text-gray-900 whitespace-pre-wrap">
                      {formatValue(value)}
                    </td>
                  ))}
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8 transition-colors duration-200">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">{dataset.title}</h1>

        <div className="flex items-center space-x-4 mb-6">
          {dataset.category && (
            <span className="bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 px-3 py-1 rounded-full text-sm">
              {dataset.category}
            </span>
          )}
          <span className="text-gray-600 dark:text-gray-400">
            ⭐ {dataset.rating.toFixed(1)} ({dataset.review_count} reviews)
          </span>
          <span className="text-gray-600 dark:text-gray-400">
            📥 {dataset.download_count} downloads
          </span>
        </div>

        <div className="mb-6">
          <h2 className="text-xl font-semibold mb-2 dark:text-white">Description</h2>
          <p className="text-gray-700 dark:text-gray-300">{dataset.description}</p>
        </div>

        <div className="grid grid-cols-2 gap-4 mb-6">
          <div>
            <span className="text-gray-600 dark:text-gray-400">Size:</span>
            <span className="ml-2 font-semibold dark:text-white">{dataset.size_mb} MB</span>
          </div>
          <div>
            <span className="text-gray-600 dark:text-gray-400">Format:</span>
            <span className="ml-2 font-semibold dark:text-white">{dataset.format || 'N/A'}</span>
          </div>
          {dataset.row_count && (
            <div>
              <span className="text-gray-600 dark:text-gray-400">Rows:</span>
              <span className="ml-2 font-semibold dark:text-white">{dataset.row_count.toLocaleString()}</span>
            </div>
          )}
          {dataset.column_count && (
            <div>
              <span className="text-gray-600 dark:text-gray-400">Columns:</span>
              <span className="ml-2 font-semibold dark:text-white">{dataset.column_count}</span>
            </div>
          )}
        </div>

        {dataset.tags && dataset.tags.length > 0 && (
          <div className="mb-6">
            <h3 className="text-lg font-semibold mb-2 dark:text-white">Tags</h3>
            <div className="flex flex-wrap gap-2">
              {dataset.tags.map((tag, index) => (
                <span
                  key={index}
                  className="bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 px-3 py-1 rounded-full text-sm"
                >
                  {tag}
                </span>
              ))}
            </div>
          </div>
        )}

        {dataset.sample_data && (
          <div className="mb-6">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-semibold mb-2 dark:text-white">Data Preview</h3>
              <button
                onClick={() => setShowDataPreview(prev => !prev)}
                className="text-blue-600 dark:text-blue-400 text-sm font-semibold"
              >
                {showDataPreview ? 'Hide preview' : 'View data'}
              </button>
            </div>
            {showDataPreview && (
              renderSampleTable(dataset.sample_data)
            )}
            {!showDataPreview && (
              <p className="text-sm text-gray-500 dark:text-gray-400">Click &ldquo;View data&rdquo; to inspect sample rows or preview info provided by the seller.</p>
            )}
          </div>
        )}

        {dataset.metadata && Object.keys(dataset.metadata).length > 0 && (
          <div className="mb-6">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-semibold mb-2 dark:text-white">Metadata</h3>
              <button
                onClick={() => setShowMetadata(prev => !prev)}
                className="text-blue-600 dark:text-blue-400 text-sm font-semibold"
              >
                {showMetadata ? 'Hide metadata' : 'View details'}
              </button>
            </div>
            {showMetadata && (
              <div className="mt-2">
                {renderKeyValueGrid(dataset.metadata)}
              </div>
            )}
            {!showMetadata && (
              <p className="text-sm text-gray-500 dark:text-gray-400">View provenance, licensing, and additional attributes shared by the seller.</p>
            )}
          </div>
        )}

        <div className="border-t dark:border-gray-700 pt-6 mt-6">
          <div className="flex justify-between items-center">
            <div>
              <span className="text-3xl font-bold text-blue-600 dark:text-blue-400">${dataset.price}</span>
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
            <div className={`mt-4 p-3 rounded ${message.includes('successful') ? 'bg-green-100 dark:bg-green-900 text-green-700 dark:text-green-200' : 'bg-red-100 dark:bg-red-900 text-red-700 dark:text-red-200'}`}>
              {message}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default DatasetDetail

