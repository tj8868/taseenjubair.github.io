# Running Backend on Android (via Termux)

This guide explains how to run the FastAPI portfolio backend on an Android device using [Termux](https://termux.dev/).

---

## 1. Install Termux & Prerequisites

1. Install **Termux** (recommended via [F-Droid](https://f-droid.org/en/packages/com.termux/) or GitHub releases, not Google Play Store).
2. Open Termux and update package repositories:
   ```bash
   pkg update && pkg upgrade -y
   ```
3. Install Python, Git, and build essentials (needed for compiled C-extensions like SQLAlchemy / Pydantic Core):
   ```bash
   pkg install -y python git clang make libffi openssl
   ```

---

## 2. Accessing the Project Directory

### Option A: Clone the Repository directly into Termux
```bash
git clone <YOUR_REPO_URL>
cd Github_portfolio/backend
```

### Option B: Accessing Files on Android Internal Storage
Grant Termux storage access:
```bash
termux-setup-storage
```
Navigate to your files (e.g. inside `Downloads` or custom folder):
```bash
cd ~/storage/shared/Download/Github_portfolio/backend
```

---

## 3. Setup and Run

In Termux on Android, python packages can be installed directly or in a virtual environment:

### Step 1: Install Dependencies
```bash
# Ensure pip is up to date
pip install --upgrade pip

# Install project dependencies
pip install -r requirements.txt
```

> **Tip for Termux compilation issues:**
> If `pydantic-core` or other binary wheels fail to compile on your device architecture, install wheels via:
> ```bash
> pip install --upgrade wheel setuptools
> pip install -r requirements.txt
> ```

### Step 2: Configure Environment
If `.env` does not exist:
```bash
cp .env.example .env
```

### Step 3: Start the Backend Server
On Android/Termux, bind to `0.0.0.0` or `127.0.0.1`:
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

---

## 4. Accessing from your Android Device

Open your Android browser (Chrome, Firefox, etc.) and visit:

- **Admin Panel**: [http://127.0.0.1:8000/back](http://127.0.0.1:8000/back) (or `http://localhost:8000/back`)
- **API Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **JSON API**: [http://127.0.0.1:8000/api/site](http://127.0.0.1:8000/api/site)

**Default Login**:
- **Username**: `admin`
- **Password**: `change-me`

---

## 5. Accessing from another device on the same Wi-Fi

Because `--host 0.0.0.0` is used, other devices on your local network (laptop, tablet) can access your backend.

1. In Termux, check your Android device's local IP:
   ```bash
   ifconfig
   ```
   *(Look for `wlan0` `inet` address, e.g., `192.168.1.45`)*
2. In the other device's browser, open:
   `http://192.168.1.45:8000/back`
