/**
 * Todo service for frontend API calls.
 */
import { api } from '@/lib/api';
import type {
  Todo,
  TodoListResponse,
  CreateTodoRequest,
  UpdateTodoRequest,
  ToggleCompletionResponse,
} from '@/types/todo';
import type { MessageResponse } from '@/types/auth';

export const todoService = {
  /**
   * Get all todos for the authenticated user.
   * @returns List of todos
   * @throws APIError with status 401 if not authenticated
   */
  async getTodos(): Promise<Todo[]> {
    const response = await api.get<TodoListResponse>('/todos');
    return response.todos;
  },

  /**
   * Create a new todo.
   * @param title - Todo title (1-500 characters)
   * @param description - Optional todo description
   * @returns Created todo
   * @throws APIError with status 400 if validation fails
   * @throws APIError with status 401 if not authenticated
   */
  async createTodo(title: string, description?: string | null): Promise<Todo> {
    const request: CreateTodoRequest = { title, description };
    return api.post<Todo>('/todos', request);
  },

  /**
   * Update an existing todo.
   * @param todoId - UUID of the todo to update
   * @param title - New todo title (1-500 characters)
   * @param description - New optional todo description
   * @returns Updated todo
   * @throws APIError with status 404 if todo not found
   * @throws APIError with status 401 if not authenticated
   */
  async updateTodo(
    todoId: string,
    title: string,
    description?: string | null
  ): Promise<Todo> {
    const request: UpdateTodoRequest = { title, description };
    return api.put<Todo>(`/todos/${todoId}`, request);
  },

  /**
   * Toggle the completion status of a todo.
   * @param todoId - UUID of the todo to toggle
   * @returns Updated todo with new completion status
   * @throws APIError with status 404 if todo not found
   * @throws APIError with status 401 if not authenticated
   */
  async toggleCompletion(todoId: string): Promise<Todo> {
    const response = await api.patch<ToggleCompletionResponse>(
      `/todos/${todoId}/toggle`
    );
    return response.todo;
  },

  /**
   * Delete a todo.
   * @param todoId - UUID of the todo to delete
   * @returns Success message
   * @throws APIError with status 404 if todo not found
   * @throws APIError with status 401 if not authenticated
   */
  async deleteTodo(todoId: string): Promise<MessageResponse> {
    return api.delete<MessageResponse>(`/todos/${todoId}`);
  },
};
