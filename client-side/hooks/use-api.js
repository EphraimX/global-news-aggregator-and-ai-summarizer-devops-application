"use client"

import { useState, useEffect } from "react"
import { apiClient } from "@/lib/api"

export function useApi(endpoint, options = {}) {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true)
        setError(null)
        const result = await apiClient.request(endpoint, options)
        setData(result)
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [endpoint])

  const refetch = async () => {
    try {
      setLoading(true)
      setError(null)
      const result = await apiClient.request(endpoint, options)
      setData(result)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return { data, loading, error, refetch }
}

export function useArticles(filters = {}) {
  const [articles, setArticles] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const fetchArticles = async () => {
    try {
      setLoading(true)
      setError(null)
      const result = await apiClient.getArticles(filters)
      setArticles(result)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchArticles()
  }, [JSON.stringify(filters)])

  return { articles, loading, error, refetch: fetchArticles }
}

export function useTrendingTopics() {
  return useApi("/api/news/trending")
}

export function useNewsStats() {
  return useApi("/api/news/stats")
}
