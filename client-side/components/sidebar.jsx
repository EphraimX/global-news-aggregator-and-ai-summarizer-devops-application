"use client"

import { X, Calendar, Tag, Building, TrendingUp, FlameIcon as Fire, Zap } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { useNews } from "@/contexts/news-context"

const topics = ["All", "World", "Politics", "Technology", "Business", "Science", "Entertainment", "Sports"]
const sources = ["All", "TechCrunch", "Reuters", "Bloomberg", "NASA News", "ESPN", "Variety"]
const dateRanges = ["Today", "Last 7 days", "Last 30 days"]

const topicColors = {
  World: "bg-gradient-to-r from-green-400 to-emerald-500 text-white",
  Politics: "bg-gradient-to-r from-gray-400 to-slate-500 text-white",
  Technology: "bg-gradient-to-r from-blue-400 to-cyan-500 text-white",
  Business: "bg-gradient-to-r from-purple-400 to-pink-500 text-white",
  Science: "bg-gradient-to-r from-orange-400 to-red-500 text-white",
  Entertainment: "bg-gradient-to-r from-pink-400 to-rose-500 text-white",
  Sports: "bg-gradient-to-r from-red-400 to-orange-500 text-white",
}

export function Sidebar({ isOpen, onClose }) {
  const {
    selectedTopic,
    setSelectedTopic,
    selectedSource,
    setSelectedSource,
    dateRange,
    setDateRange,
    filteredArticles,
  } = useNews()

  const topicCounts = topics.slice(1).reduce((acc, topic) => {
    acc[topic] = filteredArticles.filter((article) => article.topic === topic).length
    return acc
  }, {})

  return (
    <>
      {/* Mobile overlay */}
      {isOpen && <div className="fixed inset-0 bg-black/50 z-40 md:hidden backdrop-blur-sm" onClick={onClose} />}

      {/* Sidebar */}
      <aside
        className={`
        fixed md:sticky top-20 left-0 z-50 h-[calc(100vh-5rem)] w-80 
        transform transition-all duration-500 ease-out
        bg-gradient-to-b from-white/95 to-purple-50/95 dark:from-gray-900/95 dark:to-purple-900/95 
        backdrop-blur-xl border-r border-purple-200 dark:border-purple-800 overflow-y-auto
        shadow-2xl shadow-purple-500/20
        ${isOpen ? "translate-x-0" : "-translate-x-full md:translate-x-0"}
      `}
      >
        <div className="p-6 space-y-6">
          <div className="flex items-center justify-between md:hidden">
            <h2 className="text-xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
              🎛️ Filters
            </h2>
            <Button
              variant="ghost"
              size="icon"
              onClick={onClose}
              className="hover:bg-gradient-to-r hover:from-red-400 hover:to-pink-500 hover:text-white transition-all duration-300 rounded-full"
            >
              <X className="h-5 w-5" />
            </Button>
          </div>

          <Card className="border-2 border-purple-200 bg-gradient-to-br from-white/80 to-purple-50/80 backdrop-blur-sm shadow-lg hover:shadow-xl transition-all duration-300">
            <CardHeader className="pb-3">
              <CardTitle className="flex items-center gap-2 text-lg bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
                <Tag className="h-5 w-5 text-purple-500" />📂 Topics
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <Select value={selectedTopic} onValueChange={setSelectedTopic}>
                <SelectTrigger className="border-2 border-purple-200 hover:border-purple-400 bg-white/50 transition-all duration-300">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent className="bg-white/95 backdrop-blur-xl">
                  {topics.map((topic) => (
                    <SelectItem key={topic} value={topic}>
                      {topic === "All" ? "🌟 All Topics" : topic}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>

              <div className="grid grid-cols-1 gap-3 mt-4">
                {Object.entries(topicCounts).map(([topic, count]) => (
                  <Badge
                    key={topic}
                    className={`
                      justify-between cursor-pointer p-3 text-sm font-medium transition-all duration-300 hover:scale-105 hover:shadow-lg
                      ${
                        selectedTopic === topic
                          ? topicColors[topic] || "bg-gradient-to-r from-purple-500 to-pink-500 text-white"
                          : "bg-white/70 text-gray-700 hover:bg-gradient-to-r hover:from-purple-100 hover:to-pink-100 border-2 border-purple-200"
                      }
                    `}
                    onClick={() => setSelectedTopic(topic)}
                  >
                    <span className="flex items-center gap-2">
                      {topic === "Technology" && "💻"}
                      {topic === "World" && "🌍"}
                      {topic === "Business" && "💼"}
                      {topic === "Science" && "🔬"}
                      {topic === "Sports" && "⚽"}
                      {topic === "Entertainment" && "🎬"}
                      {topic === "Politics" && "🏛️"}
                      {topic}
                    </span>
                    <span className="bg-white/30 px-2 py-1 rounded-full text-xs font-bold">{count}</span>
                  </Badge>
                ))}
              </div>
            </CardContent>
          </Card>

          <Card className="border-2 border-blue-200 bg-gradient-to-br from-white/80 to-blue-50/80 backdrop-blur-sm shadow-lg hover:shadow-xl transition-all duration-300">
            <CardHeader className="pb-3">
              <CardTitle className="flex items-center gap-2 text-lg bg-gradient-to-r from-blue-600 to-cyan-600 bg-clip-text text-transparent">
                <Building className="h-5 w-5 text-blue-500" />📰 Sources
              </CardTitle>
            </CardHeader>
            <CardContent>
              <Select value={selectedSource} onValueChange={setSelectedSource}>
                <SelectTrigger className="border-2 border-blue-200 hover:border-blue-400 bg-white/50 transition-all duration-300">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent className="bg-white/95 backdrop-blur-xl">
                  {sources.map((source) => (
                    <SelectItem key={source} value={source}>
                      {source === "All" ? "🌟 All Sources" : source}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </CardContent>
          </Card>

          <Card className="border-2 border-green-200 bg-gradient-to-br from-white/80 to-green-50/80 backdrop-blur-sm shadow-lg hover:shadow-xl transition-all duration-300">
            <CardHeader className="pb-3">
              <CardTitle className="flex items-center gap-2 text-lg bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent">
                <Calendar className="h-5 w-5 text-green-500" />📅 Date Range
              </CardTitle>
            </CardHeader>
            <CardContent>
              <Select value={dateRange} onValueChange={setDateRange}>
                <SelectTrigger className="border-2 border-green-200 hover:border-green-400 bg-white/50 transition-all duration-300">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent className="bg-white/95 backdrop-blur-xl">
                  {dateRanges.map((range) => (
                    <SelectItem key={range} value={range}>
                      {range === "Today" && "📅 "}
                      {range === "Last 7 days" && "📊 "}
                      {range === "Last 30 days" && "📈 "}
                      {range}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </CardContent>
          </Card>

          <Card className="border-2 border-orange-200 bg-gradient-to-br from-white/80 to-orange-50/80 backdrop-blur-sm shadow-lg hover:shadow-xl transition-all duration-300">
            <CardHeader className="pb-3">
              <CardTitle className="flex items-center gap-2 text-lg bg-gradient-to-r from-orange-600 to-red-600 bg-clip-text text-transparent">
                <TrendingUp className="h-5 w-5 text-orange-500" />🔥 Trending Now
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="flex items-center justify-between p-3 bg-gradient-to-r from-red-100 to-orange-100 rounded-lg hover:from-red-200 hover:to-orange-200 transition-all duration-300 cursor-pointer">
                  <span className="text-sm font-medium">🤖 AI & Technology</span>
                  <Badge className="bg-gradient-to-r from-red-500 to-orange-500 text-white animate-pulse">
                    <Fire className="h-3 w-3 mr-1" />
                    Hot
                  </Badge>
                </div>
                <div className="flex items-center justify-between p-3 bg-gradient-to-r from-green-100 to-emerald-100 rounded-lg hover:from-green-200 hover:to-emerald-200 transition-all duration-300 cursor-pointer">
                  <span className="text-sm font-medium">🌱 Climate Change</span>
                  <Badge className="bg-gradient-to-r from-green-500 to-emerald-500 text-white">
                    <TrendingUp className="h-3 w-3 mr-1" />
                    Trending
                  </Badge>
                </div>
                <div className="flex items-center justify-between p-3 bg-gradient-to-r from-purple-100 to-pink-100 rounded-lg hover:from-purple-200 hover:to-pink-200 transition-all duration-300 cursor-pointer">
                  <span className="text-sm font-medium">🚀 Space Exploration</span>
                  <Badge className="bg-gradient-to-r from-purple-500 to-pink-500 text-white">
                    <Zap className="h-3 w-3 mr-1" />
                    Rising
                  </Badge>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </aside>
    </>
  )
}
