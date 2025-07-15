"use client"

import { useState, useEffect } from "react"
import { ExternalLink, Clock, Sparkles, FileText, Loader2, Heart, Share2, Bookmark, Eye } from "lucide-react"
import { Card, CardContent, CardFooter, CardHeader } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { useNews } from "@/contexts/news-context"

const topicColors = {
  Technology: "bg-gradient-to-r from-blue-500 to-cyan-500",
  World: "bg-gradient-to-r from-green-500 to-emerald-500",
  Business: "bg-gradient-to-r from-purple-500 to-pink-500",
  Science: "bg-gradient-to-r from-orange-500 to-red-500",
  Sports: "bg-gradient-to-r from-red-500 to-orange-500",
  Entertainment: "bg-gradient-to-r from-pink-500 to-rose-500",
  Politics: "bg-gradient-to-r from-gray-500 to-slate-600",
}

export function NewsCard({ article }) {
  const [showSummary, setShowSummary] = useState(false)
  const [isLiked, setIsLiked] = useState(false)
  const [isBookmarked, setIsBookmarked] = useState(false)
  const [hasViewed, setHasViewed] = useState(false)
  const { toggleSummaryView, trackView, toggleLike } = useNews()

  // Track view when card is visible
  useEffect(() => {
    if (!hasViewed) {
      const timer = setTimeout(() => {
        trackView(article.id)
        setHasViewed(true)
      }, 2000) // Track view after 2 seconds

      return () => clearTimeout(timer)
    }
  }, [article.id, hasViewed, trackView])

  const formatTimeAgo = (dateString) => {
    const date = new Date(dateString)
    const now = new Date()
    const diffInHours = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60))

    if (diffInHours < 1) return "Just now"
    if (diffInHours < 24) return `${diffInHours}h ago`
    return `${Math.floor(diffInHours / 24)}d ago`
  }

  const handleSummaryToggle = () => {
    if (!showSummary && !article.summary) {
      toggleSummaryView(article.id)
    }
    setShowSummary(!showSummary)
  }

  const handleLike = async () => {
    if (!isLiked) {
      await toggleLike(article.id)
      setIsLiked(true)
    }
  }

  const handleShare = async () => {
    if (navigator.share) {
      try {
        await navigator.share({
          title: article.title,
          text: article.originalExcerpt,
          url: article.url,
        })
      } catch (err) {
        console.log("Error sharing:", err)
      }
    } else {
      // Fallback to clipboard
      navigator.clipboard.writeText(article.url)
    }
  }

  return (
    <Card className="h-full flex flex-col hover:shadow-2xl hover:shadow-purple-500/25 transition-all duration-500 hover:scale-105 bg-gradient-to-br from-white/90 to-purple-50/50 backdrop-blur-sm border-2 border-purple-200 hover:border-purple-400 group overflow-hidden">
      {article.imageUrl && (
        <div className="aspect-video overflow-hidden rounded-t-lg relative">
          <img
            src={article.imageUrl || "/placeholder.svg"}
            alt={article.title}
            className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
          <div className="absolute top-4 right-4 flex gap-2">
            <Button
              size="sm"
              variant="ghost"
              className="bg-white/20 backdrop-blur-sm hover:bg-white/40 text-white rounded-full p-2 opacity-0 group-hover:opacity-100 transition-all duration-300"
              onClick={() => setIsBookmarked(!isBookmarked)}
            >
              <Bookmark className={`h-4 w-4 ${isBookmarked ? "fill-current" : ""}`} />
            </Button>
            <Button
              size="sm"
              variant="ghost"
              className="bg-white/20 backdrop-blur-sm hover:bg-white/40 text-white rounded-full p-2 opacity-0 group-hover:opacity-100 transition-all duration-300"
              onClick={handleShare}
            >
              <Share2 className="h-4 w-4" />
            </Button>
          </div>
        </div>
      )}

      <CardHeader className="pb-3">
        <div className="flex items-center justify-between mb-3">
          <div
            className={`flex items-center gap-2 px-3 py-1 rounded-full ${article.source.color || "bg-gradient-to-r from-blue-500 to-purple-500"} text-white shadow-lg`}
          >
            <span className="text-lg">{article.source.favicon}</span>
            <span className="text-sm font-bold">{article.source.name}</span>
          </div>
          <div className="flex items-center gap-2 bg-white/70 backdrop-blur-sm px-3 py-1 rounded-full">
            <Clock className="h-3 w-3 text-purple-500" />
            <span className="text-xs font-medium text-purple-700">{formatTimeAgo(article.publishedAt)}</span>
          </div>
        </div>

        <h3 className="font-bold text-lg leading-tight line-clamp-2 hover:text-purple-600 cursor-pointer transition-colors duration-300 group-hover:text-purple-700">
          {article.title}
        </h3>

        <Badge
          className={`w-fit text-white font-bold px-3 py-1 shadow-lg ${topicColors[article.topic] || "bg-gradient-to-r from-purple-500 to-pink-500"}`}
        >
          {article.topic === "Technology" && "💻 "}
          {article.topic === "World" && "🌍 "}
          {article.topic === "Business" && "💼 "}
          {article.topic === "Science" && "🔬 "}
          {article.topic === "Sports" && "⚽ "}
          {article.topic === "Entertainment" && "🎬 "}
          {article.topic === "Politics" && "🏛️ "}
          {article.topic}
        </Badge>
      </CardHeader>

      <CardContent className="flex-1">
        <div className="space-y-4">
          {showSummary && article.summary ? (
            <div className="p-4 bg-gradient-to-r from-purple-100 to-pink-100 rounded-xl border-l-4 border-purple-500 shadow-inner">
              <div className="flex items-center gap-2 mb-3">
                <Sparkles className="h-5 w-5 text-purple-600 animate-pulse" />
                <span className="text-sm font-bold text-purple-700">✨ AI Summary</span>
              </div>
              <p className="text-sm leading-relaxed text-gray-700 font-medium">{article.summary}</p>
            </div>
          ) : showSummary && article.isLoadingSummary ? (
            <div className="p-4 bg-gradient-to-r from-blue-100 to-purple-100 rounded-xl border-l-4 border-blue-500 shadow-inner">
              <div className="flex items-center gap-2">
                <Loader2 className="h-5 w-5 text-blue-600 animate-spin" />
                <span className="text-sm font-bold text-blue-700">🤖 Generating summary...</span>
              </div>
            </div>
          ) : (
            <div className="p-4 bg-gradient-to-r from-gray-50 to-blue-50 rounded-xl border-l-4 border-gray-400 shadow-inner">
              <div className="flex items-center gap-2 mb-3">
                <FileText className="h-5 w-5 text-gray-600" />
                <span className="text-sm font-bold text-gray-700">📄 Original Excerpt</span>
              </div>
              <p className="text-sm leading-relaxed text-gray-600">{article.originalExcerpt}</p>
            </div>
          )}
        </div>
      </CardContent>

      <CardFooter className="pt-4 space-y-3">
        <div className="flex items-center justify-between w-full">
          <Button
            size="sm"
            variant="ghost"
            onClick={handleLike}
            className={`flex items-center gap-2 transition-all duration-300 ${
              isLiked
                ? "text-red-500 hover:text-red-600 bg-red-50 hover:bg-red-100"
                : "text-gray-500 hover:text-red-500 hover:bg-red-50"
            }`}
          >
            <Heart className={`h-4 w-4 ${isLiked ? "fill-current animate-pulse" : ""}`} />
            <span className="text-xs font-medium">{article.likeCount + (isLiked ? 1 : 0)}</span>
          </Button>

          <div className="flex items-center gap-2 text-xs text-gray-500 font-medium">
            <Eye className="h-3 w-3" />
            <span>{article.viewCount} views</span>
          </div>
        </div>

        <div className="flex gap-2 w-full">
          <Button
            variant="outline"
            size="sm"
            onClick={handleSummaryToggle}
            className="flex-1 bg-gradient-to-r from-purple-50 to-pink-50 hover:from-purple-100 hover:to-pink-100 border-2 border-purple-200 hover:border-purple-400 transition-all duration-300 hover:scale-105"
            disabled={article.isLoadingSummary}
          >
            {showSummary ? (
              <>
                <FileText className="h-4 w-4 mr-2" />📄 Original
              </>
            ) : (
              <>
                <Sparkles className="h-4 w-4 mr-2" />✨ AI Summary
              </>
            )}
          </Button>

          <Button
            size="sm"
            onClick={() => window.open(article.url, "_blank")}
            className="flex-1 bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105"
          >
            <ExternalLink className="h-4 w-4 mr-2" />🔗 Read Full
          </Button>
        </div>
      </CardFooter>
    </Card>
  )
}
