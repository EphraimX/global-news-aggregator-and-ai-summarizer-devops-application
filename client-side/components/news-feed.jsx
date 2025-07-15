"use client"

import { NewsCard } from "@/components/news-card"
import { useNews } from "@/contexts/news-context"
import { Card, CardContent } from "@/components/ui/card"
import { Newspaper, Sparkles, Loader2, RefreshCw } from "lucide-react"
import { Button } from "@/components/ui/button"

export function NewsFeed() {
  const { filteredArticles, loading, error, searchQuery, selectedTopic, refetchArticles } = useNews()

  if (loading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <Card className="text-center py-16 bg-gradient-to-br from-purple-50 to-pink-50 border-2 border-purple-200 shadow-xl">
          <CardContent>
            <Loader2 className="h-16 w-16 mx-auto text-purple-500 animate-spin mb-4" />
            <h3 className="text-2xl font-bold mb-4 bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
              Loading Amazing News...
            </h3>
            <p className="text-gray-600 text-lg">🤖 Fetching the latest articles with AI summaries</p>
          </CardContent>
        </Card>
      </div>
    )
  }

  if (error) {
    return (
      <div className="container mx-auto px-4 py-8">
        <Card className="text-center py-16 bg-gradient-to-br from-red-50 to-pink-50 border-2 border-red-200 shadow-xl">
          <CardContent>
            <div className="relative mb-6">
              <Newspaper className="h-16 w-16 mx-auto text-red-400" />
              <Sparkles className="absolute -top-2 -right-2 h-8 w-8 text-yellow-400" />
            </div>
            <h3 className="text-2xl font-bold mb-4 bg-gradient-to-r from-red-600 to-pink-600 bg-clip-text text-transparent">
              Oops! Something went wrong
            </h3>
            <p className="text-gray-600 text-lg mb-4">{error}</p>
            <Button
              onClick={refetchArticles}
              className="bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600"
            >
              <RefreshCw className="h-4 w-4 mr-2" />
              Try Again
            </Button>
          </CardContent>
        </Card>
      </div>
    )
  }

  if (filteredArticles.length === 0) {
    return (
      <div className="container mx-auto px-4 py-8">
        <Card className="text-center py-16 bg-gradient-to-br from-purple-50 to-pink-50 border-2 border-purple-200 shadow-xl">
          <CardContent>
            <div className="relative mb-6">
              <Newspaper className="h-16 w-16 mx-auto text-purple-400 animate-bounce" />
              <Sparkles className="absolute -top-2 -right-2 h-8 w-8 text-yellow-400 animate-pulse" />
            </div>
            <h3 className="text-2xl font-bold mb-4 bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
              No articles found
            </h3>
            <p className="text-gray-600 text-lg">
              {searchQuery
                ? `🔍 No articles match your search for "${searchQuery}"`
                : `📰 No articles available for the selected filters`}
            </p>
            <p className="text-sm text-gray-500 mt-2">Try adjusting your filters or search terms</p>
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8 text-center">
        <h2 className="text-4xl font-bold mb-4 bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
          {selectedTopic === "All"
            ? "🌟 Latest News"
            : `${selectedTopic === "Technology" ? "💻" : selectedTopic === "World" ? "🌍" : selectedTopic === "Business" ? "💼" : selectedTopic === "Science" ? "🔬" : selectedTopic === "Sports" ? "⚽" : selectedTopic === "Entertainment" ? "🎬" : "🏛️"} ${selectedTopic} News`}
        </h2>
        <div className="flex items-center justify-center gap-2">
          <div className="h-1 w-20 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full"></div>
          <Sparkles className="h-5 w-5 text-yellow-400 animate-spin" />
          <div className="h-1 w-20 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full"></div>
        </div>
        <p className="text-gray-600 mt-4 text-lg">
          ✨ {filteredArticles.length} amazing article{filteredArticles.length !== 1 ? "s" : ""} found
        </p>
      </div>

      <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
        {filteredArticles.map((article) => (
          <NewsCard key={article.id} article={article} />
        ))}
      </div>
    </div>
  )
}
