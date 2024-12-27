from fastapi import FastAPI
from app.api.endpoints import vms

app = FastAPI()

# API-Router einbinden
app.include_router(vms.vm_router, prefix="/vms", tags=["VMs"])
