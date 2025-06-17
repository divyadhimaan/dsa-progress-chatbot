import React, { useState } from "react";
import axios from "axios";

function App() {
  const [message, setMessage] = useState("");
  const [chat, setChat] = useState([]);

  const sendMessage = async () => {
    const userMessage = { sender: "You", text: message };
    setChat([...chat, userMessage]);
    const res = await axios.post("http://localhost:5001/api/message", { message }, {
      // withCredentials: false, // set true only if using cookies/auth
      headers: {
        "Content-Type": "application/json"
      }});
    setChat([...chat, userMessage, { sender: "Bot", text: res.data.reply }]);
    setMessage("");
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>DSA Interview Prep Bot</h1>
      <div style={{ marginBottom: "10px" }}>
        {chat.map((msg, i) => (
          <p key={i}><strong>{msg.sender}:</strong> {msg.text}</p>
        ))}
      </div>
      <input
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Ask about your DSA prep..."
        style={{ width: "300px", marginRight: "10px" }}
      />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
}

export default App;
