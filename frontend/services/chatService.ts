/**
 * Chat service for frontend API calls (Phase III).
 */
import { api } from '@/lib/api';
import type {
  ChatResponse,
  Conversation,
  ConversationWithMessages,
  StreamChunk,
} from '@/types/chat';
import type { MessageResponse } from '@/types/auth';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const chatService = {
  /**
   * Send a message to the AI assistant and get a response.
   */
  async sendMessage(
    message: string,
    conversationId?: string | null
  ): Promise<ChatResponse> {
    return api.post<ChatResponse>('/api/chat', {
      message,
      conversation_id: conversationId || null,
    });
  },

  /**
   * Send a message with streaming response via SSE.
   * Calls onChunk for each token received and onDone when complete.
   */
  async sendMessageStream(
    message: string,
    conversationId: string | null | undefined,
    onChunk: (chunk: string, conversationId: string) => void,
    onDone: (conversationId: string) => void,
    onError: (error: string) => void
  ): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/api/chat/stream`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({
        message,
        conversation_id: conversationId || null,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ detail: 'Stream error' }));
      onError(errorData.detail || 'Failed to connect to chat stream');
      return;
    }

    const reader = response.body?.getReader();
    if (!reader) {
      onError('Stream not available');
      return;
    }

    const decoder = new TextDecoder();
    let buffer = '';

    try {
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop() || '';

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data: StreamChunk = JSON.parse(line.slice(6));
              if (data.error) {
                onError(data.error);
                return;
              }
              if (data.done && data.conversation_id) {
                onDone(data.conversation_id);
                return;
              }
              if (data.chunk && data.conversation_id) {
                onChunk(data.chunk, data.conversation_id);
              }
            } catch {
              // Skip malformed SSE lines
            }
          }
        }
      }
    } finally {
      reader.releaseLock();
    }
  },

  /**
   * Get all conversations for the authenticated user.
   */
  async getConversations(): Promise<Conversation[]> {
    const response = await api.get<{ conversations: Conversation[] }>(
      '/api/conversations'
    );
    return response.conversations;
  },

  /**
   * Get a specific conversation with its messages.
   */
  async getConversation(conversationId: string): Promise<ConversationWithMessages> {
    return api.get<ConversationWithMessages>(
      `/api/conversations/${conversationId}`
    );
  },

  /**
   * Get messages for a specific conversation.
   */
  async getConversationMessages(
    conversationId: string
  ): Promise<ConversationWithMessages> {
    return api.get<ConversationWithMessages>(
      `/api/conversations/${conversationId}`
    );
  },

  /**
   * Delete a conversation.
   */
  async deleteConversation(conversationId: string): Promise<MessageResponse> {
    return api.delete<MessageResponse>(`/api/conversations/${conversationId}`);
  },
};
