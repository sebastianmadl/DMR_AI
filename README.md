# DMR AI Voicebot (OE0BOT)

Ein intelligenter DMR-Voicebot, der mit einem HBLink-Master verbunden ist. Der Bot kann auf spezifische Trigger (z.B. "OE0BOT") reagieren und eine Antwort in Form von Text oder Sprache zurückgeben.

## Features

- Direkte Verbindung zum HBLink-Master
- Sprachverarbeitung mit OpenAI GPT-4
- Text-to-Speech (TTS) für Antworten
- Sprach-Erkennung (Speech-to-Text)
- AMBE-Audio-Encoding für die DMR-Kommunikation
- Unterstützt UDP-Audio-Streaming

## Vorraussetzungen

Bevor du den Bot einrichtest, stelle sicher, dass du die folgenden Software-Pakete und Tools installiert hast:

- Python 3.x
- pip (Python Package Manager)
- Git
- Build-Tools (für das Kompilieren von Abhängigkeiten)
- [MMDVM](https://github.com/mbj46/md380-emu) für AMBE-Encoding

## Installation

1. **Clone das Repository**

   Wenn du das Repository von GitHub heruntergeladen hast, entpacke die ZIP-Datei oder klone das Repository:

   ```bash
   git clone https://github.com/yourusername/DMR_AI_Voicebot.git
   cd DMR_AI_Voicebot
