/**
 * Todo type definitions for the frontend.
 */

export interface Todo {
  id: string;
  title: string;
  description: string | null;
  is_completed: boolean;
  created_at: string;
  updated_at: string;
}

export interface TodoListResponse {
  todos: Todo[];
}

export interface CreateTodoRequest {
  title: string;
  description?: string | null;
}

export interface UpdateTodoRequest {
  title: string;
  description?: string | null;
}

export interface ToggleCompletionResponse {
  message: string;
  todo: Todo;
}
