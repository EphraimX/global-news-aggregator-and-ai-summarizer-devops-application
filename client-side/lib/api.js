// API Configuration for Global News Digest AI

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

class ApiClient {
  constructor() {
    this.baseURL = API_BASE_URL
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`

    const config = {
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
      ...options,
    }

    try {
      const response = await fetch(url, config)

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      return await response.json()
    } catch (error) {
      console.error("API request failed:", error)
      throw error
    }
  }

  // News endpoints
  async getArticles(filters = {}) {
    const params = new URLSearchParams()

    Object.entries(filters).forEach(([key, value]) => {
      if (value !== null && value !== undefined && value !== "") {
        params.append(key, value)
      }
    })

    const queryString = params.toString()
    const endpoint = `/api/news/articles${queryString ? `?${queryString}` : ""}`

    return this.request(endpoint)
  }

  async getTrendingTopics() {
    return this.request("/api/news/trending")
  }

  async getNewsStats() {
    return this.request("/api/news/stats")
  }

  async getNewsSources() {
    return this.request("/api/news/sources")
  }

  // AI endpoints
  async generateSummary(title, content) {
    return this.request("/api/ai/summarize", {
      method: "POST",
      body: JSON.stringify({ title, content }),
    })
  }

  // Interaction endpoints
  async trackView(articleId) {
    return this.request(`/api/news/articles/${articleId}/view`, {
      method: "POST",
    })
  }

  async toggleLike(articleId) {
    return this.request(`/api/news/articles/${articleId}/like`, {
      method: "POST",
    })
  }

  // Health check
  async healthCheck() {
    return this.request("/health")
  }
}

export const apiClient = new ApiClient()
export default apiClient
