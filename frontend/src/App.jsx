import React, { useState, useRef, useEffect } from "react";

export default function App() {
  const [messages, setMessages] = useState([
    {
      sender: "bot",
      text: "Hello! I'm your Blacksmith Data Assistant. How can I help you today? You can ask about our remote working policy, Wi-Fi, expense claims, or IT setups!",
      sources: []
    }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [openSources, setOpenSources] = useState({});
  const messagesEndRef = useRef(null);

  const toggleSource = (idx) => {
    setOpenSources(prev => ({ ...prev, [idx]: !prev[idx] }));
  };

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMessage = input.trim();
    setInput("");
    setError(null);
    setMessages(prev => [...prev, { sender: "user", text: userMessage }]);
    setLoading(true);

    try {
      const response = await fetch("http://localhost:8000/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMessage })
      });

      if (!response.ok) throw new Error(`Server status ${response.status}`);

      const data = await response.json();
      setMessages(prev => [
        ...prev,
        { sender: "bot", text: data.answer, sources: data.sources || [] }
      ]);
    } catch (err) {
      setError("Unable to reach the assistant. Please ensure the backend is running.");
      setMessages(prev => [
        ...prev,
        { sender: "bot", text: "Oops! I encountered an issue connecting to the server.", sources: [] }
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-[#110d14] text-rose-50 font-sans">
      {/* Header */}
      <header className="px-6 py-4 bg-[#1b1422] border-b border-pink-950/80 flex items-center justify-between shadow-lg">
        <div className="flex items-center space-x-3">
          <div className="w-9 h-9 rounded-2xl bg-gradient-to-tr from-pink-600 to-rose-400 flex items-center justify-center shadow-md shadow-pink-500/20 text-white font-bold text-sm">
            B
          </div>
          <div>
            <h1 className="text-base font-semibold tracking-tight text-white">Blacksmith AI Assistant</h1>
            <p className="text-xs text-pink-300/70">Company Knowledge Base</p>
          </div>
        </div>
        <span className="text-xs font-medium bg-pink-950/60 text-pink-300 border border-pink-800/40 px-3 py-1 rounded-full">
          Grounded RAG
        </span>
      </header>

      {/* Chat Area */}
      <main className="flex-1 overflow-y-auto p-4 md:p-6 space-y-4 max-w-3xl w-full mx-auto">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`flex flex-col ${msg.sender === "user" ? "items-end" : "items-start"}`}
          >
            {/* Message Bubble */}
            <div
              className={`max-w-xl px-4 py-3 rounded-2xl text-sm leading-relaxed shadow-sm ${
                msg.sender === "user"
                  ? "bg-gradient-to-r from-pink-600 to-rose-500 text-white rounded-br-xs"
                  : "bg-[#1d1624] text-rose-100 border border-pink-950/90 rounded-bl-xs"
              }`}
            >
              <p className="whitespace-pre-wrap">{msg.text}</p>
            </div>

            {/* Collapsible Source References */}
            {msg.sources && msg.sources.length > 0 && (
              <div className="mt-2 max-w-xl w-full">
                <button
                  type="button"
                  onClick={() => toggleSource(index)}
                  className="flex items-center space-x-1.5 text-xs text-pink-300/80 hover:text-pink-200 transition-colors py-1 px-2 rounded-lg bg-pink-950/30 border border-pink-900/40"
                >
                  <span>📚</span>
                  <span className="font-medium">
                    {openSources[index] ? "Hide Sources" : `View Sources (${msg.sources.length})`}
                  </span>
                </button>

                {openSources[index] && (
                  <div className="mt-2 space-y-2 pl-2 border-l-2 border-pink-500/40 animate-fadeIn">
                    {msg.sources.map((src, sIdx) => (
                      <div key={sIdx} className="bg-[#18111e] p-3 rounded-xl border border-pink-950/60 text-xs">
                        <div className="font-semibold text-pink-400 mb-1">{src.title}</div>
                        <div className="text-pink-200/70 leading-relaxed">{src.content}</div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        ))}

        {/* Loading Spinner */}
        {loading && (
          <div className="flex items-center space-x-2 text-pink-300/80 text-xs py-2 bg-[#1d1624] px-4 py-2.5 rounded-2xl w-fit border border-pink-950/90">
            <div className="w-1.5 h-1.5 bg-pink-400 rounded-full animate-bounce"></div>
            <div className="w-1.5 h-1.5 bg-pink-400 rounded-full animate-bounce [animation-delay:-.2s]"></div>
            <div className="w-1.5 h-1.5 bg-pink-400 rounded-full animate-bounce [animation-delay:-.4s]"></div>
            <span>Reading knowledge base & drafting answer...</span>
          </div>
        )}

        {/* Error Alert */}
        {error && (
          <div className="bg-rose-950/50 border border-rose-800/80 text-rose-200 p-3 rounded-xl text-xs">
            {error}
          </div>
        )}

        <div ref={messagesEndRef} />
      </main>

      {/* Input Footer */}
      <footer className="p-4 bg-[#1b1422]/90 border-t border-pink-950/80">
        <form onSubmit={handleSubmit} className="max-w-3xl mx-auto flex items-center space-x-2">
          <input
            type="text"
            className="flex-1 bg-[#120d17] border border-pink-950/90 focus:border-pink-500/60 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-1 focus:ring-pink-500 text-rose-50 placeholder-pink-300/40 transition-all"
            placeholder="Ask about hybrid hours, sick leave, VPN..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={loading}
          />
          <button
            type="submit"
            disabled={loading || !input.trim()}
            className="bg-gradient-to-r from-pink-600 to-rose-500 hover:from-pink-500 hover:to-rose-400 disabled:opacity-40 text-white font-medium px-5 py-3 rounded-xl text-sm transition-all shadow-md shadow-pink-600/20"
          >
            Send
          </button>
        </form>
      </footer>
    </div>
  );
}