# Drift Report (2026-11-26)

This report details discrepancies between the design specifications (as documented in `README.md`, `backend/README.md`, `backend/README.LINUX.md`, and `backend/README.ANDROID.md`) and the actual implementation, detailing what is broken and what has been fixed.

---

## README.md

### Broken / Divergent:
- **Build environment drift (Windows vs Linux npm installation):** The documentation specifies running `npm install` and `npm run dev` / `npm run build` directly. The current `frontend/node_modules` was installed on Windows (`.bin/astro` references `node.exe` and `@rollup/rollup-win32-x64-msvc`), causing `npm run build` on Linux to fail with `exec: node.exe: not found` and missing `@rollup/rollup-linux-x64-gnu`.
- **Publish to GitHub authentication:** The 1-click publishing workflow documented in the README assumes an interactive terminal or pre-authenticated remote session. Without a configured credential helper or PAT in Git, the push hangs or fails.

### Fixed:
- **Automatic CMS Snapshot Sync:** Changes saved in the admin panel now update `frontend/src/data/cms-snapshot.json` reliably, ensuring build-time data fallback works even when the backend is offline.
- **Git User Identification:** Configured local repository Git author identity (`Taseen <taseenjubair@gmail.com>`), resolving the non-zero exit status 128 error during CMS publishing commits.

---

## backend/README.md

### Broken / Divergent:
- **Publish Failure on Non-interactive Git Push:** The documented workflow states that editing content in `/back` allows rebuilding or publishing to GitHub. When credentials are not cached, Git attempted an interactive prompt in a headless process. 

### Fixed:
- **Admin Password Reset:** Restored admin login capability using `admin` / `change-me`.
- **Safe Push Handling in `/back/publish`:** Refactored `backend/app/routers/admin.py` to disable blocking terminal prompts (`GIT_TERMINAL_PROMPT=0`), capture specific Git errors, and return actionable messages in the admin UI instead of crashing with an unhandled 500 error.
- **Working Tree Cleanliness:** Staged and committed 360+ pending CMS snapshot and template files to keep the Git working tree clean.

---

## backend/README.LINUX.md

### Broken / Divergent:
- **Cross-filesystem `node_modules` compatibility:** When mounting a workspace from an external NTFS/FAT32 drive across both Windows and Linux, native binary node packages (Rollup/Sharp) do not cross-execute without running `npm rebuild` or reinstalling platform-specific packages.

### Fixed:
- **Linux Execution Script (`backend/run.sh`):** Fully operational for setting up the Python virtual environment and launching the Uvicorn server on Linux.
- **SQLite Database Pathing:** Relative database connection strings correctly resolve whether executed from repository root or the `backend/` directory.

---

## backend/README.ANDROID.md

### No drift detected.
Specification accurately aligns with the modular FastAPI backend design and Termux requirements.
