from fastapi import FastAPI
from app.api.endpoints import vms
from app.api.endpoints import lxc
from dotenv import load_dotenv
import os

# Umgebungsvariablen laden
load_dotenv()

# Anwendung erstellen
app = FastAPI(
    title="Proxmox Auto-Deployer",
    description="Eine API zur Automatisierung von Proxmox VMs und Containern",
    version="1.0.0",
)

# Router für VMs und LXC einbinden
app.include_router(vms.vm_router, prefix="/vms", tags=["VMs"])
app.include_router(lxc.lxc_router, prefix="/lxc", tags=["LXC"])

# Root-Route
@app.get("/")
def read_root():
    return {"message": "Willkommen bei der Proxmox Auto-Deployer API"}

@app.get("/health")
def health_check():
    return {"status": "ok"}