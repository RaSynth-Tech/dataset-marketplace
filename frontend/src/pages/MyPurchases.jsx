import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { purchaseService } from '../services/api'

function MyPurchases() {
  const [purchases, setPurchases] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // For demo, using user_id = 1
    purchaseService.getUserPurchases(1)
      .then(data => {
        setPurchases(data || [])
        setLoading(false)
      })
      .catch(err => {
        console.error('Error fetching purchases:', err)
        setLoading(false)
      })
  }, [])

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-6">My Purchases</h1>

      {loading ? (
        <div className="text-center py-12 dark:text-gray-300">Loading...</div>
      ) : purchases.length > 0 ? (
        <div className="space-y-4">
          {purchases.map((purchase) => (
            <div
              key={purchase.id}
              className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 hover:shadow-lg transition"
            >
              <div className="flex justify-between items-start">
                <div className="flex-1">
                  <Link
                    to={`/dataset/${purchase.dataset_id}`}
                    className="text-xl font-semibold text-blue-600 dark:text-blue-400 hover:underline"
                  >
                    Dataset #{purchase.dataset_id}
                  </Link>
                  <p className="text-gray-600 dark:text-gray-400 mt-2">
                    Purchased on: {new Date(purchase.purchased_at).toLocaleDateString()}
                  </p>
                  <p className="text-gray-600 dark:text-gray-400">
                    Transaction ID: {purchase.transaction_id}
                  </p>
                </div>
                <div className="text-right">
                  <p className="text-2xl font-bold text-green-600 dark:text-green-400">${purchase.amount}</p>
                  <span className={`inline-block mt-2 px-3 py-1 rounded-full text-sm ${purchase.status === 'completed'
                      ? 'bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200'
                      : 'bg-yellow-100 dark:bg-yellow-900 text-yellow-800 dark:text-yellow-200'
                    }`}>
                    {purchase.status}
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="text-center py-12">
          <p className="text-gray-500 dark:text-gray-400 text-lg mb-4">You haven't purchased any datasets yet.</p>
          <Link
            to="/search"
            className="inline-block bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition"
          >
            Browse Datasets
          </Link>
        </div>
      )}
    </div>
  )
}

export default MyPurchases

