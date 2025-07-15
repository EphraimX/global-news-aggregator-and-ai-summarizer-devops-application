// End-to-End Testing with Playwright
const { test, expect } = require("@playwright/test")

test.describe("Global News Digest AI - E2E Tests", () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to the application
    await page.goto("http://localhost:3000")
  })

  test("should load the homepage successfully", async ({ page }) => {
    // Check if the main title is visible
    await expect(page.locator("h1")).toContainText("Global News Digest")

    // Check if the AI badge is present
    await expect(page.locator("text=Powered by AI")).toBeVisible()
  })

  test("should display news articles", async ({ page }) => {
    // Wait for articles to load
    await page.waitForSelector('[data-testid="news-card"]', { timeout: 10000 })

    // Check if at least one article is displayed
    const articles = page.locator('[data-testid="news-card"]')
    await expect(articles).toHaveCountGreaterThan(0)

    // Check if article has required elements
    const firstArticle = articles.first()
    await expect(firstArticle.locator("h3")).toBeVisible()
    await expect(firstArticle.locator('[data-testid="article-source"]')).toBeVisible()
  })

  test("should filter articles by topic", async ({ page }) => {
    // Wait for articles to load
    await page.waitForSelector('[data-testid="news-card"]')

    // Click on Technology filter
    await page.click("text=Technology")

    // Wait for filtered results
    await page.waitForTimeout(1000)

    // Check if articles are filtered
    const articles = page.locator('[data-testid="news-card"]')
    const count = await articles.count()
    expect(count).toBeGreaterThan(0)
  })

  test("should generate AI summary", async ({ page }) => {
    // Wait for articles to load
    await page.waitForSelector('[data-testid="news-card"]')

    // Click on AI Summary button for first article
    const firstSummaryButton = page.locator('button:has-text("AI Summary")').first()
    await firstSummaryButton.click()

    // Wait for summary to generate
    await page.waitForSelector("text=AI Summary", { timeout: 10000 })

    // Check if summary is displayed
    await expect(page.locator('[data-testid="ai-summary"]')).toBeVisible()
  })

  test("should search for articles", async ({ page }) => {
    // Find search input
    const searchInput = page.locator('input[placeholder*="Search"]')
    await searchInput.fill("technology")

    // Wait for search results
    await page.waitForTimeout(1000)

    // Check if search results are displayed
    const articles = page.locator('[data-testid="news-card"]')
    const count = await articles.count()
    expect(count).toBeGreaterThan(0)
  })

  test("should open article in new tab", async ({ context, page }) => {
    // Wait for articles to load
    await page.waitForSelector('[data-testid="news-card"]')

    // Click on "Read Full" button
    const readFullButton = page.locator('button:has-text("Read Full")').first()

    // Listen for new page
    const pagePromise = context.waitForEvent("page")
    await readFullButton.click()
    const newPage = await pagePromise

    // Check if new page opened
    expect(newPage.url()).not.toBe("http://localhost:3000")
  })

  test("should toggle theme", async ({ page }) => {
    // Find theme toggle button
    const themeButton = page.locator('button[aria-label*="theme"], button:has(svg)')
    await themeButton.click()

    // Check if theme changed (dark mode applied)
    await expect(page.locator("html")).toHaveClass(/dark/)
  })

  test("should handle mobile responsive design", async ({ page }) => {
    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 667 })

    // Check if mobile menu button is visible
    await expect(page.locator('button:has-text("Menu"), button[aria-label*="menu"]')).toBeVisible()

    // Check if articles are still displayed properly
    await page.waitForSelector('[data-testid="news-card"]')
    const articles = page.locator('[data-testid="news-card"]')
    await expect(articles.first()).toBeVisible()
  })
})

// Performance tests
test.describe("Performance Tests", () => {
  test("should load within acceptable time", async ({ page }) => {
    const startTime = Date.now()

    await page.goto("http://localhost:3000")
    await page.waitForSelector('[data-testid="news-card"]')

    const loadTime = Date.now() - startTime
    expect(loadTime).toBeLessThan(5000) // Should load within 5 seconds
  })

  test("should handle API errors gracefully", async ({ page }) => {
    // Mock API to return error
    await page.route("**/api/news/articles*", (route) => {
      route.fulfill({
        status: 500,
        contentType: "application/json",
        body: JSON.stringify({ error: "Internal Server Error" }),
      })
    })

    await page.goto("http://localhost:3000")

    // Check if error message is displayed
    await expect(page.locator("text=Something went wrong")).toBeVisible()

    // Check if retry button is present
    await expect(page.locator('button:has-text("Try Again")')).toBeVisible()
  })
})
