#!/usr/bin/env bash
# install.sh – Installiert Abhängigkeiten für OE0BOT Voicebot

set -e

echo "[INFO] Installiere Systemabhängigkeiten..."
sudo apt update
sudo apt install -y python3 python3-pip espeak-ng ffmpeg libespeak-ng1 portaudio19-dev sox git

if [[ "$1" == "--piper" ]]; then
    echo "[INFO] Installiere Piper (TTS)..."
    pip install piper-tts
else
    echo "[INFO] Verwende Espeak NG als TTS"
fi

echo "[INFO] Installiere Python-Abhängigkeiten..."
pip install vosk PyYAML pyaudio

# Vosk Sprachmodell (Deutsch, ca. 50 MB)
echo "[INFO] Lade Vosk Sprachmodell (Deutsch)..."
mkdir -p model
cd model
if [ ! -d "vosk-model-small-de-0.15" ]; then
    wget https://alphacephei.com/vosk/models/vosk-model-small-de-0.15.zip
    unzip vosk-model-small-de-0.15.zip
    rm vosk-model-small-de-0.15.zip
fi
cd ..

echo "[INFO] Installation abgeschlossen. Starte den Bot mit:"
echo "    python3 oe0bot.py"
