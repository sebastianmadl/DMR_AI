# README.md – OE0BOT DMR Voicebot (ÖVSV-konform)

## 📡 Beschreibung
OE0BOT ist ein experimenteller KI-Sprachbot für den digitalen Amateurfunkbetrieb über DMR. Er nutzt lokale Spracherkennung (Vosk) und Sprachsynthese (Espeak NG oder Piper), um auf Anrufe auf dem DMR-Netz zu reagieren – ganz ohne AMBE-Hardware oder md380-emu.

## ⚙ Funktionen
- 📞 **Spracheingabe (STT):** Vosk (offline)
- 🔊 **Sprachausgabe (TTS):** Espeak NG (Standard) oder Piper (optional)
- 🔗 **DMR-Anbindung:** Verbindung zu HBLink Master oder IPSC2
- 📜 **Rufzeichen-Erkennung & Antwort** mit Rapport, Name, QTH, Locator & Funkgerät
- 🔡 **Buchstabiert empfangene Rufzeichen** im NATO-Alphabet (optional)
- 🛡 **Amateurfunk-Richtlinien-konform** (ÖVSV / ITU)

## 📝 Beispiel-Antwort
> Hier ist OE0BOT, ein KI-basierter Experimentalfunk-Bot des ÖVSV. Vielen Dank für deinen Anruf, OE1KBC. Rapport ist fünf neun. Mein Operator-Name ist Sebastian, Standort ist Graz, Austria, Locator JN76pp. Mein Funkgerät ist ein TYT MD-UV390. Mikrofon zurück.

## 🛠 Installation
```bash
git clone https://github.com/dein-benutzername/oe0bot.git
cd oe0bot
chmod +x install.sh
./install.sh  # oder ./install.sh --piper für bessere TTS-Stimme
```

## 🚀 Start
```bash
python3 oe0bot.py
```

## 🧾 Konfiguration (`config.yaml`)
```yaml
rufzeichen: "OE0BOT"
hb_server_ip: "127.0.0.1"
hb_server_port: 62031
master_password: "changeme"
talkgroup_rx: 7
talkgroup_tx: 7
timeslot_rx: 2
timeslot_tx: 2
language: "de"
tts_engine: "espeak"  # oder "piper"
phonetic_callsign: true
announce_on_first_contact: true
operator_name: "Sebastian"
qth_city: "Graz"
qth_country: "Austria"
locator: "JN76pp"
rig_model: "TYT MD-UV390"
```

## 👤 Entwickler
Sebastian MADL, Mitglied des ÖVSV

Dieses Projekt dient der Erforschung digitaler Sprachverarbeitung im Amateurfunkdienst.
