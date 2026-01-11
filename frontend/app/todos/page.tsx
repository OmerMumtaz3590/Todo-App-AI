'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { todoService } from '@/services/todoService';
import { authService } from '@/services/authService';
import { APIError } from '@/lib/api';
import type { Todo } from '@/types/todo';

export default function TodosPage() {
  const router = useRouter();
  const [todos, setTodos] = useState<Todo[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [newTitle, setNewTitle] = useState('');
  const [newDescription, setNewDescription] = useState('');
  const [isCreating, setIsCreating] = useState(false);
  const [editingTodoId, setEditingTodoId] = useState<string | null>(null);
  const [editTitle, setEditTitle] = useState('');
  const [editDescription, setEditDescription] = useState('');
  const [isUpdating, setIsUpdating] = useState(false);
  const [deletingTodoId, setDeletingTodoId] = useState<string | null>(null);
  const [togglingTodoId, setTogglingTodoId] = useState<string | null>(null);

  useEffect(() => {
    loadTodos();
  }, []);

  const loadTodos = async () => {
    try {
      setIsLoading(true);
      setError('');
      const fetchedTodos = await todoService.getTodos();
      setTodos(fetchedTodos);
    } catch (err) {
      if (err instanceof APIError && err.status === 401) {
        // Not authenticated, redirect to signin
        router.push('/auth/signin');
      } else {
        setError('Failed to load todos. Please try again.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleSignout = async () => {
    try {
      await authService.signout();
      router.push('/auth/signin');
    } catch (err) {
      console.error('Signout failed:', err);
      // Still redirect even if API call fails
      router.push('/auth/signin');
    }
  };

  const handleCreateTodo = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!newTitle.trim()) {
      setError('Title is required');
      return;
    }

    if (newTitle.length > 500) {
      setError('Title must be 500 characters or less');
      return;
    }

    setIsCreating(true);
    setError('');

    try {
      const createdTodo = await todoService.createTodo(
        newTitle.trim(),
        newDescription.trim() || null
      );
      setTodos([createdTodo, ...todos]);
      setNewTitle('');
      setNewDescription('');
      setShowCreateForm(false);
    } catch (err) {
      if (err instanceof APIError) {
        if (err.status === 401) {
          router.push('/auth/signin');
        } else {
          setError(err.message || 'Failed to create todo');
        }
      } else {
        setError('An unexpected error occurred');
      }
    } finally {
      setIsCreating(false);
    }
  };

  const handleEditClick = (todo: Todo) => {
    setEditingTodoId(todo.id);
    setEditTitle(todo.title);
    setEditDescription(todo.description || '');
    setError('');
  };

  const handleUpdateTodo = async (e: React.FormEvent, todoId: string) => {
    e.preventDefault();

    if (!editTitle.trim()) {
      setError('Title is required');
      return;
    }

    if (editTitle.length > 500) {
      setError('Title must be 500 characters or less');
      return;
    }

    setIsUpdating(true);
    setError('');

    try {
      const updatedTodo = await todoService.updateTodo(
        todoId,
        editTitle.trim(),
        editDescription.trim() || null
      );
      setTodos(todos.map((t) => (t.id === todoId ? updatedTodo : t)));
      setEditingTodoId(null);
      setEditTitle('');
      setEditDescription('');
    } catch (err) {
      if (err instanceof APIError) {
        if (err.status === 401) {
          router.push('/auth/signin');
        } else if (err.status === 404) {
          setError('Todo not found');
        } else {
          setError(err.message || 'Failed to update todo');
        }
      } else {
        setError('An unexpected error occurred');
      }
    } finally {
      setIsUpdating(false);
    }
  };

  const handleCancelEdit = () => {
    setEditingTodoId(null);
    setEditTitle('');
    setEditDescription('');
    setError('');
  };

  const handleToggleCompletion = async (todoId: string) => {
    setTogglingTodoId(todoId);
    setError('');

    try {
      const updatedTodo = await todoService.toggleCompletion(todoId);
      setTodos(todos.map((t) => (t.id === todoId ? updatedTodo : t)));
    } catch (err) {
      if (err instanceof APIError) {
        if (err.status === 401) {
          router.push('/auth/signin');
        } else if (err.status === 404) {
          setError('Todo not found');
        } else {
          setError(err.message || 'Failed to toggle todo');
        }
      } else {
        setError('An unexpected error occurred');
      }
    } finally {
      setTogglingTodoId(null);
    }
  };

  const handleDeleteTodo = async (todoId: string) => {
    if (!confirm('Are you sure you want to delete this todo?')) {
      return;
    }

    setDeletingTodoId(todoId);
    setError('');

    try {
      await todoService.deleteTodo(todoId);
      setTodos(todos.filter((t) => t.id !== todoId));
    } catch (err) {
      if (err instanceof APIError) {
        if (err.status === 401) {
          router.push('/auth/signin');
        } else if (err.status === 404) {
          setError('Todo not found');
        } else {
          setError(err.message || 'Failed to delete todo');
        }
      } else {
        setError('An unexpected error occurred');
      }
    } finally {
      setDeletingTodoId(null);
    }
  };

  if (isLoading) {
    return (
      <main className="flex min-h-screen flex-col items-center justify-center p-6 bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading todos...</p>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto p-6">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">My Todos</h1>
            <p className="text-gray-600 mt-1">Manage your tasks</p>
          </div>
          <button
            onClick={handleSignout}
            className="px-4 py-2 text-sm text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50"
          >
            Sign Out
          </button>
        </div>

        {/* Error Message */}
        {error && (
          <div className="mb-6 p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg">
            {error}
          </div>
        )}

        {/* Create Todo Form */}
        {!showCreateForm && todos.length > 0 && (
          <div className="mb-6">
            <button
              onClick={() => setShowCreateForm(true)}
              className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-semibold"
            >
              + Add Todo
            </button>
          </div>
        )}

        {showCreateForm && (
          <div className="mb-6 bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">
              Create New Todo
            </h2>
            <form onSubmit={handleCreateTodo}>
              <div className="mb-4">
                <label
                  htmlFor="title"
                  className="block text-gray-700 text-sm font-bold mb-2"
                >
                  Title *
                </label>
                <input
                  type="text"
                  id="title"
                  value={newTitle}
                  onChange={(e) => setNewTitle(e.target.value)}
                  className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="What needs to be done?"
                  disabled={isCreating}
                  maxLength={500}
                  required
                />
                <p className="text-gray-500 text-xs mt-1">
                  {newTitle.length}/500 characters
                </p>
              </div>

              <div className="mb-4">
                <label
                  htmlFor="description"
                  className="block text-gray-700 text-sm font-bold mb-2"
                >
                  Description (optional)
                </label>
                <textarea
                  id="description"
                  value={newDescription}
                  onChange={(e) => setNewDescription(e.target.value)}
                  className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Add more details..."
                  rows={3}
                  disabled={isCreating}
                />
              </div>

              <div className="flex gap-3">
                <button
                  type="submit"
                  disabled={isCreating}
                  className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-semibold disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isCreating ? 'Creating...' : 'Create Todo'}
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setShowCreateForm(false);
                    setNewTitle('');
                    setNewDescription('');
                    setError('');
                  }}
                  disabled={isCreating}
                  className="px-6 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 font-semibold disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        )}

        {/* Empty State */}
        {todos.length === 0 && (
          <div className="bg-white rounded-lg shadow-md p-12 text-center">
            <div className="text-gray-400 mb-4">
              <svg
                className="mx-auto h-16 w-16"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
                />
              </svg>
            </div>
            <h2 className="text-xl font-semibold text-gray-700 mb-2">
              No todos yet
            </h2>
            <p className="text-gray-500 mb-6">
              Create your first todo to get started!
            </p>
            <button
              onClick={() => setShowCreateForm(true)}
              className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-semibold"
            >
              Create Todo
            </button>
          </div>
        )}

        {/* Todo List */}
        {todos.length > 0 && (
          <div className="space-y-3">
            {todos.map((todo) => (
              <div
                key={todo.id}
                className="bg-white rounded-lg shadow-sm p-4 border border-gray-200 hover:shadow-md transition-shadow"
              >
                {editingTodoId === todo.id ? (
                  /* Edit Mode */
                  <form onSubmit={(e) => handleUpdateTodo(e, todo.id)}>
                    <div className="mb-3">
                      <label
                        htmlFor={`edit-title-${todo.id}`}
                        className="block text-gray-700 text-sm font-bold mb-2"
                      >
                        Title *
                      </label>
                      <input
                        type="text"
                        id={`edit-title-${todo.id}`}
                        value={editTitle}
                        onChange={(e) => setEditTitle(e.target.value)}
                        className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500"
                        disabled={isUpdating}
                        maxLength={500}
                        required
                      />
                      <p className="text-gray-500 text-xs mt-1">
                        {editTitle.length}/500 characters
                      </p>
                    </div>

                    <div className="mb-3">
                      <label
                        htmlFor={`edit-description-${todo.id}`}
                        className="block text-gray-700 text-sm font-bold mb-2"
                      >
                        Description (optional)
                      </label>
                      <textarea
                        id={`edit-description-${todo.id}`}
                        value={editDescription}
                        onChange={(e) => setEditDescription(e.target.value)}
                        className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:ring-2 focus:ring-blue-500"
                        rows={3}
                        disabled={isUpdating}
                      />
                    </div>

                    <div className="flex gap-2">
                      <button
                        type="submit"
                        disabled={isUpdating}
                        className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm font-semibold disabled:opacity-50 disabled:cursor-not-allowed"
                      >
                        {isUpdating ? 'Saving...' : 'Save'}
                      </button>
                      <button
                        type="button"
                        onClick={handleCancelEdit}
                        disabled={isUpdating}
                        className="px-4 py-2 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 text-sm font-semibold disabled:opacity-50 disabled:cursor-not-allowed"
                      >
                        Cancel
                      </button>
                    </div>
                  </form>
                ) : (
                  /* View Mode */
                  <div className="flex items-start gap-3">
                    {/* Completion Checkbox */}
                    <div className="flex-shrink-0 mt-1">
                      <input
                        type="checkbox"
                        checked={todo.is_completed}
                        onChange={() => handleToggleCompletion(todo.id)}
                        disabled={togglingTodoId === todo.id}
                        className="w-5 h-5 text-blue-600 rounded border-gray-300 focus:ring-blue-500 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
                      />
                    </div>

                    {/* Todo Content */}
                    <div className="flex-grow min-w-0">
                      <h3
                        className={`text-lg font-medium ${
                          todo.is_completed
                            ? 'text-gray-400 line-through'
                            : 'text-gray-900'
                        }`}
                      >
                        {todo.title}
                      </h3>
                      {todo.description && (
                        <p
                          className={`mt-1 text-sm ${
                            todo.is_completed
                              ? 'text-gray-400 line-through'
                              : 'text-gray-600'
                          }`}
                        >
                          {todo.description}
                        </p>
                      )}
                      <div className="mt-2 flex items-center gap-4 text-xs text-gray-500">
                        <span>
                          Created:{' '}
                          {new Date(todo.created_at).toLocaleDateString()}
                        </span>
                        {todo.updated_at !== todo.created_at && (
                          <span>
                            Updated:{' '}
                            {new Date(todo.updated_at).toLocaleDateString()}
                          </span>
                        )}
                      </div>
                    </div>

                    {/* Action Buttons */}
                    <div className="flex-shrink-0 flex gap-2">
                      <button
                        onClick={() => handleEditClick(todo)}
                        className="px-3 py-1 text-sm text-blue-600 hover:bg-blue-50 rounded disabled:opacity-50"
                        title="Edit"
                        disabled={deletingTodoId === todo.id}
                      >
                        Edit
                      </button>
                      <button
                        onClick={() => handleDeleteTodo(todo.id)}
                        disabled={deletingTodoId === todo.id}
                        className="px-3 py-1 text-sm text-red-600 hover:bg-red-50 rounded disabled:opacity-50 disabled:cursor-not-allowed"
                        title="Delete"
                      >
                        {deletingTodoId === todo.id ? 'Deleting...' : 'Delete'}
                      </button>
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </main>
  );
}
