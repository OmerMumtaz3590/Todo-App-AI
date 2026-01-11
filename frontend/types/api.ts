/**
 * API request and response TypeScript types
 */

// Common API response types
export interface APIResponse<T = any> {
  data?: T;
  error?: string;
  message?: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
}

// Error response
export interface ErrorResponse {
  error: string;
  detail?: string;
}
