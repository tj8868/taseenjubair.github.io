# Running Backend on Linux

This guide covers running the FastAPI portfolio backend on Linux systems (Ubuntu, Debian, Fedora, Arch, etc.).

---

## Prerequisites

- **Python 3.11+**
- `python3-venv` and `python3-pip` installed.

On Ubuntu / Debian:
```bash
sudo apt update && sudo apt install -y python3 python3-venv python3-pip
```

On Fedora / RHEL:
```bash
sudo dnf install -y python3 python3-pip
```

On Arch Linux:
```bash
sudo pacman -S python python-pip
```

---

## Quick Start (Automated Script)

From the project root:
```bash
./backend/run.sh
```

Or from inside the `backend/` directory:
```bash
cd backend
./run.sh
```

> **Note:** If you get a permission error when executing `./run.sh`, run:
> ```bash
> chmod +x run.sh
> ./run.sh
> ```
> Or invoke it directly with bash:
> ```bash
> bash run.sh
> ```

The script automatically:
1. Sets up the virtual environment (`.venv`).
2. Installs dependencies from `requirements.txt`.
3. Copies `.env.example` to `.env` if not present.
4. Boots the Uvicorn server on port 8000.

---

## Manual Start

If you prefer to run steps manually:

```bash
# 1. Enter the backend directory
cd backend

# 2. Create and activate a Python virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy environment configuration (if .env does not exist yet)
cp .env.example .env

# 5. Start Uvicorn development server
uvicorn app.main:app --reload --port 8000
```

---

## Accessing the Backend

Once running, access via your browser:

- **Admin Panel**: [http://127.0.0.1:8000/back](http://127.0.0.1:8000/back)
- **API Docs (Swagger UI)**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Consolidated Site JSON API**: [http://127.0.0.1:8000/api/site](http://127.0.0.1:8000/api/site)

**Default Login**:
- **Username**: `admin`
- **Password**: `change-me` *(change this at `/back/account` on first login)*

---

## Troubleshooting

### 1. Port 8000 already in use
If another application is using port 8000:
```bash
# Find and terminate the process
lsof -i :8000
# Or run backend on a different port:
.venv/bin/python3 -m uvicorn app.main:app --reload --port 8001
```

### 2. External Drive / Mount Execution Restrictions (`noexec`)
If your project is located on an external drive or NTFS partition mounted with the `noexec` flag, `./run.sh` will produce a `Permission denied` error. Run via bash directly:
```bash
bash run.sh
# or
python3 -m uvicorn app.main:app --reload --port 8000
```
