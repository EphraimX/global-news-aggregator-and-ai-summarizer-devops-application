"use client"

import { createContext, useContext, useState, useEffect } from "react"
import { apiClient } from "@/lib/api"

const NewsContext = createContext(undefined)

export function NewsProvider({ children }) {
  const [articles, setArticles] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [selectedRegion, setSelectedRegion] = useState("Global")
  const [selectedTopic, setSelectedTopic] = useState("All")
  const [selectedSource, setSelectedSource] = useState("All")
  const [searchQuery, setSearchQuery] = useState("")
  const [dateRange, setDateRange] = useState("Today")

  // Fetch articles from backend
  const fetchArticles = async () => {
    setLoading(true)
    setError(null)

    try {
      const filters = {
        region: selectedRegion,
        topic: selectedTopic !== "All" ? selectedTopic : undefined,
        source: selectedSource !== "All" ? selectedSource : undefined,
        date_range: dateRange,
        search_query: searchQuery || undefined,
        limit: 20,
        page: 1,
      }

      const fetchedArticles = await apiClient.getArticles(filters)

      // Transform backend data to frontend format
      const transformedArticles = fetchedArticles.map((article) => ({
        id: article.id,
        title: article.title,
        source: {
          name: article.source.name,
          favicon: article.source.favicon,
          color: article.source.color,
        },
        originalExcerpt: article.original_excerpt,
        summary: article.summary,
        publishedAt: article.published_at,
        topic: article.topic,
        url: article.url,
        imageUrl: article.image_url,
        viewCount: article.view_count,
        likeCount: article.like_count,
        isLoadingSummary: false,
      }))

      setArticles(transformedArticles)
    } catch (err) {
      console.error("Failed to fetch articles:", err)
      setError("Failed to load articles. Please try again.")
    } finally {
      setLoading(false)
    }
  }

  // Generate AI summary
  const generateSummary = async (articleId) => {
    setArticles((prev) =>
      prev.map((article) => (article.id === articleId ? { ...article, isLoadingSummary: true } : article)),
    )

    try {
      const article = articles.find((a) => a.id === articleId)
      if (!article) return

      const response = await apiClient.generateSummary(article.title, article.originalExcerpt)

      setArticles((prev) =>
        prev.map((a) => (a.id === articleId ? { ...a, summary: response.summary, isLoadingSummary: false } : a)),
      )
    } catch (err) {
      console.error("Failed to generate summary:", err)
      setArticles((prev) => prev.map((a) => (a.id === articleId ? { ...a, isLoadingSummary: false } : a)))
    }
  }

  // Track article view
  const trackView = async (articleId) => {
    try {
      await apiClient.trackView(articleId)
      // Update local view count
      setArticles((prev) => prev.map((a) => (a.id === articleId ? { ...a, viewCount: a.viewCount + 1 } : a)))
    } catch (err) {
      console.error("Failed to track view:", err)
    }
  }

  // Toggle like
  const toggleLike = async (articleId) => {
    try {
      await apiClient.toggleLike(articleId)
      // Update local like count
      setArticles((prev) => prev.map((a) => (a.id === articleId ? { ...a, likeCount: a.likeCount + 1 } : a)))
    } catch (err) {
      console.error("Failed to toggle like:", err)
    }
  }

  const toggleSummaryView = (articleId) => {
    const article = articles.find((a) => a.id === articleId)
    if (article && !article.summary && !article.isLoadingSummary) {
      generateSummary(articleId)
    }
  }

  // Filter articles based on current filters
  const filteredArticles = articles.filter((article) => {
    const matchesSearch =
      !searchQuery ||
      article.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      article.originalExcerpt.toLowerCase().includes(searchQuery.toLowerCase())

    const matchesTopic = selectedTopic === "All" || article.topic === selectedTopic
    const matchesSource = selectedSource === "All" || article.source.name === selectedSource

    return matchesSearch && matchesTopic && matchesSource
  })

  // Fetch articles when filters change
  useEffect(() => {
    fetchArticles()
  }, [selectedRegion, selectedTopic, selectedSource, dateRange])

  // Search with debounce
  useEffect(() => {
    const timeoutId = setTimeout(() => {
      if (searchQuery !== "") {
        fetchArticles()
      }
    }, 500)

    return () => clearTimeout(timeoutId)
  }, [searchQuery])

  return (
    <NewsContext.Provider
      value={{
        articles,
        filteredArticles,
        loading,
        error,
        selectedRegion,
        selectedTopic,
        selectedSource,
        searchQuery,
        dateRange,
        setSelectedRegion,
        setSelectedTopic,
        setSelectedSource,
        setSearchQuery,
        setDateRange,
        generateSummary,
        toggleSummaryView,
        trackView,
        toggleLike,
        refetchArticles: fetchArticles,
      }}
    >
      {children}
    </NewsContext.Provider>
  )
}

export function useNews() {
  const context = useContext(NewsContext)
  if (context === undefined) {
    throw new Error("useNews must be used within a NewsProvider")
  }
  return context
}
