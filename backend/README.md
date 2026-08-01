# Portfolio content backend

FastAPI + SQLite. Serves an admin panel at **`/back`** and a read-only JSON API that the
Astro site consumes **at build time**.

The public site stays a static GitHub Pages build. Nothing here needs to be online for
visitors: it only needs to be running when you rebuild the site.

## Requirements

Python 3.11 or newer. Check with `python --version`.
If it is missing, install it from <https://www.python.org/downloads/> and tick
**"Add python.exe to PATH"** during setup.

## Run it

```powershell
.\backend\run.ps1
```

First run creates `.venv`, installs dependencies, writes a `.env` with a generated
`SECRET_KEY`, and seeds the database from your existing site content.

| What | Where |
| --- | --- |
| Admin panel | <http://127.0.0.1:8000/back> |
| API docs | <http://127.0.0.1:8000/docs> |
| Full payload | <http://127.0.0.1:8000/api/site> |

Default login is `admin` / `change-me`. **Change it at `/back/account` on first login.**

### Manual start

```powershell
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
copy .env.example .env
.venv\Scripts\python -m uvicorn app.main:app --reload --port 8000
```

## Publishing edits

The site is static, so edits go live on the next build:

```bash
npm --prefix frontend run build
```

The build reads `PUBLIC_CMS_URL` (default `http://127.0.0.1:8000`) and, on success, saves
what it got to `frontend/src/data/cms-snapshot.json`. **Commit that file.** The GitHub
Actions runner cannot reach a backend on your laptop, so the snapshot is what it deploys
from.

So the full publish loop is, from the repository root:

```powershell
.\backend\run.ps1                   # one terminal, leave it running
npm --prefix frontend run build     # another: fetches content, writes the snapshot
git add -A
git commit -m "Update content"
git push
```

If the backend is not running, the build does not fail. It uses the last snapshot, or
`frontend/src/data/site.ts` if there is no snapshot yet, and says which one it picked in
the log.

## What the panel manages

- **Profile**: name, role, location, bio, photo and CV paths
- **About**: narrative sections and research interests
- **Education**: qualifications shown on About and in the CV
- **Content**: YouTube videos, LinkedIn posts, articles, talks

Publications, experience, skills, stats, and social links still live in `src/data/site.ts`.

## Data

Everything is in `backend/portfolio.db`. Back it up by copying that one file.
It is gitignored, along with `.env`.

## Notes on deploying

Local-only today. To put it on a server later:

1. Set a real `SECRET_KEY` and a strong `ADMIN_PASSWORD` in `.env`.
2. Serve over HTTPS and set `https_only=True` on `SessionMiddleware` in `app/main.py`.
3. Add the site origin to `CORS_ORIGINS`.
4. Drop `--reload` and run behind a reverse proxy.
