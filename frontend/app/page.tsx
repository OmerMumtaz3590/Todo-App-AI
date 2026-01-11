export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="text-center">
        <h1 className="text-4xl font-bold mb-4">Todo App</h1>
        <p className="text-lg mb-8">Full-stack todo application with authentication</p>
        <div className="space-x-4">
          <a
            href="/auth/signin"
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            Sign In
          </a>
          <a
            href="/auth/signup"
            className="px-6 py-3 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300"
          >
            Sign Up
          </a>
        </div>
      </div>
    </main>
  );
}
