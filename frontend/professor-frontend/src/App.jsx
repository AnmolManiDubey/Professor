import React, { useState, useRef, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
import "./App.css";

// Helper to remove "Reference Links" section from Markdown
function stripReferenceLinksSection(markdown) {
  const regex = /#+\s*Reference\s+Links[\s\S]*?(?=\n#+\s|\n?$)/i;
  return markdown.replace(regex, "").trim();
}

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, errorMessage: "" };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, errorMessage: error.message };
  }

  componentDidCatch(error, errorInfo) {
    console.error("ErrorBoundary caught an error", error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="error-boundary">
          <h3>Failed to load explanation.</h3>
          <p>{this.state.errorMessage}</p>
        </div>
      );
    }
    return this.props.children;
  }
}

export default function App() {
  const [topic, setTopic] = useState("");
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const chatContainerRef = useRef(null);
  const inputRef = useRef(null);

  const scrollToBottom = () => {
    if (chatContainerRef.current) {
      setTimeout(() => {
        chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
      }, 100);
    }
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  useEffect(() => {
    // Auto-focus the search input when component mounts
    if (inputRef.current) {
      inputRef.current.focus();
    }
  }, []);

  // Refocus input after messages change (when new message is added)
  useEffect(() => {
    if (messages.length > 0 && inputRef.current) {
      // Small delay to ensure the message is rendered
      setTimeout(() => {
        inputRef.current.focus();
      }, 200);
    }
  }, [messages.length]);

  async function handleSubmit(e) {
    e.preventDefault();
    if (!input.trim()) return;

    const newMessages = [...messages, { role: "user", content: input.trim() }];
    setMessages(newMessages);
    setInput("");
    setLoading(true);
    setError(null);

    try {
const res = await fetch("https://professor-backend.vercel.app/teach", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    topic: input.trim(), // always use current topic
    messages: newMessages,
  }),
});

      if (!res.ok) {
        throw new Error("Failed to fetch explanation");
      }

      const data = await res.json();

      setTopic(data.topic); // 🆙 update topic here

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.explanation,
          images: data.images || [],
          references: data.reference_links || [],
        },
      ]);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  function toggleTheme() {
    document.body.classList.toggle("dark-mode");
  }

  return (
    <div className="app-container">
      <header className="app-header">
        <div className="header-content">
          <h1>Professor AI</h1>
          <p className="header-subtitle">Your intelligent learning companion</p>
        </div>
        <button onClick={toggleTheme} className="btn-theme-toggle" aria-label="Toggle Dark Mode">
          🌓
        </button>
      </header>

      <main className="main-content">
        <div className="chat-container" ref={chatContainerRef}>
          {messages.length === 0 && (
            <div className="welcome-message">
              <div className="welcome-icon">🎓</div>
              <h2>Welcome to Professor AI</h2>
              <p>Ask me anything! I'm here to help you learn and understand complex topics.</p>
            </div>
          )}

          <div className="chat-messages">
            {messages.map((msg, i) => (
              <div
                key={i}
                className={`chat-message ${msg.role === "user" ? "chat-user" : "chat-assistant"}`}
              >
                <div className="message-avatar">
                  {msg.role === "user" ? "👤" : "🤖"}
                </div>
                <div className="message-content">
                  <ErrorBoundary>
                    <ReactMarkdown remarkPlugins={[remarkMath]} rehypePlugins={[rehypeKatex]}>
                      {stripReferenceLinksSection(
                        (msg.content || "")
                          .replace(/\\begin\{aligned\}/g, "")
                          .replace(/\\end\{aligned\}/g, "")
                          .replace(/\\\\/g, "\n")
                      )}
                    </ReactMarkdown>
                  </ErrorBoundary>

                  {msg.role === "assistant" && (
                    <>
                      {msg.images?.length > 0 && (
                        <div className="image-grid">
                          {msg.images.map((img, idx) => (
                            <a
                              key={idx}
                              href={img.link}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="image-card"
                            >
                              <img src={img.thumbnail} alt={img.title} />
                              <p>{img.title}</p>
                            </a>
                          ))}
                        </div>
                      )}

                      {msg.references?.length > 0 && (
                        <div className="reference-block">
                          <h4>📚 Reference Links</h4>
                          <ul>
                            {msg.references.map((ref, idx) => (
                              <li key={idx}>
                                <a href={ref.url} target="_blank" rel="noopener noreferrer">
                                  {ref.title}
                                </a>
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </>
                  )}
                </div>
              </div>
            ))}
            {loading && (
              <div className="chat-message chat-assistant">
                <div className="message-avatar">🤖</div>
                <div className="message-content">
                  <div className="loading-indicator">
                    <div className="loading-dots">
                      <span></span>
                      <span></span>
                      <span></span>
                    </div>
                    <p>Thinking...</p>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>

        {error && (
          <div className="error-container">
            <p className="error-msg">❌ Error: {error}</p>
          </div>
        )}

        <div className="search-container">
          <form onSubmit={handleSubmit} className="search-form">
            <div className="search-input-wrapper">
              <input
                ref={inputRef}
                type="text"
                placeholder="Ask your question here..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
                className="search-input"
                aria-label="Chat input"
                disabled={loading}
              />
              <button 
                type="submit" 
                disabled={loading || !input.trim()} 
                className="search-button"
              >
                {loading ? (
                  <div className="button-loading">
                    <span></span>
                  </div>
                ) : (
                  "➤"
                )}
              </button>
            </div>
          </form>
        </div>
      </main>

      <footer className="app-footer">
        <small>© 2025 Professor AI - Powered by AI</small>
      </footer>
    </div>
  );
}
