import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export const datasetService = {
  search: async (params) => {
    const response = await api.get('/api/datasets/search', { params })
    return response.data
  },

  getById: async (id) => {
    const response = await api.get(`/api/datasets/${id}`)
    return response.data
  },

  getRecommendations: async () => {
    const response = await api.get('/api/datasets/recommendations')
    return response.data
  },

  list: async (skip = 0, limit = 20) => {
    const response = await api.get('/api/datasets/', { params: { skip, limit } })
    return response.data
  },
}

export const purchaseService = {
  create: async (datasetId) => {
    const response = await api.post('/api/purchases/', { dataset_id: datasetId })
    return response.data
  },

  getUserPurchases: async (userId) => {
    const response = await api.get(`/api/purchases/user/${userId}`)
    return response.data
  },
}

export const supportService = {
  query: async (query) => {
    const response = await api.post('/api/support/query', { query })
    return response.data
  },
}

export default api

