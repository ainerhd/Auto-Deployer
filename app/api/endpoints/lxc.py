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
def create_container(
    node: str ,
    password: str,
    vmid: int = None,  # VMID ist optional
    hostname: str = "default-container",
    memory: int = 1024,
    storage: str = "local-lvm",  # Speicherort
    size: str = "8",  # Größe des Root-Dateisystems
    net_name: str = "eth0",
    bridge: str = "vmbr0",
    ip: str = "dhcp",
    template: str = "ubuntu",
    cores: int = 1,
    nesting: int = 1,  # Nesting-Feature aktivieren, Standard ist 1
):
    try:
        # Proxmox-Client abrufen
        proxmox = get_proxmox_client()

        # Automatische VMID-Ermittlung, falls keine angegeben wurde
        if vmid is None:
            used_vmids = {int(vm["vmid"]) for vm in proxmox.cluster.resources.get(type="vm")}
            vmid = next(vmid for vmid in range(100, 10000) if vmid not in used_vmids)

        # Template-Switch
        templates = {
            "debian": "local:vztmpl/debian-11-standard_11.0-1_amd64.tar.zst",
            "ubuntu": "local:vztmpl/ubuntu-24.10-standard_24.10-1_amd64.tar.zst",
            "centos": "local:vztmpl/centos-8-standard_8.0-1_amd64.tar.zst",
        }

        # Standard-Template, wenn der Schlüssel nicht existiert
        selected_template = templates.get(template, templates["ubuntu"])

        # Dynamisches net0-Feld
        net0 = f"name={net_name},bridge={bridge},ip={ip}"

        # Dynamisches rootfs-Feld
        rootfs = f"{storage}:{size}"

        # Dynamisches feature Feld
        features = f"nesting={nesting}"

        # LXC-Container erstellen
        result = proxmox.nodes(node).lxc.post(
            vmid=vmid,
            hostname=hostname,
            memory=memory,
            rootfs=rootfs,  # Korrekt formatiertes rootfs
            net0=net0,
            ostemplate=selected_template,
            storage=storage,
            cores=cores,
            password=password,
            features=features,
            unprivileged=1,
        )
        return {
            "status": "success",
            "message": f"Container {hostname} mit ID {vmid} auf Node {node} erstellt.",
            "vmid": vmid,
            "template": selected_template,
            "rootfs": rootfs,
            "net0": net0,
            "nesting": nesting,
            "result": result,
        }
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
