import logging
from proxmoxer import ProxmoxAPI
from dotenv import load_dotenv
import os

# Logging aktivieren
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv(override=True)

PROXMOX_HOST = os.getenv("PROXMOX_HOST")
PROXMOX_TOKEN = os.getenv("PROXMOX_TOKEN")

if not PROXMOX_HOST or not PROXMOX_TOKEN:
    raise ValueError("PROXMOX_HOST oder PROXMOX_TOKEN fehlt in der .env-Datei")

def get_proxmox_client():
    logger.debug(f"Verbindungsversuch zu {PROXMOX_HOST} mit Token {PROXMOX_TOKEN}")
    try:
        token_parts = PROXMOX_TOKEN.split('=')
        if len(token_parts) != 2:
            raise ValueError("PROXMOX_TOKEN hat ein ungültiges Format")
        
        token_name = token_parts[0]
        token_value = token_parts[1]

        print(token_name)
        print(token_value)

        # Direkte Verbindung zur Proxmox API
        proxmox = ProxmoxAPI(
            PROXMOX_HOST,  # Entferne Leerzeichen
            user=token_name,
            password=token_value,
            verify_ssl=False,
            service="pve",
            backend="https"
        )
        return proxmox
    except Exception as e:
        raise RuntimeError(f"Fehler beim Verbinden mit der Proxmox API: {e}")

if __name__ == "__main__":
    try:
        proxmox = get_proxmox_client()
        nodes = proxmox.nodes.get()
        print("Proxmox Nodes:", nodes)
    except Exception as e:
        print("Fehler beim Verbinden mit der Proxmox API:", e)
