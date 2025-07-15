"use client"
import { Search, Menu, Globe, Sun, Moon, Sparkles } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { useTheme } from "next-themes"
import { useNews } from "@/contexts/news-context"

export function Header({ onMenuClick }) {
  const { theme, setTheme } = useTheme()
  const { selectedRegion, setSelectedRegion, searchQuery, setSearchQuery } = useNews()

  return (
    <header className="sticky top-0 z-50 w-full backdrop-blur-xl bg-white/80 dark:bg-gray-900/80 border-b border-purple-200 dark:border-purple-800 shadow-lg shadow-purple-500/10">
      <div className="container mx-auto px-4">
        <div className="flex h-20 items-center justify-between">
          <div className="flex items-center gap-4">
            <Button
              variant="ghost"
              size="icon"
              className="md:hidden hover:bg-gradient-to-r hover:from-purple-500 hover:to-pink-500 hover:text-white transition-all duration-300"
              onClick={onMenuClick}
            >
              <Menu className="h-5 w-5" />
            </Button>

            <div className="flex items-center gap-3">
              <div className="relative">
                <Globe className="h-8 w-8 text-transparent bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 bg-clip-text animate-pulse" />
                <Sparkles className="absolute -top-1 -right-1 h-4 w-4 text-yellow-400 animate-bounce" />
              </div>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
                  Global News Digest
                </h1>
                <p className="text-xs bg-gradient-to-r from-purple-500 to-pink-500 bg-clip-text text-transparent font-semibold">
                  ✨ Powered by AI
                </p>
              </div>
            </div>
          </div>

          <div className="flex items-center gap-4">
            <div className="hidden md:flex items-center gap-2">
              <div className="relative group">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-purple-400 group-focus-within:text-purple-600 transition-colors" />
                <Input
                  placeholder="🔍 Search amazing news..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-10 w-72 border-2 border-purple-200 focus:border-purple-500 bg-white/50 backdrop-blur-sm hover:bg-white/70 transition-all duration-300 rounded-full"
                />
              </div>
            </div>

            <Select value={selectedRegion} onValueChange={setSelectedRegion}>
              <SelectTrigger className="w-36 border-2 border-blue-200 hover:border-blue-400 bg-gradient-to-r from-blue-50 to-purple-50 hover:from-blue-100 hover:to-purple-100 transition-all duration-300 rounded-full">
                <SelectValue />
              </SelectTrigger>
              <SelectContent className="bg-white/95 backdrop-blur-xl border-purple-200">
                <SelectItem value="Global">🌍 Global</SelectItem>
                <SelectItem value="US">🇺🇸 US</SelectItem>
                <SelectItem value="EU">🇪🇺 EU</SelectItem>
                <SelectItem value="Asia">🌏 Asia</SelectItem>
                <SelectItem value="Africa">🌍 Africa</SelectItem>
              </SelectContent>
            </Select>

            <Button
              variant="ghost"
              size="icon"
              onClick={() => setTheme(theme === "light" ? "dark" : "light")}
              className="relative overflow-hidden bg-gradient-to-r from-yellow-400 to-orange-500 hover:from-yellow-500 hover:to-orange-600 text-white rounded-full transition-all duration-300 hover:scale-110"
            >
              <Sun className="h-5 w-5 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
              <Moon className="absolute h-5 w-5 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
            </Button>
          </div>
        </div>

        <div className="md:hidden pb-4">
          <div className="relative group">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-purple-400 group-focus-within:text-purple-600 transition-colors" />
            <Input
              placeholder="🔍 Search amazing news..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10 border-2 border-purple-200 focus:border-purple-500 bg-white/50 backdrop-blur-sm rounded-full"
            />
          </div>
        </div>
      </div>
    </header>
  )
}
