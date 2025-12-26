import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Handle token expiration
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export interface LoginData {
  username: string
  password: string
}

export interface RegisterData {
  username: string
  password: string
  currency_preference?: string
}

export interface DashboardSummary {
  net_worth: number
  total_assets: number
  total_liabilities: number
  monthly_income: number
  monthly_expenses: number
  savings_rate: number
  top_spending_categories: Array<{ category: string; amount: number }>
}

export interface Transaction {
  id: number
  account_id: number
  amount: number
  category: string
  description: string | null
  timestamp: string
}

export interface InvestmentPerformance {
  total_value: number
  total_cost_basis: number
  total_return: number
  total_return_percentage: number
  time_weighted_return: number
  sharpe_ratio: number | null
  asset_allocation: Array<{ ticker: string; value: number; percentage: number }>
}

export const authAPI = {
  login: async (data: LoginData) => {
    const formData = new FormData()
    formData.append('username', data.username)
    formData.append('password', data.password)
    const response = await api.post('/api/auth/login', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    return response.data
  },
  register: async (data: RegisterData) => {
    const response = await api.post('/api/auth/register', data)
    return response.data
  },
}

export const dashboardAPI = {
  getSummary: async (): Promise<DashboardSummary> => {
    const response = await api.get('/api/dashboard/summary')
    return response.data
  },
}

export const transactionsAPI = {
  getTransactions: async (skip: number = 0, limit: number = 100): Promise<Transaction[]> => {
    const response = await api.get(`/api/transactions/?skip=${skip}&limit=${limit}`)
    return response.data
  },
  uploadCSV: async (file: File, accountId?: number) => {
    const formData = new FormData()
    formData.append('file', file)
    const response = await api.post(`/api/transactions/upload?account_id=${accountId || ''}`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    return response.data
  },
}

export const investmentsAPI = {
  getPerformance: async (): Promise<InvestmentPerformance> => {
    const response = await api.get('/api/investments/performance')
    return response.data
  },
}

export default api

