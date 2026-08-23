import time
import os
import subprocess
from fastapi import FastAPI, HTTPException, Query

app = FastAPI(title="Performance Test Demo API")

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI Performance Demo"}

@app.get("/api/v1/health")
def health_check():
    return {"status": "healthy", "timestamp": time.time()}

@app.get("/api/v1/items/{item_id}")
def read_item(item_id: int):
    if item_id <= 0:
        raise HTTPException(status_code=400, detail="Item ID must be positive")
    return {"item_id": item_id, "name": f"Item {item_id}", "status": "active"}

# Vulnerable endpoint for Snyk security testing demo (Command Injection)
@app.get("/api/v1/ping")
def ping_host(host: str = Query(..., description="Host to ping")):
    # INTENTIONAL VULNERABILITY FOR SNYK DEMO: Unsanitized input passed directly to shell command
    command = f"ping -c 1 {host}"
    try:
        result = subprocess.check_output(command, shell=True, text=True, timeout=5)
        return {"output": result}
    except Exception as e:
        return {"error": str(e)}

