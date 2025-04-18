#!/bin/bash

# System vorbereiten
echo "Installiere notwendige Pakete..."
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv build-essential git libsndfile1

# Virtuelle Umgebung erstellen
python3 -m venv venv
source venv/bin/activate

# Abhängigkeiten installieren
pip install -r requirements.txt

# Piper-Modell und AMBE Encoder herunterladen
mkdir -p piper_models
cd piper_models
wget https://huggingface.co/espnet/kan-bayashi_ljspeech_tts_train_tacotron2_raw_phn_tacotron2/1?download -O de-thorsten.onnx

cd ..
git clone https://github.com/mbj46/md380-emu.git
cd md380-emu
make

# Konfiguration prüfen
echo "Prüfe config.yaml..."
if [ ! -f config.yaml ]; then
    echo "Fehler: config.yaml nicht gefunden!"
    exit 1
fi

echo "Installation abgeschlossen!"
