import React, { useRef } from 'react';

const ChatForms = ({chatHistory,setChatHistory,generateBotResponse}) => {
  const inputRef = useRef();

  const handleFormSubmit = (e) => {
    e.preventDefault();

    const userMessage = inputRef.current.value.trim();
    console.log("user Message: ",userMessage);

    if (!userMessage) return console.log("Not defined");

    console.log("User message:", userMessage);

    // Optional: clear the input field
    setChatHistory((history)=>[...history, {role:"user",text:userMessage}]);

    // Plac holder for bot response....
    setTimeout(()=> { 
    setChatHistory((history)=>[...history, {role:"model",text:"Thinking..."}]),
    // Generating bot response
    generateBotResponse([...chatHistory,{role:"user",text:userMessage}],userMessage)
    },600)
  
    inputRef.current.value = "";
  };

  return (
    <form action="#" className="chat-form" onSubmit={handleFormSubmit}>
      <input
        type="text"
        ref={inputRef}
        placeholder="Write chat message..."
        className="message-input"
        required
      />
      <button type="submit" className="material-symbols-rounded">
        arrow_upward
      </button>
    </form>
  );
};

export default ChatForms;
