import yaml
import requests
import time
import pyaudio
import speech_recognition as sr
from espeakng import ESpeakNG

# Konfiguration laden
with open('config.yaml', 'r') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

# TTS-Setup
tts = ESpeakNG()
tts.voice = 'de'  # Sprache auf Deutsch setzen
tts.speed = 150   # Geschwindigkeit anpassen

# Funktionen für TTS
def speak(text):
    tts.say(text)

# Funktionen für STT
def listen():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    
    with microphone as source:
        print("Höre auf einen Befehl...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        
    try:
        print("Erkenne Sprache...")
        command = recognizer.recognize_google(audio, language='de-DE')
        print(f"Verstanden: {command}")
        return command
    except sr.UnknownValueError:
        print("Konnte die Sprache nicht verstehen.")
        return None
    except sr.RequestError:
        print("Fehler bei der Anfrage an die STT-API.")
        return None

# Verbindung zu HBLink
def connect_to_hblink():
    url = f"http://{config['hb_server_ip']}:{config['hb_server_port']}/api/"
    headers = {'Authorization': f"Bearer {config['master_password']}"}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print("Erfolgreich mit HBLink verbunden.")
    else:
        print("Verbindung zu HBLink fehlgeschlagen.")
        time.sleep(5)  # Versuchen, alle 5 Sekunden erneut zu verbinden

# Empfang und Senden von Nachrichten
def handle_message(message):
    # Hier kannst du den Empfang von DMR-Nachrichten implementieren und die Ausgabe an den Bot weiterleiten
    print(f"Nachricht empfangen: {message}")
    speak(f"Nachricht erhalten: {message}")

# Hauptlogik
def main():
    while True:
        # Verbindung zum HBLink-Server herstellen
        connect_to_hblink()

        # Warten auf eine Nachricht oder einen Befehl
        command = listen()

        if command:
            if "beenden" in command:
                speak("Bot wird beendet.")
                break
            elif "Rapport" in command:
                speak(f"Rapport fünf neun.")
            else:
                # Senden von Nachrichten (Beispiel)
                handle_message(command)

if __name__ == "__main__":
    main()
