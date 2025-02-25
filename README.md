# 🦆 Pato Bot

Pato Bot is a versatile Discord bot that provides multiple functionalities, including trivia games, music playback, memes, and voice channel management. Built using **Discord.py**, this bot enhances your Discord server experience with fun and interactive commands.

---

## 🚀 Features

### 🎮 Trivia Game

- Play trivia with easy or hard questions
- Randomized questions from a predefined database
- Tracks player scores and announces the winner

### 🎵 Music Player

- Join and leave voice channels
- Play, pause, stop, and resume music from YouTube
- Uses **FFmpeg** and **youtube-dl** for streaming

### 🤣 Meme Generator

- Fetches random memes from Reddit (`r/memes`)
- Ensures fresh, non-stickied posts for entertainment

### 🔊 Voice Channel Manager

- Join and leave voice channels
- Speak text messages in multiple languages using TTS

### 📜 Custom Help Command

- Provides an organized list of available commands

---

## 🛠 Installation

### 1️⃣ Prerequisites

Ensure you have the following installed:

- Python 3.13+
- FFmpeg
- Required Python libraries

### 2️⃣ Clone the Repository

```sh
git clone https://github.com/yourusername/project_pato.git
cd project_pato
```

### 3️⃣ Install Dependencies

```sh
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables

Create a `.env` file and add your bot token and API keys:

```
DISCORD_TOKEN=your-bot-token
REDDIT_CLIENT_ID=your-client-id
REDDIT_CLIENT_SECRET=your-client-secret
REDDIT_USER_AGENT=your-user-agent
```

### 5️⃣ Run the Bot

```sh
python main.py
```

---

## 📜 Commands

| Command                    | Description             |
|----------------------------|-------------------------|
| `!commands`                | Show available commands |
| `!start_trivia easy/hard`  | Start a trivia game     |
| `!answer <text>`           | Answer in the game      |
| `!stop_trivia`             | End a trivia game       |
| `!meme`                    | Get a random meme       |
| `!music play <URL>`        | Play music from YouTube |
| `!stop`                    | Stop music              |
| `!join`                    | Join voice channel      |
| `!leave`                   | Leave voice channel     |
| `!speak <language> <text>` | Convert text to speech  |

---

## 🎯 Contributing

1. Fork the repository
2. Create a new branch (`feature/new-feature`)
3. Commit changes and push to GitHub
4. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License**.

---
