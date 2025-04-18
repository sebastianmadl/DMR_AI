#!/usr/bin/env python3
# oe0bot.py – DMR Voicebot (ÖVSV-konform)

import socket
import yaml
import time
import os
import threading
import subprocess
from vosk import Model, KaldiRecognizer
import pyaudio

# Konfiguration laden
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

CALLSIGN = config.get("rufzeichen", "OE0BOT")
PHONETIC = config.get("phonetic_callsign", True)
LANGUAGE = config.get("language", "de")
TTS_ENGINE = config.get("tts_engine", "espeak")
FIRST_CONTACT_ANNOUNCE = config.get("announce_on_first_contact", True)

OPERATOR = config.get("operator_name", "Sebastian")
QTH_CITY = config.get("qth_city", "Graz")
QTH_COUNTRY = config.get("qth_country", "Austria")
LOCATOR = config.get("locator", "JN76pp")
RIG_MODEL = config.get("rig_model", "TYT MD-UV390")

HB_SERVER = config.get("hb_server_ip", "127.0.0.1")
HB_PORT = config.get("hb_server_port", 62031)

# Audio Input vorbereiten (Vosk)
model = Model(lang=LANGUAGE)
recognizer = KaldiRecognizer(model, 16000)
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

# Begrüßung nur einmal pro Session
first_contact_done = False

def speak(text):
    if TTS_ENGINE == "espeak":
        subprocess.run(["espeak-ng", "-v", LANGUAGE, text])
    elif TTS_ENGINE == "piper":
        subprocess.run(["piper", "--text", text])


def to_phonetic(callsign):
    nato = {
        'A': 'Alfa', 'B': 'Bravo', 'C': 'Charlie', 'D': 'Delta', 'E': 'Echo', 'F': 'Foxtrot',
        'G': 'Golf', 'H': 'Hotel', 'I': 'India', 'J': 'Juliett', 'K': 'Kilo', 'L': 'Lima',
        'M': 'Mike', 'N': 'November', 'O': 'Oscar', 'P': 'Papa', 'Q': 'Quebec', 'R': 'Romeo',
        'S': 'Sierra', 'T': 'Tango', 'U': 'Uniform', 'V': 'Victor', 'W': 'Whiskey', 'X': 'X-ray',
        'Y': 'Yankee', 'Z': 'Zulu', '0': 'Zero', '1': 'One', '2': 'Two', '3': 'Three',
        '4': 'Four', '5': 'Five', '6': 'Six', '7': 'Seven', '8': 'Eight', '9': 'Nine'
    }
    return ' '.join(nato.get(char.upper(), char) for char in callsign)


def handle_call(caller):
    global first_contact_done

    if PHONETIC:
        spelled = to_phonetic(caller)
        speak(f"Rufzeichen erkannt: {spelled}.")

    if FIRST_CONTACT_ANNOUNCE and not first_contact_done:
        speak("Hier ist OE0BOT, ein KI-basierter Experimentalfunk-Bot des ÖVSV, entwickelt von Sebastian MADL. Dieses Projekt dient der Erforschung digitaler Sprachverarbeitung im Amateurfunk.")
        first_contact_done = True

    speak(f"Vielen Dank für deinen Anruf, {caller}. Rapport ist fünf neun. Mein Operator-Name ist {OPERATOR}, Standort ist {QTH_CITY}, {QTH_COUNTRY}, Locator {LOCATOR}. Mein Funkgerät ist ein {RIG_MODEL}. Mikrofon zurück.")


def receive_loop():
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            if CALLSIGN.lower() in result.lower():
                # Extrahiere Rufzeichen aus dem Satz (vereinfachte Annahme)
                words = result.lower().split()
                for i, word in enumerate(words):
                    if word == CALLSIGN.lower() and i >= 1:
                        caller = words[i - 1].upper()
                        handle_call(caller)


def connect_to_hblink():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HB_SERVER, HB_PORT))
        print(f"[INFO] Verbunden mit HBLink Master bei {HB_SERVER}:{HB_PORT}")
        # Placeholder – Datenstrom hier integrieren wenn nötig
    except Exception as e:
        print(f"[ERROR] Verbindung fehlgeschlagen: {e}")


if __name__ == "__main__":
    print("[INFO] OE0BOT Voicebot gestartet.")
    threading.Thread(target=receive_loop, daemon=True).start()
    connect_to_hblink()
    while True:
        time.sleep(1)
