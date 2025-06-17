import axios from "axios";

export const sendMessage = (message) =>
  axios.post("http://localhost:5000/api/message", { message });
