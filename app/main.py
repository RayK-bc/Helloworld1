import subprocess
from fastapi import FastAPI, HTTPException, Query

app = FastAPI(title="Performance Test Demo API")

@app.get("/api/v1/")
def ping_host(host: str = Query(..., description="Host to ping")):
    try:
        # 將命令拆分為列表，並設 shell=False
        result = subprocess.check_output(
            ["ping", "-c", "1", host], 
            shell=False, 
            text=True, 
            timeout=5
        )
        return {"output": result}
    except Exception as e:
        return {"error": str(e)}