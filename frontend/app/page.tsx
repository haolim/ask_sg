"use client"
import { useState } from "react";
import ChatInput from "./ChatInput";

type Message = {
  text: string;
  role: string;
} 

export default function Home() {
  const [inputText, setInputText] = useState("");
  const [userMessages, setUserMessages] = useState<Message[]>([
    {text: "How can I help you today?", role: "system"},
    {text: "Median price in Bishan?", role: "user"},
    {text: "I'm sorry, there is no information found for Bishan.", role: "system"}
  ]);
  function handleSend(newText: string) {
    setUserMessages([...userMessages, {text: newText, role: "user"}]);
    setInputText("")
  }
  return(
    <main>
      <h1>ask_sg</h1>
      <div>
      <ChatInput
        inputText={inputText}
        onInputTextChange={setInputText} 
        onSend={handleSend}/>
      </div>

      <div>
        {userMessages.map( (m, i) => <MessageBubble key={i} text={m.text} role={m.role} />)}
      </div>
    </main>
  );
}

function MessageBubble( {text, role}: {text: string; role: string}) {
  return (
    <div>
      {role === "user" ? "You: " : "Bot: "}
      {text}
    </div>
  );
}



