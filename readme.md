


## Flow

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
└────────────────────┘
