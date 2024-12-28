from fastapi import APIRouter, HTTPException
from app.proxmox import get_proxmox_client

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

# Route: Liste der VMs abrufen
@vm_router.get("/")
def list_vms():
    try:
        proxmox = get_proxmox_client()

        # Alle Knoten durchsuchen und VMs abrufen
        vms = []
        for node in proxmox.nodes.get():
            vms.extend(proxmox.nodes(node['node']).qemu.get())

        return {"status": "success", "vms": vms}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Route: Details einer VM abrufen
@vm_router.get("/{node}/{vmid}")
def get_vm_details(node: str, vmid: int):
    try:
        proxmox = get_proxmox_client()
        vm_details = proxmox.nodes(node).qemu(vmid).status.current.get()
        return {"status": "success", "vm_details": vm_details}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Route: VM starten
@vm_router.post("/{node}/{vmid}/start")
def start_vm(node: str, vmid: int):
    try:
        proxmox = get_proxmox_client()
        proxmox.nodes(node).qemu(vmid).status.start.post()
        return {"status": "success", "message": f"VM {vmid} auf Node {node} gestartet."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Route: VM stoppen
@vm_router.post("/{node}/{vmid}/stop")
def stop_vm(node: str, vmid: int):
    try:
        proxmox = get_proxmox_client()
        proxmox.nodes(node).qemu(vmid).status.stop.post()
        return {"status": "success", "message": f"VM {vmid} auf Node {node} gestoppt."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Route: Neue VM erstellen
@vm_router.post("/{node}/create")
def create_vm(node: str, vmid: int, name: str, cores: int, memory: int, scsi0: str, net0: str):
    try:
        proxmox = get_proxmox_client()
        proxmox.nodes(node).qemu.post(
            vmid=vmid,
            name=name,
            cores=cores,
            memory=memory,
            scsi0=scsi0,  # Erwartet Format wie "local-lvm:128"
            net0=net0     # Erwartet Format wie "virtio,bridge=vmbr0"
        )
        return {"status": "success", "message": f"VM {name} mit ID {vmid} auf Node {node} erstellt."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Route: VM löschen
@vm_router.delete("/{node}/{vmid}")
def delete_vm(node: str, vmid: int):
    try:
        proxmox = get_proxmox_client()
        proxmox.nodes(node).qemu(vmid).delete()
        return {"status": "success", "message": f"VM {vmid} auf Node {node} gelöscht."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
