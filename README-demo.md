# Fornas Match — Panduan Demo

## Cara 1: Demo Offline (Tanpa Server)

Cukup buka file HTML langsung di browser:

```
D:\Hackthon IBM\fornas-match-demo.html
```

- Klik chip atau ketik kasus → klik **Proses Kasus**
- Data yang muncul adalah data contoh (hardcoded), bukan dari Langflow
- Tidak butuh internet, tidak butuh server

---

## Cara 2: Live — Terhubung ke Langflow

### Prasyarat
- Langflow sudah berjalan di `http://localhost:7860`
- Python 3.x sudah terinstall

### Langkah

**1. Install dependensi (sekali saja)**
```powershell
python -m pip install fastapi uvicorn httpx
```

**2. Jalankan proxy server**
```powershell
cd "D:\Hackthon IBM"
python server.py
```

Output yang diharapkan:
```
====================================================
  Fornas Match Proxy Server
  Buka browser: http://localhost:8000
  API docs:     http://localhost:8000/docs
  Langflow:     http://localhost:7860
====================================================
```

**3. Buka browser**
```
http://localhost:8000
```

**4. Aktifkan Mode Live**
- Di halaman demo, geser toggle **Demo → Live**
- Badge di header berubah menjadi 🟢 **Mode Live**
- Sekarang semua hasil berasal dari Langflow secara langsung

---

## Arsitektur

```
Browser (fornas-match-demo.html)
    │  fetch POST /api/cek_fornas
    │  fetch POST /api/cek_stok
    │  fetch POST /api/hitung_dosis
    │  fetch POST /api/generate_pio
    ▼
server.py (FastAPI, port 8000)
    │  POST /api/v1/run/{flow_id}
    │  Header: x-api-key
    ▼
Langflow (port 7860)
    ├── Flow: cek_fornas            (26ae314f-...)
    ├── Flow: cek_stok              (09c035c8-...)
    ├── Flow: hitung_kesetaraan_dosis (81fa04c2-...)
    └── Flow: generate_pio          (64e061b5-...)
```

---

## Endpoint Proxy (untuk debugging)

| Endpoint | Langflow Flow |
|---|---|
| `POST /api/cek_fornas` | `cek_fornas` |
| `POST /api/cek_stok` | `cek_stok` |
| `POST /api/hitung_dosis` | `hitung_kesetaraan_dosis` |
| `POST /api/generate_pio` | `generate_pio` |
| `GET /health` | status check |
| `GET /docs` | Swagger UI otomatis |

Request body semua endpoint:
```json
{
  "input_value": "teks kasus dari apoteker",
  "session_id": "opsional"
}
```

---

## Troubleshooting

| Masalah | Solusi |
|---|---|
| `❌ Tidak bisa menghubungi Langflow` | Pastikan `python server.py` sudah jalan |
| `[502] Langflow error` | Pastikan Langflow di port 7860 aktif |
| Badge tidak berubah hijau | Refresh halaman, coba toggle ulang |
| CORS error di konsol browser | Buka via `http://localhost:8000`, bukan `file://` |
