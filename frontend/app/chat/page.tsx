'use client';

import { useState, useEffect, useRef, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { chatService } from '@/services/chatService';
import { authService } from '@/services/authService';
import type { ChatMessage, Conversation } from '@/types/chat';
import { APIError } from '@/lib/api';

/**
 * Simple markdown-to-HTML converter for chat messages (MCP-061).
 * Handles: bold, italic, code blocks, inline code, lists, line breaks.
 */
function renderMarkdown(text: string): string {
  let html = text
    // Escape HTML entities
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    // Code blocks (``` ... ```)
    .replace(/```(\w*)\n([\s\S]*?)```/g, '<pre class="bg-gray-800 text-green-300 p-3 rounded-lg my-2 overflow-x-auto text-sm"><code>$2</code></pre>')
    // Inline code
    .replace(/`([^`]+)`/g, '<code class="bg-gray-200 text-gray-800 px-1 rounded text-sm">$1</code>')
    // Bold
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    // Italic
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    // Unordered lists
    .replace(/^\s*[-*]\s+(.+)$/gm, '<li class="ml-4">$1</li>')
    // Ordered lists
    .replace(/^\s*\d+\.\s+(.+)$/gm, '<li class="ml-4 list-decimal">$1</li>')
    // Line breaks (double newline = paragraph)
    .replace(/\n\n/g, '<br/><br/>')
    // Single line breaks
    .replace(/\n/g, '<br/>');

  // Wrap consecutive <li> elements in <ul>
  html = html.replace(/((?:<li[^>]*>.*?<\/li>\s*(?:<br\/>)?)+)/g, '<ul class="list-disc my-2">$1</ul>');

  return html;
}

export default function ChatPage() {
  const router = useRouter();
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [activeConversationId, setActiveConversationId] = useState<string | null>(null);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isStreaming, setIsStreaming] = useState(false);
  const [streamingContent, setStreamingContent] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  // Auto-scroll to bottom when messages change
  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, streamingContent, scrollToBottom]);

  // Load conversations on mount
  useEffect(() => {
    loadConversations();
  }, []);

  async function loadConversations() {
    try {
      const convs = await chatService.getConversations();
      setConversations(convs);
    } catch (err) {
      if (err instanceof APIError && err.status === 401) {
        router.push('/auth/signin');
        return;
      }
      // Silently fail — conversations sidebar just empty
    }
  }

  async function loadConversation(conversationId: string) {
    try {
      const conv = await chatService.getConversation(conversationId);
      setActiveConversationId(conversationId);
      setMessages(conv.messages || []);
      setError(null);
    } catch (err) {
      if (err instanceof APIError && err.status === 401) {
        router.push('/auth/signin');
        return;
      }
      setError('Failed to load conversation.');
    }
  }

  async function handleSend() {
    if (!input.trim() || isLoading || isStreaming) return;

    const userMessage = input.trim();
    setInput('');
    setError(null);

    // Optimistically add user message
    const tempUserMsg: ChatMessage = {
      id: `temp-${Date.now()}`,
      role: 'user',
      content: userMessage,
      created_at: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, tempUserMsg]);

    // Use streaming
    setIsStreaming(true);
    setStreamingContent('');

    try {
      await chatService.sendMessageStream(
        userMessage,
        activeConversationId,
        // onChunk
        (chunk: string, conversationId: string) => {
          if (!activeConversationId) {
            setActiveConversationId(conversationId);
          }
          setStreamingContent((prev) => prev + chunk);
        },
        // onDone
        (conversationId: string) => {
          setStreamingContent((prev) => {
            // Move streaming content to final message
            const finalContent = prev;
            if (finalContent) {
              const assistantMsg: ChatMessage = {
                id: `msg-${Date.now()}`,
                role: 'assistant',
                content: finalContent,
                created_at: new Date().toISOString(),
              };
              setMessages((msgs) => [...msgs, assistantMsg]);
            }
            return '';
          });
          setIsStreaming(false);
          setActiveConversationId(conversationId);
          loadConversations();
        },
        // onError
        (errorMsg: string) => {
          setError(errorMsg);
          setIsStreaming(false);
          setStreamingContent('');
        }
      );
    } catch {
      // Fallback to non-streaming
      setIsStreaming(false);
      setStreamingContent('');
      setIsLoading(true);
      try {
        const response = await chatService.sendMessage(
          userMessage,
          activeConversationId
        );
        const assistantMsg: ChatMessage = {
          id: `msg-${Date.now()}`,
          role: 'assistant',
          content: response.response,
          created_at: new Date().toISOString(),
        };
        setMessages((prev) => [...prev, assistantMsg]);
        setActiveConversationId(response.conversation_id);
        loadConversations();
      } catch (err) {
        if (err instanceof APIError && err.status === 401) {
          router.push('/auth/signin');
          return;
        }
        setError(err instanceof Error ? err.message : 'Failed to send message.');
      } finally {
        setIsLoading(false);
      }
    }
  }

  function handleNewConversation() {
    setActiveConversationId(null);
    setMessages([]);
    setStreamingContent('');
    setError(null);
    inputRef.current?.focus();
  }

  async function handleDeleteConversation(conversationId: string, e: React.MouseEvent) {
    e.stopPropagation();
    if (!confirm('Delete this conversation?')) return;
    try {
      await chatService.deleteConversation(conversationId);
      if (activeConversationId === conversationId) {
        handleNewConversation();
      }
      setConversations((prev) => prev.filter((c) => c.id !== conversationId));
    } catch (err) {
      setError('Failed to delete conversation.');
    }
  }

  async function handleSignOut() {
    try {
      await authService.signout();
      router.push('/auth/signin');
    } catch {
      router.push('/auth/signin');
    }
  }

  function handleKeyDown(e: React.KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  }

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Sidebar - Conversation History (MCP-063) */}
      {sidebarOpen && (
        <div className="w-72 bg-gray-900 text-white flex flex-col">
          <div className="p-4 border-b border-gray-700">
            <button
              onClick={handleNewConversation}
              className="w-full px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg text-sm font-medium transition-colors"
            >
              + New Chat
            </button>
          </div>
          <div className="flex-1 overflow-y-auto">
            {conversations.map((conv) => (
              <div
                key={conv.id}
                onClick={() => loadConversation(conv.id)}
                className={`group flex items-center justify-between px-4 py-3 cursor-pointer hover:bg-gray-800 transition-colors ${
                  activeConversationId === conv.id ? 'bg-gray-800' : ''
                }`}
              >
                <span className="text-sm truncate flex-1">
                  {conv.title || 'New Conversation'}
                </span>
                <button
                  onClick={(e) => handleDeleteConversation(conv.id, e)}
                  className="opacity-0 group-hover:opacity-100 text-gray-400 hover:text-red-400 ml-2 transition-opacity"
                  title="Delete conversation"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              </div>
            ))}
            {conversations.length === 0 && (
              <p className="text-gray-500 text-sm text-center py-8">
                No conversations yet
              </p>
            )}
          </div>
          <div className="p-4 border-t border-gray-700 space-y-2">
            <a
              href="/todos"
              className="block text-center text-sm text-gray-400 hover:text-white transition-colors"
            >
              Classic Todos View
            </a>
            <button
              onClick={handleSignOut}
              className="w-full px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded-lg text-sm transition-colors"
            >
              Sign Out
            </button>
          </div>
        </div>
      )}

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <div className="bg-white border-b px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="text-gray-500 hover:text-gray-700"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
            <h1 className="text-xl font-semibold text-gray-800">Todo AI Assistant</h1>
          </div>
        </div>

        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto px-6 py-4 space-y-4">
          {messages.length === 0 && !isStreaming && (
            <div className="flex flex-col items-center justify-center h-full text-gray-400">
              <svg className="w-16 h-16 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
              <p className="text-lg font-medium">Start a conversation</p>
              <p className="text-sm mt-1">Ask me to manage your todos using natural language</p>
              <div className="mt-6 grid gap-2 text-sm">
                <p className="text-gray-500">Try saying:</p>
                <button
                  onClick={() => setInput('Show me all my todos')}
                  className="px-4 py-2 bg-white border rounded-lg hover:bg-gray-50 text-gray-600 transition-colors"
                >
                  &quot;Show me all my todos&quot;
                </button>
                <button
                  onClick={() => setInput('Add a todo: Buy groceries')}
                  className="px-4 py-2 bg-white border rounded-lg hover:bg-gray-50 text-gray-600 transition-colors"
                >
                  &quot;Add a todo: Buy groceries&quot;
                </button>
                <button
                  onClick={() => setInput('What tasks do I have left?')}
                  className="px-4 py-2 bg-white border rounded-lg hover:bg-gray-50 text-gray-600 transition-colors"
                >
                  &quot;What tasks do I have left?&quot;
                </button>
              </div>
            </div>
          )}

          {messages.map((msg) => (
            <div
              key={msg.id}
              className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[75%] rounded-2xl px-4 py-3 ${
                  msg.role === 'user'
                    ? 'bg-blue-600 text-white'
                    : 'bg-white border border-gray-200 text-gray-800'
                }`}
              >
                {msg.role === 'assistant' ? (
                  <div
                    className="prose prose-sm max-w-none"
                    dangerouslySetInnerHTML={{ __html: renderMarkdown(msg.content) }}
                  />
                ) : (
                  <p className="whitespace-pre-wrap">{msg.content}</p>
                )}
              </div>
            </div>
          ))}

          {/* Streaming indicator (MCP-062) */}
          {isStreaming && streamingContent && (
            <div className="flex justify-start">
              <div className="max-w-[75%] rounded-2xl px-4 py-3 bg-white border border-gray-200 text-gray-800">
                <div
                  className="prose prose-sm max-w-none"
                  dangerouslySetInnerHTML={{ __html: renderMarkdown(streamingContent) }}
                />
                <span className="inline-block w-2 h-4 bg-gray-400 animate-pulse ml-1" />
              </div>
            </div>
          )}

          {/* Typing indicator */}
          {(isLoading || (isStreaming && !streamingContent)) && (
            <div className="flex justify-start">
              <div className="bg-white border border-gray-200 rounded-2xl px-4 py-3">
                <div className="flex space-x-2">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                </div>
              </div>
            </div>
          )}

          {/* Error display */}
          {error && (
            <div className="flex justify-center">
              <div className="bg-red-50 border border-red-200 text-red-700 rounded-lg px-4 py-3 text-sm max-w-md">
                <p>{error}</p>
                <button
                  onClick={() => setError(null)}
                  className="text-red-500 hover:text-red-700 text-xs mt-1 underline"
                >
                  Dismiss
                </button>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="bg-white border-t px-6 py-4">
          <div className="max-w-4xl mx-auto flex gap-3">
            <textarea
              ref={inputRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Type a message... (Enter to send, Shift+Enter for new line)"
              className="flex-1 resize-none border border-gray-300 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-800 placeholder-gray-400"
              rows={1}
              disabled={isLoading || isStreaming}
            />
            <button
              onClick={handleSend}
              disabled={!input.trim() || isLoading || isStreaming}
              className="px-6 py-3 bg-blue-600 text-white rounded-xl hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
