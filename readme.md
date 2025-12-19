# DSA Interview Assistant 🚀

A personalized DSA interview preparation chatbot powered by AI. The assistant adapts its coaching style based on your experience level (SDE-1, SDE-2, or SDE-3), providing tailored guidance for technical interviews.

## Features

- 🎯 **Three SDE Levels** - Personalized coaching for Entry, Mid, and Senior level interviews
- 🤖 **AI-Powered** - Uses Groq's LLaMA models for intelligent responses
- 💬 **Interactive Chat** - Clean, modern chat interface with markdown support
- 📝 **Session Memory** - Persistent conversation history with MongoDB
- 🎨 **Responsive UI** - Mobile-friendly design built with Next.js
- ⚡ **Fast Responses** - Choose between 70B (powerful) or 8B (fast) models

## How It Works

### 1. Select Your Level

Choose your target interview level from the dropdown:

- **SDE-1 (Entry Level)**: For fresh graduates and early-career engineers
  - Focus: Fundamentals, basic data structures, easy-medium problems
  - Topics: Arrays, Strings, Linked Lists, Stacks, Queues, Basic Trees/Graphs
  - Style: Patient, beginner-friendly with step-by-step explanations
  
- **SDE-2 (Mid Level)**: For experienced engineers (2-5 years)
  - Focus: Advanced algorithms, optimization, medium-hard problems
  - Topics: Dynamic Programming, Advanced Graphs, System Design basics
  - Style: Technical discussions with trade-offs and complexity analysis
  
- **SDE-3 (Senior Level)**: For senior engineers and tech leads
  - Focus: Expert algorithms, distributed systems, architecture
  - Topics: Advanced DP, Network Flow, Scalability, Production systems
  - Style: Expert-level discussions with architectural considerations

### 2. Persona System

Each level has a unique AI persona that adapts:

**SDE-1 Persona:**
```
- Explains concepts with analogies and real-world examples
- Breaks down problems into smaller steps
- Provides hints before full solutions
- Celebrates progress and encourages learning
```

**SDE-2 Persona:**
```
- Discusses multiple solutions and their trade-offs
- Focuses on time/space optimization
- Connects problems to real-world scenarios
- Assumes solid CS fundamentals
```

**SDE-3 Persona:**
```
- Expects optimal solutions from the start
- Discusses scalability and distributed systems
- Analyzes worst-case scenarios and failure modes
- Provides production-ready insights
```

### 3. Conversation Flow

```
User selects SDE level → Frontend sends request with level parameter
                                    ↓
Backend receives level → Loads appropriate persona from simple_agent.py
                                    ↓
Groq API processes → Returns tailored response based on level
                                    ↓
Response displayed → Conversation saved to MongoDB
```

### 4. Session Management

- Each chat session gets a unique ID stored in browser's sessionStorage
- Conversations are persisted to MongoDB for history
- Click "New Chat" to start fresh (clears current session)
- Previous conversations are automatically loaded on page refresh

## Tech Stack

### Frontend
- **Next.js 14** - React framework with TypeScript
- **Tailwind CSS** - Utility-first styling
- **React Markdown** - Render formatted responses
- **Axios** - HTTP client for API calls
- **Notistack** - Toast notifications

### Backend
- **Flask** - Python web framework
- **Groq API** - LLaMA 3.3 (70B) and LLaMA 3.1 (8B) models
- **MongoDB** - Conversation persistence
- **Python-dotenv** - Environment configuration

## Getting Started

### Prerequisites
- Node.js 18+
- Python 3.8+
- MongoDB instance (local or Atlas)
- Groq API key ([Get one here](https://console.groq.com))

### Environment Setup

Create a `.env` file in the root directory:

```env
# Groq API Key (Required)
GROQ_API_KEY=your_groq_api_key_here

# MongoDB Connection (Required)
MONGODB_URI=your_mongodb_connection_string

# Backend Port (Optional, defaults to 5001)
BACKEND_PORT=5001
```

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd progress-tracker
```

2. **Install frontend dependencies**
```bash
cd frontend
npm install
```

3. **Install backend dependencies**
```bash
cd ../backend
pip install -r requirements.txt
```

### Running the Application

1. **Start the backend** (from project root):
```bash
python3 backend/app.py
```
Backend will run on `http://localhost:5001`

2. **Start the frontend** (in a new terminal):
```bash
cd frontend
npm run dev
```
Frontend will run on `http://localhost:3000`

3. **Open your browser** and navigate to `http://localhost:3000`

## Usage Examples

### For SDE-1 (Entry Level)
```
You: "Explain how to solve Two Sum"
Bot: Breaks down the problem step-by-step, explains hash map approach 
     with simple examples, discusses time complexity in beginner terms
```

### For SDE-2 (Mid Level)
```
You: "What are the key patterns for SDE interviews?"
Bot: Discusses advanced patterns (sliding window, two pointers, DP),
     provides complexity analysis, suggests optimization techniques
```

### For SDE-3 (Senior Level)
```
You: "How would you design a distributed rate limiter?"
Bot: Discusses system design considerations, scalability trade-offs,
     production-ready solutions with failure handling
```

## API Endpoints

### POST `/api/message`
Send a message to the chatbot

**Request Body:**
```json
{
  "message": "Explain binary search",
  "level": "SDE1",
  "model": "llama-3.3-70b-versatile",
  "session_id": "uuid-string"
}
```

**Response:**
```json
{
  "reply": {
    "status": "ok",
    "message": "Binary search is a divide-and-conquer algorithm..."
  }
}
```

### GET `/api/memory?session_id=xxx`
Retrieve conversation history for a session

### POST `/api/clear?session_id=xxx`
Clear conversation history for a session

### GET `/healthy`
Health check endpoint

## Project Structure

```
progress-tracker/
├── backend/
│   ├── app.py                 # Flask application & routes
│   ├── simple_agent.py        # AI agent with SDE personas
│   ├── logger.py              # Session logging & MongoDB
│   ├── progress_store.py      # Progress data management
│   └── requirements.txt       # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   └── chat/
│   │   │       └── page.tsx   # Main chat interface
│   │   └── utils/
│   │       └── session.ts     # Session management
│   ├── public/                # Static assets
│   └── package.json           # Node dependencies
└── README.md
```

## Customization

### Modify Personas

Edit `backend/simple_agent.py` to customize the coaching style for each level:

```python
SDE_PERSONAS = {
    "SDE1": """Your custom SDE-1 persona here...""",
    "SDE2": """Your custom SDE-2 persona here...""",
    "SDE3": """Your custom SDE-3 persona here..."""
}
```

### Add More Levels

1. Add a new persona in `simple_agent.py`
2. Add the level to the `levels` array in `frontend/src/app/chat/page.tsx`
3. Restart both frontend and backend

### Change Models

Update the `models` array in `frontend/src/app/chat/page.tsx` with any Groq-supported model.

## Deployment

### Backend (Render/Railway/Heroku)
1. Set environment variables (GROQ_API_KEY, MONGODB_URI)
2. Deploy the `backend` directory
3. Use `gunicorn` for production: `gunicorn app:app`

### Frontend (Vercel/Netlify)
1. Set `NEXT_PUBLIC_API_BASE_URL` to your backend URL
2. Deploy the `frontend` directory
3. Build command: `npm run build`
4. Output directory: `.next`

## Troubleshooting

**Backend won't start:**
- Check if port 5001 is already in use: `lsof -i :5001`
- Verify MongoDB connection string
- Ensure GROQ_API_KEY is set

**Frontend can't connect:**
- Verify backend is running on port 5001
- Check CORS settings in `backend/app.py`
- Ensure `baseUrl` in frontend matches backend URL

**Model errors:**
- Verify you're using supported Groq models
- Check API key is valid
- Review Groq API quotas

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License - feel free to use this project for your interview preparation!

---

**Happy Coding! May your interviews be bug-free! 🐛✨**