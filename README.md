# WhatsApp LLM Router 🚀

An enterprise-grade, highly resilient WhatsApp AI assistant with a decoupled microservice architecture, automatic LLM failover load-balancing, and native Text-to-Speech (TTS) Voice Note generation.

This project splits the AI logic and the WhatsApp Web socket handling into two separate microservices. This allows you to host the headless WhatsApp connection securely on a lightweight VPS (or Pterodactyl panel) while running the heavy AI compute locally or on a dedicated server.

## Core Features ✨

*   **100% Uptime LLM Routing Engine:** If an AI API key fails or runs out of credits, the system instantly fails over to the next provider in the queue (e.g., Gemini -> Groq -> Mistral).
*   **Native WhatsApp Voice Notes:** The AI can generate actual `.mp3` audio files and send them directly to the user as native WhatsApp voice notes using Microsoft Edge-TTS.
*   **Decoupled Architecture:** 
    *   `text-agent-vps` (NodeJS): Handles the headless WhatsApp Web browser via Puppeteer.
    *   `desktop-voice-agent` (Python/FastAPI): The "Brain Server" handling the AI inference, tool routing, and audio generation.
*   **Multi-Key Load Balancing:** Supply multiple API keys for the same provider to bypass rate limits automatically!

---

## Installation & Setup 🛠️

### Prerequisites
*   Node.js v20+
*   Python 3.11+
*   FFmpeg (Required for sending audio files)

### 1. Configure API Keys
1. Navigate to the `desktop-voice-agent/` directory.
2. Rename `.env.example` to `.env`.
3. Open `.env` and paste your free API keys for Gemini, Groq, or Mistral. (Links to get these keys are provided directly inside the file!).

### 2. Quick Start (Windows)
If you are running both the Brain Server and the Text Agent on the same Windows Desktop, simply double-click the `start_agent.bat` file in the root directory!

This will instantly open two terminals, install all NPM/Pip dependencies automatically, and generate the WhatsApp QR Code on your screen. Scan it with your phone, and your AI is online!

### 3. Advanced VPS Deployment (Linux / Pterodactyl)
If you want to run the WhatsApp connection 24/7 on a VPS:
1. Upload the `text-agent-vps` folder to your server.
2. Ensure you have Google Chrome or Chromium installed on your server (Puppeteer requires this).
3. Run `npm install` followed by `npm start`.
4. Run your `desktop-voice-agent` (The Brain) locally on your PC, and use a tool like Ngrok to expose port `8000`. Update the `TEXT_AGENT_URL` in your `.env` file to point to your VPS IP!

---

## Architecture Flow ⚙️
1. User sends a WhatsApp message.
2. `text-agent-vps` (NodeJS) receives the message and sends it via HTTP POST to the Brain Server.
3. `desktop-voice-agent` (Python) parses the chat history, filters out hallucinated XML tool calls, and passes it to the `LLMRouter`.
4. The router attempts to contact the primary LLM (e.g., Gemini). If it fails, it cascades down the configured `AI_FALLBACK_ORDER` list.
5. If the user asked for a voice message, the Brain Server executes the `send_voice_note` tool using Edge-TTS, saves the `.mp3`, and sends an HTTP POST back to the NodeJS server to transmit the audio file to the user.

---

## Frequently Asked Questions (FAQ) ❓

<details>
<summary><b>My Text Agent crashes with `ENOENT` regarding Chrome/Puppeteer!</b></summary>
<br>
Your server is likely running Alpine Linux (common on Pterodactyl panels). Alpine cannot natively run Puppeteer's Chrome binary without complex workarounds. Ask your host to switch you to a "Node.js Puppeteer" egg, or run the project on a standard Ubuntu VPS or Windows desktop.
</details>

<details>
<summary><b>Why did the AI reply with raw XML like `<change_voice>`?</b></summary>
<br>
Sometimes open-source models (like LLaMA 3.1) leak their internal tool-calling tokens into the final text output. We have built-in Regex filters to scrub this, but if you switch models or providers, you may need to update the regex rules in `app/main.py`.
</details>

<details>
<summary><b>How do I change the default AI voice?</b></summary>
<br>
Inside `desktop-voice-agent/app/main.py`, the default TTS voice is set to `en-US-AvaNeural`. You can easily change this to `en-US-JennyNeural`, `en-US-GuyNeural`, or any other Microsoft Edge TTS voice.
</details>

<details>
<summary><b>Does running this cost money?</b></summary>
<br>
No! The architecture is specifically designed around free, open-source AI providers like Groq, Mistral, and Google Gemini API tiers.
</details>

---

*Engineered with precision for absolute fault tolerance.*
