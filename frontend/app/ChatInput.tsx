"use client"

export default function ChatInput({ inputText, 
  onInputTextChange,
  onSend }: {inputText: string; onInputTextChange: (value: string) => void; onSend: (value: string) => void }) {
  return (
    <div>
      <input type="text"
      value={inputText}
      placeholder="Ask about HDB resale..."
      onChange={ (e) => onInputTextChange(e.target.value)}/>
      <button onClick={() => onSend(inputText)}>
        Send!
      </button>
    </div>
  );
}