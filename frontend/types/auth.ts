/**
 * Authentication type definitions for the frontend.
 */

export interface SignupRequest {
  email: string;
  password: string;
}

export interface SignupResponse {
  message: string;
  user_id: string;
}

export interface SigninRequest {
  email: string;
  password: string;
}

export interface SigninResponse {
  message: string;
  user: User;
}

export interface User {
  id: string;
  email: string;
}

export interface MessageResponse {
  message: string;
}

export interface ErrorResponse {
  error: string;
  detail?: string;
}

/**
 * Authentication state for the application.
 */
export interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}
