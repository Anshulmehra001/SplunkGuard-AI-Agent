import React, { useState } from 'react';
import './ChatInterface.css';
import * as api from '../api';

function ChatInterface() {
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState([
    {
      type: 'agent',
      text: '👋 Hi! I\'m SplunkGuard AI. Ask me about security threats, events, or query your Splunk data in plain English!',
      timestamp: new Date()
    }
  ]);
  const [loading, setLoading] = useState(false);

  const exampleQueries = [
    'Show me failed logins in the last hour',
    'What are the top threat sources today?',
    'Any suspicious activity from 192.168.1.100?',
    'List all critical security events'
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!query.trim() || loading) return;

    const userMessage = {
      type: 'user',
      text: query,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setQuery('');
    setLoading(true);

    try {
      const response = await api.sendQuery(query);
      
      const agentMessage = {
        type: 'agent',
        text: response.response?.explanation || 'Query processed successfully!',
        data: response,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, agentMessage]);
    } catch (error) {
      const errorMessage = {
        type: 'error',
        text: `Sorry, I encountered an error: ${error.message}`,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleExampleClick = (example) => {
    setQuery(example);
  };

  return (
    <div className="chat-interface">
      <h2>💬 Chat with AI Agent</h2>
      
      <div className="chat-messages">
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.type}`}>
            <div className="message-header">
              <span className="message-sender">
                {message.type === 'user' ? '👤 You' : '🤖 SplunkGuard AI'}
              </span>
              <span className="message-time">
                {message.timestamp.toLocaleTimeString()}
              </span>
            </div>
            <div className="message-text">{message.text}</div>
            
            {message.data?.results && (
              <div className="message-data">
                <div className="data-header">
                  Found {message.data.count} results
                </div>
                {message.data.splunk_query && (
                  <div className="splunk-query">
                    <strong>Splunk Query:</strong>
                    <code>{message.data.splunk_query}</code>
                  </div>
                )}
              </div>
            )}
          </div>
        ))}
        
        {loading && (
          <div className="message agent loading-message">
            <div className="message-text">
              <span className="typing-indicator">
                <span></span><span></span><span></span>
              </span>
              Analyzing...
            </div>
          </div>
        )}
      </div>

      <div className="example-queries">
        <p>Try these examples:</p>
        <div className="examples-list">
          {exampleQueries.map((example, index) => (
            <button
              key={index}
              className="example-btn"
              onClick={() => handleExampleClick(example)}
              disabled={loading}
            >
              {example}
            </button>
          ))}
        </div>
      </div>

      <form className="chat-input-form" onSubmit={handleSubmit}>
        <input
          type="text"
          className="chat-input"
          placeholder="Ask me anything about security..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          disabled={loading}
        />
        <button 
          type="submit" 
          className="send-btn"
          disabled={loading || !query.trim()}
        >
          {loading ? '⏳' : '🚀'}
        </button>
      </form>
    </div>
  );
}

export default ChatInterface;
