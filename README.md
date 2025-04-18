# OE0BOT DMR Voicebot (ÖVSV-konform)

## 📡 Beschreibung
OE0BOT ist ein experimenteller KI-Sprachbot für den digitalen Amateurfunkbetrieb über DMR. Er verwendet lokale Spracherkennung und Sprachsynthese ohne AMBE-Hardware.

## ⚙ Funktionen
- 📞 Spracheingabe: Vosk (offline)
- 🔊 Sprachausgabe: Espeak NG oder Piper
- 🔗 Verbindung zu HBLink oder IPSC2 (konfigurierbar)
- 📜 Automatischer Rapport & persönliche Daten aus `config.yaml`
- 🔡 NATO-Buchstabieralphabet für empfangene Rufzeichen
- 🛡 Einhaltung der Amateurfunkrichtlinien (ÖVSV / ITU)

## 🚀 Start
```bash
chmod +x install.sh
./install.sh
python3 oe0bot.py
```

## 👤 Entwickler
Sebastian MADL, Mitglied des ÖVSV
