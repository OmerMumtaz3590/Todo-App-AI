/**
 * Authentication service for frontend API calls.
 */
import { api } from '@/lib/api';
import type {
  SignupRequest,
  SignupResponse,
  SigninRequest,
  SigninResponse,
  MessageResponse,
  User,
} from '@/types/auth';

export const authService = {
  /**
   * Create a new user account.
   * @param email - User email address
   * @param password - User password (min 8 characters)
   * @returns Signup response with user_id
   * @throws APIError with status 409 if email already exists
   * @throws APIError with status 400 if validation fails
   */
  async signup(email: string, password: string): Promise<SignupResponse> {
    const request: SignupRequest = { email, password };
    return api.post<SignupResponse>('/auth/signup', request);
  },

  /**
   * Sign in an existing user and establish a session.
   * @param email - User email address
   * @param password - User password
   * @returns Signin response with user info
   * @throws APIError with status 401 if credentials are invalid
   */
  async signin(email: string, password: string): Promise<SigninResponse> {
    const request: SigninRequest = { email, password };
    return api.post<SigninResponse>('/auth/signin', request);
  },

  /**
   * Sign out the authenticated user and clear the session.
   * @returns Success message
   * @throws APIError with status 401 if not authenticated
   */
  async signout(): Promise<MessageResponse> {
    return api.post<MessageResponse>('/auth/signout');
  },

  /**
   * Get the current authenticated user.
   * This assumes a /auth/me endpoint exists (to be implemented in future).
   * @returns User info or null if not authenticated
   */
  async getCurrentUser(): Promise<User | null> {
    try {
      // This endpoint will be implemented in Phase 9 (T040+)
      // For now, return null - authentication state managed via cookies
      return null;
    } catch (error) {
      return null;
    }
  },
};
