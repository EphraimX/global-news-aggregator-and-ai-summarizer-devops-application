import { generateText } from "ai"
import { openai } from "@ai-sdk/openai"

export async function POST(request) {
  try {
    const { title, content } = await request.json()

    const { text } = await generateText({
      model: openai("gpt-4o"),
      system:
        "You are a professional news summarizer with a vibrant personality. Create concise, informative summaries that capture the key points of news articles in 1-3 sentences. Focus on the most important facts and implications while maintaining an engaging tone.",
      prompt: `Summarize this exciting news article:

Title: ${title}
Content: ${content}

Provide a clear, concise summary in 1-3 sentences that captures the essential information and significance of this news story. Make it engaging and informative!`,
    })

    return Response.json({ summary: text })
  } catch (error) {
    console.error("Summarization error:", error)
    return Response.json({ error: "Failed to generate summary" }, { status: 500 })
  }
}
