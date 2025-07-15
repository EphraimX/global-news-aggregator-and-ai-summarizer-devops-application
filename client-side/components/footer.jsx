export function Footer() {
  return (
    <footer className="border-t-2 border-purple-200 bg-gradient-to-r from-purple-50 via-pink-50 to-blue-50 dark:from-gray-900 dark:via-purple-900 dark:to-indigo-900">
      <div className="container mx-auto px-4 py-12">
        <div className="grid gap-8 md:grid-cols-3">
          <div className="text-center md:text-left">
            <h3 className="font-bold text-xl mb-4 bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
              🌟 Global News Digest AI
            </h3>
            <p className="text-gray-600 leading-relaxed">
              Stay informed with AI-powered news summaries from around the world. Experience the future of news
              consumption! ✨
            </p>
            <div className="flex justify-center md:justify-start gap-4 mt-4">
              <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center text-white font-bold cursor-pointer hover:scale-110 transition-transform">
                📘
              </div>
              <div className="w-8 h-8 bg-gradient-to-r from-pink-500 to-red-500 rounded-full flex items-center justify-center text-white font-bold cursor-pointer hover:scale-110 transition-transform">
                📷
              </div>
              <div className="w-8 h-8 bg-gradient-to-r from-blue-400 to-cyan-500 rounded-full flex items-center justify-center text-white font-bold cursor-pointer hover:scale-110 transition-transform">
                🐦
              </div>
            </div>
          </div>

          <div className="text-center">
            <h4 className="font-bold text-lg mb-4 bg-gradient-to-r from-blue-600 to-cyan-600 bg-clip-text text-transparent">
              🚀 Features
            </h4>
            <ul className="space-y-3 text-gray-600">
              <li className="hover:text-purple-600 cursor-pointer transition-colors">🤖 AI-Generated Summaries</li>
              <li className="hover:text-purple-600 cursor-pointer transition-colors">🌍 Global News Coverage</li>
              <li className="hover:text-purple-600 cursor-pointer transition-colors">⚡ Real-time Updates</li>
              <li className="hover:text-purple-600 cursor-pointer transition-colors">📊 Topic Categorization</li>
            </ul>
          </div>

          <div className="text-center md:text-right">
            <h4 className="font-bold text-lg mb-4 bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent">
              📋 About
            </h4>
            <ul className="space-y-3 text-gray-600">
              <li className="hover:text-purple-600 cursor-pointer transition-colors">🔒 Privacy Policy</li>
              <li className="hover:text-purple-600 cursor-pointer transition-colors">📜 Terms of Service</li>
              <li className="hover:text-purple-600 cursor-pointer transition-colors">📧 Contact Us</li>
              <li className="hover:text-purple-600 cursor-pointer transition-colors">📚 API Documentation</li>
            </ul>
          </div>
        </div>

        <div className="border-t-2 border-purple-200 mt-8 pt-8 text-center">
          <div className="bg-gradient-to-r from-purple-100 to-pink-100 rounded-full px-6 py-3 inline-block mb-4">
            <p className="text-purple-700 font-bold">✨ Powered by OpenAI Summarizer • 🚀 Built with Love</p>
          </div>
          <p className="text-gray-500 text-sm">© 2024 Global News Digest AI • Making news consumption magical! 🎭</p>
        </div>
      </div>
    </footer>
  )
}
