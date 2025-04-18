#!/bin/bash
# Installation script for DMR AI Voicebot

echo "Updating system..."
sudo apt update && sudo apt upgrade -y

echo "Installing dependencies..."
sudo apt install -y python3 python3-pip espeak ffmpeg git

echo "Installing Python packages..."
pip3 install vosk pyyaml sounddevice numpy

echo "Creating config.yaml..."
cat <<EOF > config.yaml
rufzeichen: "OE0BOT"
dmr_id: "2320999"
hb_server_ip: "127.0.0.1"
hb_server_port: 62031
master_password: "changeme"
talkgroup_rx: 7
talkgroup_tx: 7
timeslot_rx: 2
timeslot_tx: 2
language: "de"
tts_engine: "espeak"
phonetic_callsign: true
operator_name: "Sebastian"
qth_city: "Graz"
qth_country: "Austria"
locator: "JN76pp"
rig_model: "TYT MD-UV390"
developer: "Sebastian MADL, ÖVSV Mitglied"
EOF

echo "Done. Run 'python3 oe0bot.py' to start the bot."
