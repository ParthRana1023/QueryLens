import React, { useState } from 'react';
import { Send } from 'lucide-react';

const ChatInterface = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  const handleSend = (e) => {
    e.preventDefault();
    if (input.trim()) {
      setMessages([...messages, { type: 'user', content: input }]);
      // Here you would typically make an API call to get the response
      setMessages(prev => [...prev, { 
        type: 'assistant', 
        content: 'This is a mock response. In a real implementation, this would be the response from your PDF knowledge base.'
      }]);
      setInput('');
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-messages">
        <div className="message-list">
          {messages.map((message, index) => (
            <div
              key={index}
              className={`message ${message.type}`}
            >
              <div className="message-content">
                {message.content}
              </div>
            </div>
          ))}
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
          />
          <button type="submit" className="chat-send-btn">
            <Send size={20} />
          </button>
        </div>
      </form>
    </div>
  );
};

export default ChatInterface;