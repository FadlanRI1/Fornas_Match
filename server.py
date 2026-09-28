"""
Fornas Match — Proxy Server Lokal
Meneruskan request dari fornas-match-demo.html ke Langflow MCP (localhost:7860)
Jalankan: python server.py
"""

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn, os, json, asyncio

# ── Langflow config (sama dengan .bob/mcp.json) ──────────────────────────────
LANGFLOW_BASE = "http://localhost:7860"
API_KEY       = "sk-ttBvabWi0y8reXsSWahpL6lCsEP95RT6VDQ_pKFI3Mo"

# Flow IDs diambil dari tool IDs di mcp.json
FLOW_IDS = {
    "cek_fornas":            "26ae314f-579c-4a9e-8238-3778a642e76d",
    "cek_stok":              "09c035c8-23e6-48df-a3c1-3a92dec1abdd",
    "hitung_kesetaraan_dosis": "81fa04c2-d4fc-4c72-b45c-dcbbc49481c9",
    "generate_pio":          "64e061b5-7167-468b-b1d4-8ba014268495",
}

HEADERS = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json",
}

# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(title="Fornas Match Proxy", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Models ────────────────────────────────────────────────────────────────────
class RunRequest(BaseModel):
    input_value: str
    session_id: str = ""

# ── Helper: call Langflow run endpoint ───────────────────────────────────────
async def call_langflow(flow_id: str, input_value: str, session_id: str = "") -> dict:
    url = f"{LANGFLOW_BASE}/api/v1/run/{flow_id}"
    payload = {
        "input_value": input_value,
        "output_type": "chat",
        "input_type": "chat",
    }
    if session_id:
        payload["session_id"] = session_id

    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.post(url, json=payload, headers=HEADERS)

    if resp.status_code != 200:
        raise HTTPException(
            status_code=resp.status_code,
            detail=f"Langflow error: {resp.text[:400]}"
        )

    data = resp.json()
    # ambil teks output dari struktur Langflow
    try:
        text = data["outputs"][0]["outputs"][0]["results"]["message"]["text"]
    except (KeyError, IndexError):
        text = json.dumps(data, ensure_ascii=False)
    return {"result": text, "raw": data}

# ── Endpoints ─────────────────────────────────────────────────────────────────

@app.get("/health")
async def health():
    return {"status": "ok", "langflow": LANGFLOW_BASE}

@app.post("/api/cek_fornas")
async def api_cek_fornas(req: RunRequest):
    return await call_langflow(FLOW_IDS["cek_fornas"], req.input_value, req.session_id)

@app.post("/api/cek_stok")
async def api_cek_stok(req: RunRequest):
    return await call_langflow(FLOW_IDS["cek_stok"], req.input_value, req.session_id)

@app.post("/api/hitung_dosis")
async def api_hitung_dosis(req: RunRequest):
    return await call_langflow(FLOW_IDS["hitung_kesetaraan_dosis"], req.input_value, req.session_id)

@app.post("/api/generate_pio")
async def api_generate_pio(req: RunRequest):
    return await call_langflow(FLOW_IDS["generate_pio"], req.input_value, req.session_id)

# ── Serve HTML ────────────────────────────────────────────────────────────────
@app.get("/")
async def serve_html():
    html_path = os.path.join(os.path.dirname(__file__), "fornas-match-demo.html")
    return FileResponse(html_path, media_type="text/html")

# ── Run ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("\n" + "="*52)
    print("  Fornas Match Proxy Server")
    print("  Buka browser: http://localhost:8000")
    print("  API docs:     http://localhost:8000/docs")
    print("  Langflow:     " + LANGFLOW_BASE)
    print("="*52 + "\n")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
