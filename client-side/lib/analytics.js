// Simple analytics
export const trackEvent = (event, data) => {
  console.log("Event:", event, data)

  // Send to analytics service
  if (typeof window !== "undefined") {
    // Google Analytics, Mixpanel, etc.
  }
}

// Track API errors
export const trackError = (error, context) => {
  console.error("Error:", error, context)

  // Send to error tracking service
  // Sentry, LogRocket, etc.
}
