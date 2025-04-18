import socket
import threading
import yaml
import time
import subprocess
from pathlib import Path

# --- Konfiguration laden ---
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

hblink_cfg = config.get("hblink", {})
bot_cfg = config.get("bot", {})
paths = config.get("paths", {})
mmdvm_cfg = config.get("mmdvm", {})

MASTER_IP = hblink_cfg.get("master_ip")
MASTER_PORT = hblink_cfg.get("master_port")
CALLSIGN = hblink_cfg.get("peer_callsign", "OE0BOT")
TG_RX = int(hblink_cfg.get("talkgroup_rx", 7))
TS_RX = int(hblink_cfg.get("timeslot_rx", 2))

TRIGGER_WORDS = [CALLSIGN.lower(), "cq", "an "+CALLSIGN.lower(), CALLSIGN.lower()+" von"]

# --- UDP-Verbindung zum HBLink-Master ---
def listen_to_hblink():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", MASTER_PORT))
    print(f"[HBLink] Lausche auf {MASTER_PORT} ...")
    while True:
        data, addr = sock.recvfrom(1024)
        if not data:
            continue

        # Dummy-Paketverarbeitung: Nur Trigger-Beispiel
        audio_sample = data  # TODO: richtige DMR-Decodierung

        if CALLSIGN.encode() in data:
            print("[Trigger] OE0BOT wurde gerufen.")
            handle_trigger(audio_sample)

# --- Trigger behandeln ---
def handle_trigger(audio_data):
    print("[Audio] Empfange und speichere Audio zur Verarbeitung ...")
    with open(paths["input_audio"], "wb") as f:
        f.write(audio_data)

    # Schritt 1: STT (Whisper)
    transcript = transcribe_audio(paths["input_audio"])
    print(f"[Transkript] {transcript}")

    # Schritt 2: GPT-Antwort
    reply = ask_gpt(transcript)
    print(f"[Antwort] {reply}")

    # Schritt 3: TTS-Ausgabe
    synthesize(reply)

    # Schritt 4: AMBE kodieren
    encode_ambe(paths["output_audio_wav"], paths["output_audio_ambe"])

    # Schritt 5: Sende AMBE-Daten an HBLink oder UART
    send_audio(paths["output_audio_ambe"])

# --- Spracherkennung ---
def transcribe_audio(path):
    return "Dies ist eine Beispielantwort."

# --- GPT ---
def ask_gpt(text):
    return f"Hallo OM, du hast gesagt: '{text}' — ich bin OE0BOT."

# --- TTS ---
def synthesize(text):
    print(f"[TTS] Text-to-Speech für: {text}")
    with open(paths["output_audio_wav"], "wb") as f:
        f.write(b"WAV-Dummy")

# --- AMBE ---
def encode_ambe(input_wav, output_amb):
    print(f"[AMBE] Kodiere {input_wav} nach {output_amb}")
    subprocess.run([
        mmdvm_cfg["ambe_encoder_path"],
        "-i", input_wav,
        "-o", output_amb
    ])

# --- Audio senden ---
def send_audio(ambe_file):
    with open(ambe_file, "rb") as f:
        data = f.read()
    # Dummy: Wir senden an UART oder an einen definierten Port
    print(f"[SEND] Sende {len(data)} Bytes AMBE an MMDVM oder HBLink")

if __name__ == "__main__":
    listener = threading.Thread(target=listen_to_hblink)
    listener.start()
    print("[Bot] OE0BOT gestartet.")
