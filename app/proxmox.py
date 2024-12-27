from proxmoxer import ProxmoxAPI
from dotenv import load_dotenv
import os

# Umgebungsvariablen laden
load_dotenv()

# Zugangsdaten aus .env-Datei
PROXMOX_HOST = os.getenv("PROXMOX_HOST")
PROXMOX_TOKEN = os.getenv("PROXMOX_TOKEN")

# Verbindung zur Proxmox API mit Token herstellen
def get_proxmox_client():
    try:
        proxmox = ProxmoxAPI(
            PROXMOX_HOST,
            token_name=PROXMOX_TOKEN.split('=')[0],  # Token-Namen extrahieren
            token_value=PROXMOX_TOKEN.split('=')[1],  # Token-Wert extrahieren
            verify_ssl=False
        )
        return proxmox
    except Exception as e:
        raise RuntimeError(f"Fehler beim Verbinden mit der Proxmox API: {e}")
