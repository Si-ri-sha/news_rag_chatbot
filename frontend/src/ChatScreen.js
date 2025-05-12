import React, { useState } from "react";

const ChatScreen = () => {
  const [messages, setMessages] = useState([]);
  const [userInput, setUserInput] = useState("");

  // Function to fetch the bot's response from the backend
  const fetchBotResponse = async (userQuery) => {
    try {
      const response = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          session_id: "default-session", // or generate one dynamically
          message: userQuery,
        }),
      });

      const data = await response.json();
      console.log("Backend response:", data);
      return data.answer;
    } catch (error) {
      console.error("Error fetching bot response:", error);
      return "Sorry, there was an issue with the bot.";
    }
  };

  // Function to handle sending a message
  const handleSendMessage = async () => {
    const userMessage = { text: userInput, sender: "user" };
    setMessages((prevMessages) => [...prevMessages, userMessage]); // Add user message
    setUserInput(""); // Clear the input field

    // Placeholder for bot response with animation class
    const botMessage = { text: "Fetching response...", sender: "bot", typing: true };
    setMessages((prevMessages) => [...prevMessages, botMessage]);

    // Fetch the bot's response from the backend
    const botResponse = await fetchBotResponse(userInput);

    // Update the chat with the actual bot response
    setMessages((prevMessages) => [
      ...prevMessages.slice(0, -1), // Remove the placeholder message
      { text: botResponse, sender: "bot" }, // Add the actual bot response
    ]);
  };

  // Function to reset chat session
  const handleReset = () => {
    setMessages([]); // Clear the chat history
  };

  return (
    <div className="w-full max-w-2xl mx-auto bg-white p-6 rounded-lg shadow-lg">
      <div className="overflow-y-auto max-h-96">
        <div className="space-y-4">
          {messages.map((msg, index) => (
            <div key={index} className={msg.sender === "user" ? "text-right" : "text-left"}>
              <div
                className={`inline-block p-2 rounded-lg ${
                  msg.sender === "user" ? "bg-blue-500 text-white" : "bg-gray-300"
                } ${msg.typing ? "animate-pulse" : ""}`}
              >
                {msg.text}
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="flex mt-4 space-x-4">
        <input
          type="text"
          value={userInput}
          onChange={(e) => setUserInput(e.target.value)}
          className="flex-1 p-2 border border-gray-300 rounded-lg"
          placeholder="Type your message..."
        />
        <button
          onClick={handleSendMessage}
          className="px-4 py-2 bg-blue-500 text-white rounded-lg"
        >
          Send
        </button>
      </div>

      <button
        onClick={handleReset}
        className="mt-4 w-full py-2 bg-red-500 text-white rounded-lg"
      >
        Reset Session
      </button>
    </div>
  );
};

export default ChatScreen;
