import React, { useState } from "react";
import { Send } from "lucide-react";

const ChatInterface = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const sessionId = React.useMemo(
    () => Math.random().toString(36).substring(7),
    []
  );

  const handleSend = async (e) => {
    e.preventDefault();
    if (input.trim()) {
      const userMessage = { type: "user", content: input };
      setMessages((prev) => [...prev, userMessage]);
      setInput("");
      setIsLoading(true);

      try {
        const response = await fetch("http://localhost:8000/chat/send", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            session_id: sessionId,
            message: input,
          }),
        });

        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.detail || "Server error occurred");
        }

        const assistantMessage = {
          type: "assistant",
          content: data.response,
        };
        setMessages((prev) => [...prev, assistantMessage]);
      } catch (error) {
        console.error("Error sending message:", error);
        const errorMessage = {
          type: "assistant",
          content: `Error: ${
            error.message || "Unable to process your request. Please try again."
          }`,
        };
        setMessages((prev) => [...prev, errorMessage]);
      } finally {
        setIsLoading(false);
      }
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-messages">
        <div className="message-list">
          {messages.map((message, index) => (
            <div key={index} className={`message ${message.type}`}>
              <div className="message-content">{message.content}</div>
            </div>
          ))}
          {isLoading && (
            <div className="message assistant">
              <div className="message-content">
                <span className="loading-dots">Thinking...</span>
              </div>
            </div>
          )}
        </div>
      </div>
      <form onSubmit={handleSend} className="chat-input-container">
        <div className="chat-input-form">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a question about your PDFs..."
            className="chat-input"
            disabled={isLoading}
          />
          <button type="submit" className="chat-send-btn" disabled={isLoading}>
            <Send size={20} />
          </button>
        </div>
      </form>
    </div>
  );
};

export default ChatInterface;
