"""Server-rendered admin panel mounted at /back."""

import secrets
from pathlib import Path

from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session

from .. import models, serialize
from ..database import get_db
from ..security import hash_password, verify_password

router = APIRouter(prefix="/back", tags=["admin"], include_in_schema=False)

templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent.parent / "templates"))

SESSION_USER_KEY = "admin_user_id"
SESSION_CSRF_KEY = "csrf_token"


# ── auth helpers ─────────────────────────────────────────────────────────────


def csrf_token(request: Request) -> str:
    token = request.session.get(SESSION_CSRF_KEY)
    if not token:
        token = secrets.token_urlsafe(32)
        request.session[SESSION_CSRF_KEY] = token
    return token


def check_csrf(request: Request, submitted: str) -> None:
    expected = request.session.get(SESSION_CSRF_KEY, "")
    if not expected or not secrets.compare_digest(expected, submitted or ""):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Invalid or expired form token")


def current_admin(request: Request, db: Session = Depends(get_db)) -> models.AdminUser:
    """Redirects to the login page instead of returning a bare 401."""
    user_id = request.session.get(SESSION_USER_KEY)
    user = db.get(models.AdminUser, user_id) if user_id else None
    if user is None:
        request.session.pop(SESSION_USER_KEY, None)
        raise HTTPException(
            status.HTTP_303_SEE_OTHER, headers={"Location": "/back/login"}
        )
    return user


def render(request: Request, template: str, admin: models.AdminUser, **context) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        template,
        {
            "admin": admin,
            # Drives the nav highlight: "dashboard.html" -> "dashboard".
            "active": template.removesuffix(".html"),
            "csrf": csrf_token(request),
            "flash": request.query_params.get("ok"),
            "error": request.query_params.get("error"),
            **context,
        },
    )


def back_to(path: str, ok: str | None = None) -> RedirectResponse:
    url = f"/back{path}" + (f"?ok={ok}" if ok else "")
    return RedirectResponse(url, status_code=status.HTTP_303_SEE_OTHER)


# ── login ────────────────────────────────────────────────────────────────────


@router.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    if request.session.get(SESSION_USER_KEY):
        return RedirectResponse("/back", status_code=status.HTTP_303_SEE_OTHER)
    return templates.TemplateResponse(
        request,
        "login.html",
        {"csrf": csrf_token(request), "error": request.query_params.get("error")},
    )


@router.post("/login")
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    csrf: str = Form(""),
    db: Session = Depends(get_db),
):
    check_csrf(request, csrf)
    user = db.scalar(select(models.AdminUser).where(models.AdminUser.username == username))
    if user is None or not verify_password(password, user.password_hash):
        return RedirectResponse(
            "/back/login?error=Incorrect+username+or+password",
            status_code=status.HTTP_303_SEE_OTHER,
        )
    # New session id material on privilege change, to blunt session fixation.
    request.session.clear()
    request.session[SESSION_USER_KEY] = user.id
    request.session[SESSION_CSRF_KEY] = secrets.token_urlsafe(32)
    return RedirectResponse("/back", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/logout")
def logout(request: Request, csrf: str = Form("")):
    check_csrf(request, csrf)
    request.session.clear()
    return RedirectResponse("/back/login", status_code=status.HTTP_303_SEE_OTHER)


# ── dashboard ────────────────────────────────────────────────────────────────


@router.get("", response_class=HTMLResponse)
def dashboard(
    request: Request,
    admin: models.AdminUser = Depends(current_admin),
    db: Session = Depends(get_db),
):
    counts = {
        "about": db.query(models.AboutSection).count(),
        "interests": db.query(models.Interest).count(),
        "education": db.query(models.Education).count(),
        "content": db.query(models.ContentItem).count(),
        "published": db.query(models.ContentItem)
        .filter(models.ContentItem.is_published.is_(True))
        .count(),
    }
    return render(request, "dashboard.html", admin, counts=counts)


# ── profile + about lead ─────────────────────────────────────────────────────


@router.get("/profile", response_class=HTMLResponse)
def profile_form(
    request: Request,
    admin: models.AdminUser = Depends(current_admin),
    db: Session = Depends(get_db),
):
    return render(request, "profile.html", admin, profile=serialize.get_profile(db))


@router.post("/profile")
def profile_save(
    request: Request,
    name: str = Form(""),
    short_name: str = Form(""),
    kicker: str = Form(""),
    role: str = Form(""),
    location: str = Form(""),
    bio: str = Form(""),
    photo: str = Form(""),
    photo_alt: str = Form(""),
    resume: str = Form(""),
    about_lead: str = Form(""),
    csrf: str = Form(""),
    admin: models.AdminUser = Depends(current_admin),
    db: Session = Depends(get_db),
):
    check_csrf(request, csrf)
    profile = serialize.get_profile(db)
    profile.name = name.strip()
    profile.short_name = short_name.strip()
    profile.kicker = kicker.strip()
    profile.role = role.strip()
    profile.location = location.strip()
    profile.bio = bio.strip()
    profile.photo = photo.strip()
    profile.photo_alt = photo_alt.strip()
    profile.resume = resume.strip()
    profile.about_lead = about_lead.strip()
    db.commit()
    return back_to("/profile", "Profile saved")


# ── about sections + interests ───────────────────────────────────────────────


@router.get("/about", response_class=HTMLResponse)
def about_page(
    request: Request,
    admin: models.AdminUser = Depends(current_admin),
    db: Session = Depends(get_db),
):
    sections = db.scalars(
        select(models.AboutSection).order_by(
            models.AboutSection.sort_order, models.AboutSection.id
        )
    ).all()
    interests = db.scalars(
        select(models.Interest).order_by(models.Interest.sort_order, models.Interest.id)
    ).all()
    return render(request, "about.html", admin, sections=sections, interests=interests)


@router.post("/about/sections")
def about_section_create(
    request: Request,
    heading: str = Form(...),
    body: str = Form(""),
    sort_order: int = Form(0),
    csrf: str = Form(""),
    admin: models.AdminUser = Depends(current_admin),
    db: Session = Depends(get_db),
):
    check_csrf(request, csrf)
    db.add(models.AboutSection(heading=heading.strip(), body=body, sort_order=sort_order))
    db.commit()
    return back_to("/about", "Section added")


@router.post("/about/sections/{section_id}")
def about_section_update(
    section_id: int,
    request: Request,
    heading: str = Form(...),
    body: str = Form(""),
    sort_order: int = Form(0),
    csrf: str = Form(""),
    admin: models.AdminUser = Depends(current_admin),
    db: Session = Depends(get_db),
):
    check_csrf(request, csrf)
    section = db.get(models.AboutSection, section_id)
    if section is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Section not found")
    section.heading = heading.strip()
    section.body = body
    section.sort_order = sort_order
    db.commit()
    return back_to("/about", "Section updated")


@router.post("/about/sections/{section_id}/delete")
def about_section_delete(
    section_id: int,
    request: Request,
    csrf: str = Form(""),
    admin: models.AdminUser = Depends(current_admin),
    db: Session = Depends(get_db),
):
    check_csrf(request, csrf)
    section = db.get(models.AboutSection, section_id)
    if section is not None:
        db.delete(section)
        db.commit()
    return back_to("/about", "Section deleted")


@router.post("/about/interests")
def interests_save(
    request: Request,
    interests: str = Form(""),
    csrf: str = Form(""),
    admin: models.AdminUser = Depends(current_admin),
    db: Session = Depends(get_db),
):
    """One interest per line. Replaces the whole list, which keeps ordering simple."""
    check_csrf(request, csrf)
    labels = [line.strip() for line in interests.splitlines() if line.strip()]
    db.query(models.Interest).delete()
    for order, label in enumerate(labels):
        db.add(models.Interest(label=label, sort_order=order))
    db.commit()
    return back_to("/about", "Interests saved")


# ── education ────────────────────────────────────────────────────────────────


@router.get("/education", response_class=HTMLResponse)
def education_page(
    request: Request,
    admin: models.AdminUser = Depends(current_admin),
    db: Session = Depends(get_db),
):
    rows = db.scalars(
        select(models.Education).order_by(models.Education.sort_order, models.Education.id)
    ).all()
    return render(request, "education.html", admin, rows=rows)


@router.post("/education")
def education_create(
    request: Request,
    degree: str = Form(...),
    school: str = Form(""),
    note: str = Form(""),
    year: str = Form(""),
    sort_order: int = Form(0),
    csrf: str = Form(""),
    admin: models.AdminUser = Depends(current_admin),
    db: Session = Depends(get_db),
):
    check_csrf(request, csrf)
    db.add(
        models.Education(
            degree=degree.strip(),
            school=school.strip(),
            note=note.strip(),
            year=year.strip(),
            sort_order=sort_order,
        )
    )
    db.commit()
    return back_to("/education", "Qualification added")


@router.post("/education/{row_id}")
def education_update(
    row_id: int,
    request: Request,
    degree: str = Form(...),
    school: str = Form(""),
    note: str = Form(""),
    year: str = Form(""),
    sort_order: int = Form(0),
    csrf: str = Form(""),
    admin: models.AdminUser = Depends(current_admin),
    db: Session = Depends(get_db),
):
    check_csrf(request, csrf)
    row = db.get(models.Education, row_id)
    if row is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Qualification not found")
    row.degree = degree.strip()
    row.school = school.strip()
    row.note = note.strip()
    row.year = year.strip()
    row.sort_order = sort_order
    db.commit()
    return back_to("/education", "Qualification updated")


@router.post("/education/{row_id}/delete")
def education_delete(
    row_id: int,
    request: Request,
    csrf: str = Form(""),
    admin: models.AdminUser = Depends(current_admin),
    db: Session = Depends(get_db),
):
    check_csrf(request, csrf)
    row = db.get(models.Education, row_id)
    if row is not None:
        db.delete(row)
        db.commit()
    return back_to("/education", "Qualification deleted")


# ── content ──────────────────────────────────────────────────────────────────


@router.get("/content", response_class=HTMLResponse)
def content_page(
    request: Request,
    admin: models.AdminUser = Depends(current_admin),
    db: Session = Depends(get_db),
):
    rows = db.scalars(
        select(models.ContentItem).order_by(
            models.ContentItem.featured.desc(),
            models.ContentItem.sort_order,
            models.ContentItem.id.desc(),
        )
    ).all()
    return render(request, "content.html", admin, rows=rows, platforms=models.PLATFORMS)


def _apply_content_fields(row: models.ContentItem, **f) -> None:
    row.platform = f["platform"]
    row.title = f["title"].strip()
    row.description = f["description"].strip()
    row.url = f["url"].strip()
    row.thumbnail = f["thumbnail"].strip()
    row.published_at = f["published_at"].strip()
    row.tags = f["tags"].strip()
    row.featured = f["featured"]
    row.is_published = f["is_published"]
    row.sort_order = f["sort_order"]
    # Derived, not user-entered: keeps the embed working even if someone pastes
    # a share link with tracking params on it.
    row.video_id = serialize.extract_youtube_id(row.url) if row.platform == "youtube" else ""


@router.post("/content")
def content_create(
    request: Request,
    platform: str = Form("youtube"),
    title: str = Form(...),
    description: str = Form(""),
    url: str = Form(""),
    thumbnail: str = Form(""),
    published_at: str = Form(""),
    tags: str = Form(""),
    featured: bool = Form(False),
    is_published: bool = Form(False),
    sort_order: int = Form(0),
    csrf: str = Form(""),
    admin: models.AdminUser = Depends(current_admin),
    db: Session = Depends(get_db),
):
    check_csrf(request, csrf)
    row = models.ContentItem()
    _apply_content_fields(
        row,
        platform=platform,
        title=title,
        description=description,
        url=url,
        thumbnail=thumbnail,
        published_at=published_at,
        tags=tags,
        featured=featured,
        is_published=is_published,
        sort_order=sort_order,
    )
    db.add(row)
    db.commit()
    return back_to("/content", "Content added")


@router.post("/content/{row_id}")
def content_update(
    row_id: int,
    request: Request,
    platform: str = Form("youtube"),
    title: str = Form(...),
    description: str = Form(""),
    url: str = Form(""),
    thumbnail: str = Form(""),
    published_at: str = Form(""),
    tags: str = Form(""),
    featured: bool = Form(False),
    is_published: bool = Form(False),
    sort_order: int = Form(0),
    csrf: str = Form(""),
    admin: models.AdminUser = Depends(current_admin),
    db: Session = Depends(get_db),
):
    check_csrf(request, csrf)
    row = db.get(models.ContentItem, row_id)
    if row is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Content item not found")
    _apply_content_fields(
        row,
        platform=platform,
        title=title,
        description=description,
        url=url,
        thumbnail=thumbnail,
        published_at=published_at,
        tags=tags,
        featured=featured,
        is_published=is_published,
        sort_order=sort_order,
    )
    db.commit()
    return back_to("/content", "Content updated")


@router.post("/content/{row_id}/delete")
def content_delete(
    row_id: int,
    request: Request,
    csrf: str = Form(""),
    admin: models.AdminUser = Depends(current_admin),
    db: Session = Depends(get_db),
):
    check_csrf(request, csrf)
    row = db.get(models.ContentItem, row_id)
    if row is not None:
        db.delete(row)
        db.commit()
    return back_to("/content", "Content deleted")


# ── account ──────────────────────────────────────────────────────────────────


@router.get("/account", response_class=HTMLResponse)
def account_page(request: Request, admin: models.AdminUser = Depends(current_admin)):
    return render(request, "account.html", admin)


@router.post("/account/password")
def change_password(
    request: Request,
    current_password: str = Form(...),
    new_password: str = Form(...),
    confirm_password: str = Form(...),
    csrf: str = Form(""),
    admin: models.AdminUser = Depends(current_admin),
    db: Session = Depends(get_db),
):
    check_csrf(request, csrf)
    if not verify_password(current_password, admin.password_hash):
        return RedirectResponse(
            "/back/account?error=Current+password+is+wrong",
            status_code=status.HTTP_303_SEE_OTHER,
        )
    if new_password != confirm_password:
        return RedirectResponse(
            "/back/account?error=New+passwords+do+not+match",
            status_code=status.HTTP_303_SEE_OTHER,
        )
    if len(new_password) < 10:
        return RedirectResponse(
            "/back/account?error=Use+at+least+10+characters",
            status_code=status.HTTP_303_SEE_OTHER,
        )
    admin.password_hash = hash_password(new_password)
    db.commit()
    return back_to("/account", "Password changed")
