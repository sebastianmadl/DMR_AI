
import yaml
import time
import socket
import sounddevice as sd
import numpy as np
import subprocess
from vosk import Model, KaldiRecognizer
import json


def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)


def speak(text, config):
    print("[TTS]", text)
    if config["tts_engine"] == "espeak":
        subprocess.run(["espeak", "-v", config["language"], text])
    else:
        print("[WARN] TTS engine not supported.")


def callsign_to_phonetic(callsign):
    icao = {
        'A': "Alpha", 'B': "Bravo", 'C': "Charlie", 'D': "Delta",
        'E': "Echo", 'F': "Foxtrot", 'G': "Golf", 'H': "Hotel",
        'I': "India", 'J': "Juliett", 'K': "Kilo", 'L': "Lima",
        'M': "Mike", 'N': "November", 'O': "Oscar", 'P': "Papa",
        'Q': "Quebec", 'R': "Romeo", 'S': "Sierra", 'T': "Tango",
        'U': "Uniform", 'V': "Victor", 'W': "Whiskey", 'X': "X-ray",
        'Y': "Yankee", 'Z': "Zulu",
        '0': "Zero", '1': "One", '2': "Two", '3': "Three",
        '4': "Four", '5': "Five", '6': "Six", '7': "Seven",
        '8': "Eight", '9': "Nine"
    }
    return ' '.join(icao.get(c.upper(), c) for c in callsign)


def generate_rapport(config, callsign):
    rapport = f"{callsign}, hier ist {config['rufzeichen']} mit einem Rapport 5 9."
    if config.get("phonetic_callsign"):
        rapport += f" {callsign_to_phonetic(callsign)}."
    rapport += f" Mein Name ist {config['operator_name']}, QTH ist {config['qth_city']}, {config['qth_country']}, Locator {config['locator']}."
    rapport += f" Ich benutze ein {config['rig_model']}."
    return rapport


def recognize_speech(callback, config):
    model = Model(lang=config['language'])
    rec = KaldiRecognizer(model, 16000)
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=lambda indata, frames, time, status: None):
        print("[INFO] Sprachsteuerung aktiv...")
        while True:
            data = sd.rec(4000, samplerate=16000, channels=1, dtype='int16')
            sd.wait()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                if result.get("text"):
                    callback(result["text"])


def handle_command(text, config):
    print("[Speech]", text)
    if config['rufzeichen'].lower() in text.lower():
        words = text.lower().split()
        for w in words:
            if w.startswith("oe") or w.startswith("dl"):
                callsign = w.upper()
                rapport = generate_rapport(config, callsign)
                speak(rapport, config)
                return
    elif "wer hat dich" in text.lower() and "entwickelt" in text.lower():
        speak(f"Ich wurde entwickelt von {config['developer']}", config)


def main():
    config = load_config()
    recognize_speech(lambda text: handle_command(text, config), config)


if __name__ == "__main__":
    main()
