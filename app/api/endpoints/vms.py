from fastapi import APIRouter
from app.proxmox import get_proxmox_client  # Importiere die Funktion zur Proxmox-Verbindung

# Erstelle den Router
vm_router = APIRouter()

# Route zum Testen der Proxmox-API-Verbindung
@vm_router.get("/test-token")
def test_proxmox_token():
    try:
        # Proxmox-Client erstellen
        proxmox = get_proxmox_client()
        
        # Liste der Knoten abrufen
        nodes = proxmox.nodes.get()
        return {"status": "success", "nodes": nodes}
    except Exception as e:
        return {"status": "error", "message": str(e)}
