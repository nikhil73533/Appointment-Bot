import React, { useState } from "react";
import ChatbotIcon from "./components/ChatbotIcon";
import ChatForms from "./components/ChatForms";
import ChatMessage from "./components/ChatMessage";

const App = () => {
  const [chatHistory,setChatHistory] = useState([]);
 

  const generateBotResponse = async (history,userMessage)=>{

     const updateHistory = (apiResponseText)=>{
      setChatHistory(prev =>[...prev.filter(msg=> msg.text !=="Thinking..."),{role:"model",text:apiResponseText}])
  }
    console.log(userMessage);
    const requestOptions = {
      method:"POST",
      headers:{"Content-Type":"application/json"},
      body: JSON.stringify({user_query:userMessage})
    }

    try {
        const url =  "http://127.0.0.1:8000/qna"
        console.log(url);
        const response  = await fetch(url,requestOptions);   
        const data=  await response.json();
        if(!response.ok) throw new Error("Something went wrong!");

        // clean and udpate the history with bot response.
        updateHistory(data);

    } catch (error) {
      console.log(error);
    }
  }

  return (
    <div className="container">
      <div className="chatbot-popup">
        <div className="chat-header">
          <div className="header-info">
            <ChatbotIcon />
            <h2 className="logo-text">AI Receptionist</h2>
          </div>
            <button class="material-symbols-rounded">keyboard_arrow_down</button>
        </div>
        {/*  Chat bot body*/}
        <div className="chat-body">
          <div className="message bot-message">
            <ChatbotIcon />
            <p className="message-text">Hi there How can I help you today ?</p>
          </div>


          {chatHistory.map((chat,index)=>(
            <ChatMessage key={index} chat = {chat}/>
          ))}
        
        </div>
        <div className="chat-footer">
          <ChatForms chatHistory = {chatHistory} setChatHistory={setChatHistory} generateBotResponse={generateBotResponse}/>
        </div>
      </div>
    </div>
  );
};

export default App;
