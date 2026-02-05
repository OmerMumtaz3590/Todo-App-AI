export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24 bg-gradient-to-b from-gray-50 to-white">
      <div className="text-center">
        <h1 className="text-5xl font-bold mb-4 text-gray-900">Todo AI Assistant</h1>
        <p className="text-lg mb-8 text-gray-600 max-w-md mx-auto">
          Manage your tasks with natural language. Just chat with your AI assistant to create, update, and organize todos.
        </p>
        <div className="space-x-4">
          <a
            href="/chat"
            className="px-8 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-lg font-medium transition-colors inline-block"
          >
            Start Chatting
          </a>
          <a
            href="/auth/signin"
            className="px-6 py-3 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 transition-colors inline-block"
          >
            Sign In
          </a>
        </div>
        <div className="mt-12 grid gap-4 text-left max-w-lg mx-auto">
          <div className="flex items-start gap-3 bg-white p-4 rounded-lg shadow-sm border">
            <span className="text-2xl">💬</span>
            <div>
              <h3 className="font-semibold text-gray-800">Natural Language</h3>
              <p className="text-sm text-gray-600">Say &quot;Add a todo: Buy groceries&quot; and it just works</p>
            </div>
          </div>
          <div className="flex items-start gap-3 bg-white p-4 rounded-lg shadow-sm border">
            <span className="text-2xl">📋</span>
            <div>
              <h3 className="font-semibold text-gray-800">Full Todo Management</h3>
              <p className="text-sm text-gray-600">Create, update, complete, and delete tasks through conversation</p>
            </div>
          </div>
          <div className="flex items-start gap-3 bg-white p-4 rounded-lg shadow-sm border">
            <span className="text-2xl">🔄</span>
            <div>
              <h3 className="font-semibold text-gray-800">Conversation History</h3>
              <p className="text-sm text-gray-600">Pick up right where you left off with persistent chat history</p>
            </div>
          </div>
        </div>
        <div className="mt-8">
          <a
            href="/todos"
            className="text-sm text-gray-500 hover:text-gray-700 transition-colors"
          >
            Prefer the classic view? Go to Todos →
          </a>
        </div>
      </div>
    </main>
  );
}
