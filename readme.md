# DSA Progress bot

A simple chat interface built with React (Next.js) and Flask/Node.js backend, designed for productivity workflows like daily planning, task marking, and custom bot responses.


## Features
- Chat interface with user and bot message bubbles
- Suggestion buttons for quick interaction (e.g., “What is the plan for today?”)
- API communication with backend using Axios
- Stylish UI with left/right alignment for bot/user
- Dynamic updates with typing placeholders ("...")
- Mobile-responsive layout
- Session based temporary storage
- Persistent memory saved to MongoDb
- Responses with clickable leetcode links
- Using model 
  - Meta LLaMA 3 (llama3-8b-8192): lightweight, fast
  - Meta LLaMA 3 (llama3-70b-8192): very strong

## UI Sample
![Alt text](./images/ui-demo.png)

<!-- ## AI Models
| Model Name        | Description                      |
| ----------------- | -------------------------------- |
| `llama3-8b-8192`  | Meta LLaMA 3 (lightweight, fast) |
| `llama3-70b-8192` | Meta LLaMA 3 (very strong)       |
| `gemma-7b-it`     | Google Gemma (chat tuned)        |
 -->

<!-- ## Flow

┌────────────────────┐
│  User Interface    │ (CLI / Web / Telegram)
└────────┬───────────┘
         ↓
┌────────────────────┐
│  Agent Brain       │ ← System Prompt + Goal Tracking Logic
│  (OpenAI API)      │
└────────┬───────────┘
         ↓
┌────────────────────┐
│  Tools             │
│  - Memory Log      │ ← JSON/DB
│  - DSA Sheet DB    │ ← Local / API
│  - Reminder API    │ ← Optional
└────────────────────┘ -->



<!-- ## Deployments
backend - render (https://dsa-progress-chatbot.onrender.com)
frontend - vercel (https://d-bot-jet.vercel.app/) -->