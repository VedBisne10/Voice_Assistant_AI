# Nova — Desktop Voice Assistant

Nova is a fully local, offline-capable voice assistant that runs on your machine. You talk, Nova listens, understands what you want, and either responds or takes action — opening apps, searching the web, managing files, controlling your system, and more. No cloud dependency for the AI brain. Everything runs on your own hardware using Ollama.

---

## Demo

> 📹 **[Watch Demo](#)**
> *https://drive.google.com/file/d/1hkMB6Hb76cYejylA1XRdcrGqfyc9Iejd/view?usp=sharing*

---

## Features

- 🎙️ **Voice Input** — Captures your voice from the mic and transcribes it using Faster Whisper
- 🧠 **Local AI** — Powered by Gemma3:12b running through Ollama — no API key, no internet needed for the AI
- 🔊 **Natural Voice Output** — Speaks responses using ElevenLabs neural TTS (high quality, no robotic sound)
- 💾 **Memory** — Remembers facts about you across sessions (name, preferences, ongoing projects)
- 📜 **Conversation History** — Keeps track of recent messages so responses stay in context
- ⚡ **Action System** — Can perform real tasks on your computer when you ask
  - Open apps and games
  - Search the web
  - Open websites
  - Compose emails in Gmail
  - Open folders and files
  - Find files by name
  - Get current time and date
  - Take screenshots
  - Control system volume
  - Lock screen, shutdown, restart

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Speech to Text** | [Faster Whisper](https://github.com/SYSTRAN/faster-whisper) (small model, CPU, int8) |
| **AI / LLM** | [Gemma3:12b](https://ollama.com/library/gemma3) via [Ollama](https://ollama.com) |
| **Text to Speech** | [ElevenLabs](https://elevenlabs.io) (eleven_turbo_v2_5) |
| **Audio Playback** | Windows Media Foundation via PowerShell |
| **Audio Recording** | [SoundDevice](https://python-sounddevice.readthedocs.io) + [SoundFile](https://python-soundfile.readthedocs.io) |
| **Memory Storage** | JSON files (local disk) |
| **Environment Variables** | [python-dotenv](https://pypi.org/project/python-dotenv) |
| **HTTP Requests** | [Requests](https://requests.readthedocs.io) |
| **Language** | Python 3.10+ |
| **Platform** | Windows |

---

## Project Structure

```
VoiceAssistant/
│
├── app.py                          # entry point, starts Nova
│
├── assistant/
│   ├── orchestrator.py             # main loop, connects everything
│   ├── listener.py                 # records mic audio
│   ├── transcriber.py              # converts audio to text
│   └── speaker.py                  # converts text to speech
│
├── ai/
│   ├── local_llm_client.py         # talks to Ollama
│   ├── memory_manager.py           # saves/loads memory and chat history
│   └── tool_router.py              # detects and runs tool calls from AI
│
├── actions/
│   ├── app_actions.py              # opening apps and games
│   ├── browser_actions.py          # web search, websites, Gmail
│   ├── file_actions.py             # folders, files, search
│   ├── system_actions.py           # time, date, screenshot, volume, lock, shutdown
│   └── utility_actions.py          # AI-powered: email drafts, summaries, translation
│
├── config/
│   ├── settings.py                 # all configurable settings in one place
│   └── constants.py                # file paths and system prompt
│
├── utils/
│   ├── logger.py                   # shared logger
│   └── file_helper.py              # read/write JSON helpers
│
├── data/
│   ├── memory.json                 # stored user facts
│   └── conversation_history.json   # recent chat messages
│
├── requirements.txt
└── .env                            # API keys (not committed to git)
```

---

## Setup Guide

### Prerequisites

- Windows 10 or 11
- Python 3.10 or higher
- [Ollama](https://ollama.com/download) installed
- A microphone
- An [ElevenLabs](https://elevenlabs.io) account (free tier gives 10,000 characters/month)

---

### Step 1 — Clone the repo

```bash
git clone https://github.com/VedBisne10/VoiceAssistant.git
cd VoiceAssistant
```

---

### Step 2 — Create a virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

---

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
pip install elevenlabs
```

---

### Step 4 — Pull the AI model via Ollama

Make sure Ollama is installed, then pull the model:

```bash
ollama pull gemma3:12b
```

> This is a ~8GB download. Once pulled it runs fully offline.

Start the Ollama server (keep this running in a separate terminal):

```bash
ollama serve
```

---

### Step 5 — Add your ElevenLabs API key

Create a `.env` file in the project root (or edit the existing one):

```
ELEVENLABS_API_KEY=your_api_key_here
```

Get your key from: [elevenlabs.io/app/settings/api-keys](https://elevenlabs.io/app/settings/api-keys)

---

### Step 6 — Configure your apps and folders

Open `actions/app_actions.py` and add the paths to the apps you want Nova to open:

```python
APPS = {
    "chrome":   r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "spotify":  r"C:\Users\YourName\AppData\Roaming\Spotify\Spotify.exe",
    # add more here
}
```

Open `actions/file_actions.py` and add your folder shortcuts:

```python
FOLDERS = {
    "desktop":   r"C:\Users\YourName\Desktop",
    "downloads": r"C:\Users\YourName\Downloads",
    # add more here
}
```

---

### Step 7 — (Optional) Change the voice

Nova uses the **George** voice by default. To use a different ElevenLabs voice:

1. Go to [elevenlabs.io/app/voice-lab](https://elevenlabs.io/app/voice-lab)
2. Find a voice you like and copy its ID
3. Open `config/settings.py` and update:

```python
ELEVENLABS_VOICE_ID = "your_voice_id_here"
```

---

### Step 8 — Run Nova

```bash
python app.py
```

Nova will start listening. Speak naturally — she'll respond or take action based on what you say.

---

## Usage Examples

| What you say | What Nova does |
|---|---|
| `"Open Chrome"` | Launches Chrome |
| `"Search for the weather in London"` | Opens Google with that search |
| `"Open my downloads folder"` | Opens Downloads in File Explorer |
| `"What time is it"` | Says the current time |
| `"Take a screenshot"` | Saves a screenshot to your Desktop |
| `"Set volume to 50"` | Sets system volume to 50% |
| `"Lock my screen"` | Locks Windows |
| `"Write an email to John about the meeting tomorrow"` | Drafts an email and opens Gmail |
| `"Goodbye Nova"` | Ends the conversation |

---

## Stopping Nova

Say any of these to end the session:

- `"Goodbye Nova"`
- `"End conversation"`
- `"Stop conversation"`
- `"Exit"`

Or press `Ctrl+C` in the terminal.

---

## Notes

- Nova listens for **5 seconds** per turn. If you get cut off, you can increase `duration` in `assistant/listener.py`
- The AI model (Gemma3:12b) requires around **8GB of RAM** to run comfortably
- ElevenLabs free tier has **10,000 characters/month** — about 7-10 minutes of speech
- All memory and conversation history is stored locally in the `data/` folder

---

## License

MIT License — see [LICENSE](LICENSE)
