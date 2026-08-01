from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from .config import settings
from .database import Base, SessionLocal, engine
from .routers import admin, public
from .seed import seed

STATIC_DIR = Path(__file__).resolve().parent / "static"


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        seed(db)
    yield


app = FastAPI(
    title="Portfolio CMS",
    description="Content backend for the taseenjubair portfolio. Admin panel at /back.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.secret_key,
    session_cookie="portfolio_admin",
    max_age=settings.session_max_age,
    same_site="lax",
    # Leave False for plain-HTTP localhost; set True once served over HTTPS.
    https_only=False,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.mount("/back/static", StaticFiles(directory=str(STATIC_DIR)), name="admin-static")

app.include_router(public.router)
app.include_router(admin.router)


@app.get("/", include_in_schema=False)
def root() -> RedirectResponse:
    return RedirectResponse("/back")


@app.get("/healthz", tags=["public"])
def healthz() -> dict[str, str]:
    return {"status": "ok"}
