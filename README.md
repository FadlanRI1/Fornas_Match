# Fornas Match 💊

> Sistem cerdas berbasis AI untuk pengecekan Formularium Nasional (Fornas), stok obat, konversi dosis, dan pembuatan informasi obat (PIO) — didukung oleh **Langflow** dan **IBM Bob**.

---

## Daftar Isi

- [Gambaran Umum](#gambaran-umum)
- [Fitur](#fitur)
- [Arsitektur](#arsitektur)
- [Struktur Proyek](#struktur-proyek)
- [Prasyarat](#prasyarat)
- [Instalasi & Menjalankan](#instalasi--menjalankan)
  - [Mode Offline (Demo)](#1-mode-offline-demo)
  - [Mode Live (Langflow)](#2-mode-live-langflow)
- [Endpoint API](#endpoint-api)
- [Dataset](#dataset)
- [Variabel Konfigurasi](#variabel-konfigurasi)
- [Troubleshooting](#troubleshooting)
- [Kontribusi](#kontribusi)

---

## Gambaran Umum

**Fornas Match** membantu apoteker dan tenaga farmasi untuk:

1. Mengecek apakah suatu obat tercantum dalam Fornas.
2. Mengecek ketersediaan stok obat.
3. Menghitung kesetaraan dosis antar-obat.
4. Membuat teks PIO (Pelayanan Informasi Obat) secara otomatis.

Antarmuka berbasis browser single-page dapat berjalan dalam dua mode: **Demo offline** (data hardcoded) dan **Live** (terhubung ke Langflow AI flows).

---

## Fitur

| Fitur | Mode Demo | Mode Live |
|---|:---:|:---:|
| Cek status Fornas | ✅ | ✅ |
| Cek stok obat | ✅ | ✅ |
| Hitung kesetaraan dosis | ✅ | ✅ |
| Generate teks PIO | ✅ | ✅ |
| Hasil dari AI Langflow | ❌ | ✅ |
| Butuh internet / server | ❌ | ✅ |

---

## Arsitektur

```
Browser  (fornas-match-demo.html)
    │
    │  fetch POST /api/cek_fornas
    │  fetch POST /api/cek_stok
    │  fetch POST /api/hitung_dosis
    │  fetch POST /api/generate_pio
    ▼
server.py  (FastAPI — port 8000)
    │
    │  POST /api/v1/run/{flow_id}
    │  Header: x-api-key
    ▼
Langflow   (port 7860)
    ├── Flow: cek_fornas              (26ae314f-...)
    ├── Flow: cek_stok                (09c035c8-...)
    ├── Flow: hitung_kesetaraan_dosis (81fa04c2-...)
    └── Flow: generate_pio            (64e061b5-...)
```

---

## Struktur Proyek

```
Hackthon IBM/
├── fornas-match-demo.html   # UI utama (single-page app)
├── server.py                # Proxy FastAPI — jembatan browser ↔ Langflow
├── hello.py                 # Script utilitas kecil
├── README.md                # Dokumentasi ini
├── README-demo.md           # Panduan singkat demo
├── .gitignore               # Pola file yang diabaikan Git
├── .env.example             # Template variabel lingkungan (tidak berisi secret)
└── Dataset/
    ├── Daftar Obat Fornas Lengkap.xlsx
    └── Daftar Obat - [A-Z].xlsx     # Dataset per huruf awal
```

---

## Prasyarat

| Kebutuhan | Versi minimum |
|---|---|
| Python | 3.9+ |
| pip | — |
| Langflow | sudah berjalan di `http://localhost:7860` |
| Browser modern | Chrome / Edge / Firefox |

---

## Instalasi & Menjalankan

### 1. Mode Offline (Demo)

Tidak butuh instalasi apa pun. Cukup buka file HTML langsung di browser:

```
fornas-match-demo.html  →  klik kanan → Open with → Browser
```

- Data yang tampil adalah data contoh (hardcoded).
- Toggle **Demo / Live** ada di header halaman.

---

### 2. Mode Live (Langflow)

**Langkah 1 — Clone & masuk ke direktori**

```bash
git clone <repo-url>
cd "Hackthon IBM"
```

**Langkah 2 — Buat file `.env` dari template**

```bash
copy .env.example .env
```

Edit `.env` dan isi `LANGFLOW_API_KEY` dengan API key Langflow Anda.

**Langkah 3 — Install dependensi Python**

```bash
python -m pip install fastapi uvicorn httpx
```

Atau gunakan virtual environment (disarankan):

```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
pip install fastapi uvicorn httpx
```

**Langkah 4 — Jalankan proxy server**

```bash
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

**Langkah 5 — Buka browser & aktifkan Mode Live**

1. Buka `http://localhost:8000`
2. Geser toggle **Demo → Live** di header.
3. Badge berubah menjadi 🟢 **Mode Live** — semua hasil kini dari Langflow.

---

## Endpoint API

Semua endpoint menerima `Content-Type: application/json`.

### Request body (semua endpoint POST)

```json
{
  "input_value": "teks kasus dari apoteker",
  "session_id": "opsional-string"
}
```

### Response body

```json
{
  "result": "teks hasil dari Langflow",
  "raw": { ... }
}
```

### Daftar endpoint

| Method | Endpoint | Deskripsi |
|---|---|---|
| `GET` | `/health` | Status server & koneksi Langflow |
| `GET` | `/docs` | Swagger UI otomatis (FastAPI) |
| `POST` | `/api/cek_fornas` | Cek status obat di Fornas |
| `POST` | `/api/cek_stok` | Cek ketersediaan stok obat |
| `POST` | `/api/hitung_dosis` | Hitung kesetaraan dosis |
| `POST` | `/api/generate_pio` | Generate teks informasi obat (PIO) |

---

## Dataset

Folder `Dataset/` berisi file Excel daftar obat Fornas:

- `Daftar Obat Fornas Lengkap.xlsx` — dataset gabungan lengkap.
- `Daftar Obat - [A-Z].xlsx` — dataset per huruf awal nama obat.

> **Catatan:** Dataset ini tidak dihilangkan dari Git secara default. Jika dataset bersifat sensitif atau terlalu besar, batalkan komentar baris `# Dataset/` di `.gitignore`.

---

## Variabel Konfigurasi

Buat file `.env` berdasarkan `.env.example`:

| Variabel | Default | Keterangan |
|---|---|---|
| `LANGFLOW_BASE` | `http://localhost:7860` | URL Langflow |
| `LANGFLOW_API_KEY` | — | **Wajib** — API key Langflow |

> ⚠️ **Jangan pernah commit API key** langsung di `server.py` atau file lain yang masuk Git. Selalu gunakan `.env`.

---

## Troubleshooting

| Masalah | Solusi |
|---|---|
| `❌ Tidak bisa menghubungi Langflow` | Pastikan `python server.py` sudah berjalan |
| `[502] Langflow error` | Pastikan Langflow aktif di port 7860 |
| Badge tidak berubah hijau | Refresh halaman, toggle ulang |
| CORS error di konsol browser | Akses via `http://localhost:8000`, bukan `file://` |
| `ModuleNotFoundError` | Jalankan `pip install fastapi uvicorn httpx` |
| Port 8000 sudah dipakai | Edit baris `port=8000` di `server.py` |

---

## Kontribusi

1. Fork repo ini.
2. Buat branch fitur: `git checkout -b fitur/nama-fitur`
3. Commit perubahan: `git commit -m "feat: deskripsi singkat"`
4. Push ke branch: `git push origin fitur/nama-fitur`
5. Buka Pull Request.

---

*Dibuat untuk IBM Hackathon — Fornas Match Team*
