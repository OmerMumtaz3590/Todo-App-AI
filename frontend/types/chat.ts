/**
 * Chat type definitions for the frontend (Phase III).
 */

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  created_at: string;
}

export interface Conversation {
  id: string;
  title: string | null;
  created_at: string;
  updated_at: string;
}

export interface ChatRequest {
  message: string;
  conversation_id?: string | null;
}

export interface ChatResponse {
  response: string;
  conversation_id: string;
}

export interface ConversationWithMessages {
  id: string;
  title: string | null;
  created_at: string;
  updated_at: string;
  messages: ChatMessage[];
}

export interface StreamChunk {
  chunk?: string;
  conversation_id?: string;
  done?: boolean;
  error?: string;
}
