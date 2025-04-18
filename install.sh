#!/usr/bin/env bash
set -e
echo "[INFO] Installiere Systemabhängigkeiten..."
sudo apt update
sudo apt install -y python3 python3-pip espeak-ng ffmpeg libespeak-ng1 portaudio19-dev sox git
echo "[INFO] Installiere Python-Pakete..."
pip install vosk PyYAML pyaudio
echo "[INFO] Lade Vosk Sprachmodell (Deutsch)..."
mkdir -p model
cd model
if [ ! -d "vosk-model-small-de-0.15" ]; then
    wget https://alphacephei.com/vosk/models/vosk-model-small-de-0.15.zip
    unzip vosk-model-small-de-0.15.zip
    rm vosk-model-small-de-0.15.zip
fi
cd ..
echo "[INFO] Fertig. Starte den Bot mit: python3 oe0bot.py"
