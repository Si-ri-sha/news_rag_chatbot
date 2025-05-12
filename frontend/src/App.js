import React from 'react';
import ChatScreen from './ChatScreen'; // Import the ChatScreen component
import './App.css'; // Tailwind CSS should already be configured, so this can stay

function App() {
  return (
    <div className="min-h-screen bg-gray-100 flex justify-center items-center">
      <ChatScreen />
    </div>
  );
}

export default App;
