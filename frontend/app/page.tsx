"use client"
import { useState } from "react";
import { DefaultChatTransport } from "ai";
import { useChat } from "@ai-sdk/react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

export default function Home() {
  const [input, setInput] = useState("");
  const { messages, sendMessage, status } = useChat ({
    transport: new DefaultChatTransport({ api: "http://localhost:8000/api/v1/ask/" }),
  });
  const busy = status === "submitted" || status === "streaming";
  const assistantCount = messages.filter((m) => m.role === "assistant").length;

  return (
    
    <div>
      {messages.map((m) => (
        <div key={m.id}>
          <b>{m.role}:</b>{" "}
          {m.parts.map((p, i) => (p.type === "text" ? 
          //<span key={i}>{p.text}</span>
          <ReactMarkdown key={i} remarkPlugins={[remarkGfm]}>{p.text}</ReactMarkdown>
          : null)
          )}
        </div>
      ))}
      <p>Replies: {assistantCount}</p>
      <input value={input} onChange={(e) => setInput(e.target.value)} disabled={busy} />
      <button onClick={() => { sendMessage({ text: input}); setInput(""); }} disabled={input.trim() === "" || busy}>Send</button>
    </div>
  );
}

