from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World, ich befinde mich im test Ordner..."}

@app.get("/health")
def health_check():
    return {"status": "ok"}