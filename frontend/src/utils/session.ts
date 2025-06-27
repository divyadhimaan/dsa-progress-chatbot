export function getOrCreateSessionId() {
    let sessionId = localStorage.getItem("dsa_session_id");
    if (!sessionId) {
      sessionId = crypto.randomUUID(); // or use a custom UUID function
      localStorage.setItem("dsa_session_id", sessionId);
    }
    return sessionId;
  }
  