# oe0bot.py – Hauptprogramm des DMR Voicebots ohne AMBE
import yaml
import time

def buchstabiere_rufzeichen(callsign):
    nato = {
        "A": "Alfa", "B": "Bravo", "C": "Charlie", "D": "Delta", "E": "Echo", "F": "Foxtrot",
        "G": "Golf", "H": "Hotel", "I": "India", "J": "Juliett", "K": "Kilo", "L": "Lima",
        "M": "Mike", "N": "November", "O": "Oscar", "P": "Papa", "Q": "Quebec", "R": "Romeo",
        "S": "Sierra", "T": "Tango", "U": "Uniform", "V": "Victor", "W": "Whiskey", "X": "X-ray",
        "Y": "Yankee", "Z": "Zulu", "0": "Zero", "1": "One", "2": "Two", "3": "Three",
        "4": "Four", "5": "Five", "6": "Six", "7": "Seven", "8": "Eight", "9": "Nine"
    }
    return " ".join([nato.get(c.upper(), c) for c in callsign])

def lade_konfiguration():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

def generiere_antwort(config, anrufer):
    antwort = f"Hier ist {config['rufzeichen']}, ein KI-basierter Experimentalfunk-Bot des ÖVSV."
    if config.get("announce_on_first_contact", True):
        antwort += f" Dieses Projekt dient der Erforschung digitaler Sprachverarbeitung im Amateurfunk."
    antwort += f" Vielen Dank für deinen Anruf, {anrufer}. Rapport ist fünf neun."
    antwort += f" Mein Operator-Name ist {config['operator_name']}, Standort ist {config['qth_city']}, {config['qth_country']}, Locator {config['locator']}."
    antwort += f" Mein Funkgerät ist ein {config['rig_model']}."
    if config.get("phonetic_callsign", False):
        antwort += f" Dein Rufzeichen buchstabiert: {buchstabiere_rufzeichen(anrufer)}."
    antwort += " Mikrofon zurück."
    return antwort

def main():
    config = lade_konfiguration()
    print("[DMR] Voicebot gestartet. Warte auf CQ...")

    while True:
        anrufer = "OE1KBC"
        print(f"[DMR] Anruf empfangen von {anrufer}")
        antwort = generiere_antwort(config, anrufer)
        print(f"[BOT] Antwort: {antwort}")
        time.sleep(10)

if __name__ == "__main__":
    main()
