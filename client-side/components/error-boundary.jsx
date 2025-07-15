"use client"

import React from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { AlertTriangle, RefreshCw } from "lucide-react"

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props)
    this.state = { hasError: false, error: null, errorInfo: null }
  }

  static getDerivedStateFromError(error) {
    return { hasError: true }
  }

  componentDidCatch(error, errorInfo) {
    this.setState({
      error: error,
      errorInfo: errorInfo,
    })

    // Log error to monitoring service
    console.error("Error caught by boundary:", error, errorInfo)
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-red-50 to-pink-50 p-4">
          <Card className="max-w-md w-full border-2 border-red-200 shadow-xl">
            <CardHeader className="text-center">
              <div className="mx-auto mb-4 p-3 bg-red-100 rounded-full w-fit">
                <AlertTriangle className="h-8 w-8 text-red-500" />
              </div>
              <CardTitle className="text-2xl font-bold text-red-600">Oops! Something went wrong</CardTitle>
            </CardHeader>
            <CardContent className="text-center space-y-4">
              <p className="text-gray-600">We encountered an unexpected error. Please try refreshing the page.</p>

              {process.env.NODE_ENV === "development" && (
                <details className="text-left bg-gray-100 p-4 rounded-lg text-sm">
                  <summary className="cursor-pointer font-semibold">Error Details</summary>
                  <pre className="mt-2 whitespace-pre-wrap">{this.state.error && this.state.error.toString()}</pre>
                  <pre className="mt-2 whitespace-pre-wrap text-xs">{this.state.errorInfo.componentStack}</pre>
                </details>
              )}

              <Button
                onClick={() => window.location.reload()}
                className="bg-gradient-to-r from-red-500 to-pink-500 hover:from-red-600 hover:to-pink-600"
              >
                <RefreshCw className="h-4 w-4 mr-2" />
                Refresh Page
              </Button>
            </CardContent>
          </Card>
        </div>
      )
    }

    return this.props.children
  }
}

export default ErrorBoundary
