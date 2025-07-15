"use client"

import { useState } from "react"
import { Header } from "@/components/header"
import { NewsFeed } from "@/components/news-feed"
import { Sidebar } from "@/components/sidebar"
import { Footer } from "@/components/footer"
import { NewsProvider } from "@/contexts/news-context"
import { ThemeProvider } from "@/components/theme-provider"

export default function Home() {
  const [sidebarOpen, setSidebarOpen] = useState(false)

  return (
    <ThemeProvider attribute="class" defaultTheme="light">
      <NewsProvider>
        <div className="min-h-screen bg-gradient-to-br from-purple-50 via-blue-50 to-indigo-100 dark:from-gray-900 dark:via-purple-900 dark:to-indigo-900">
          <Header onMenuClick={() => setSidebarOpen(!sidebarOpen)} />

          <div className="flex">
            <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />

            <main className="flex-1 transition-all duration-300">
              <NewsFeed />
            </main>
          </div>

          <Footer />
        </div>
      </NewsProvider>
    </ThemeProvider>
  )
}
