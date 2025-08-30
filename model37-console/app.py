import os
from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse
from pydantic import BaseModel
from datetime import datetime
from auth import check_token
import pipeline, store

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8080"))

app = FastAPI(title="Model37 Console", version="0.1.0")
app.mount("/web", StaticFiles(directory="web"), name="web")

class RunResp(BaseModel):
    timestamp: str
    count: int
    report: str

@app.get("/", response_class=HTMLResponse)
def home():
    with open("web/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())

@app.get("/health")
def health():
    return {"ok": True, "time": datetime.utcnow().isoformat()}

@app.post("/run/today", response_model=RunResp)
def run_today(_: bool = Depends(check_token)):
    out = pipeline.run_today_all()
    return RunResp(timestamp=datetime.utcnow().isoformat(),
                   count=out["count"], report=out["report"])

@app.get("/value-picks/today")
def value_picks_today(_: bool = Depends(check_token)):
    rows = store.load_report("today")
    return JSONResponse(rows)

@app.get("/report/today.csv")
def download_today(_: bool = Depends(check_token)):
    p = store.report_path("today")
    if not os.path.exists(p):
        return JSONResponse({"error": "No report yet"}, status_code=404)
    return FileResponse(p, media_type="text/csv", filename=os.path.basename(p))
