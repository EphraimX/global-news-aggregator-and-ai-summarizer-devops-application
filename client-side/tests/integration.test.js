// Integration test example
describe("Frontend-Backend Integration", () => {
  test("should fetch articles from backend", async () => {
    const response = await fetch("http://localhost:8000/api/news/articles?limit=5")
    const articles = await response.json()

    expect(response.status).toBe(200)
    expect(Array.isArray(articles)).toBe(true)
    expect(articles.length).toBeGreaterThan(0)
  })

  test("should generate AI summary", async () => {
    const response = await fetch("http://localhost:8000/api/ai/summarize", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        title: "Test Article",
        content: "This is a test article content for summarization.",
      }),
    })

    const result = await response.json()
    expect(response.status).toBe(200)
    expect(result.summary).toBeDefined()
  })
})
