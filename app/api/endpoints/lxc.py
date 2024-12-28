from fastapi import APIRouter, HTTPException
from app.proxmox import get_proxmox_client

lxc_router = APIRouter()

# Route: Liste aller LXC-Container abrufen
@lxc_router.get("/{node}/containers")
def list_containers(node: str):
    try:
        proxmox = get_proxmox_client()
        containers = proxmox.nodes(node).lxc.get()
        return {"status": "success", "containers": containers}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Route: Details eines spezifischen Containers abrufen
@lxc_router.get("/{node}/containers/{vmid}")
def get_container_details(node: str, vmid: int):
    try:
        proxmox = get_proxmox_client()
        details = proxmox.nodes(node).lxc(vmid).status.current.get()
        return {"status": "success", "details": details}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Route: Einen neuen LXC-Container erstellen
@lxc_router.post("/{node}/containers/create")
def create_container(node: str, vmid: int, hostname: str, memory: int, rootfs: str, net0: str):
    try:
        proxmox = get_proxmox_client()
        result = proxmox.nodes(node).lxc.post(
            vmid=vmid,
            hostname=hostname,
            memory=memory,
            rootfs=rootfs,
            net0=net0,
            ostemplate="local:vztmpl/debian-11-standard_11.0-1_amd64.tar.gz",
            storage="local-lvm",
            cores=1
        )
        return {"status": "success", "message": f"Container {hostname} mit ID {vmid} auf Node {node} erstellt.", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Route: Einen LXC-Container starten
@lxc_router.post("/{node}/containers/{vmid}/start")
def start_container(node: str, vmid: int):
    try:
        proxmox = get_proxmox_client()
        proxmox.nodes(node).lxc(vmid).status.start.post()
        return {"status": "success", "message": f"Container {vmid} auf Node {node} gestartet."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Route: Einen LXC-Container stoppen
@lxc_router.post("/{node}/containers/{vmid}/stop")
def stop_container(node: str, vmid: int):
    try:
        proxmox = get_proxmox_client()
        proxmox.nodes(node).lxc(vmid).status.stop.post()
        return {"status": "success", "message": f"Container {vmid} auf Node {node} gestoppt."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Route: Einen LXC-Container löschen
@lxc_router.delete("/{node}/containers/{vmid}")
def delete_container(node: str, vmid: int):
    try:
        proxmox = get_proxmox_client()
        proxmox.nodes(node).lxc(vmid).delete()
        return {"status": "success", "message": f"Container {vmid} auf Node {node} gelöscht."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
