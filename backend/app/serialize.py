"""Model rows -> public API payloads."""

import re

from sqlalchemy import select
from sqlalchemy.orm import Session

from . import models, schemas

_PLATFORM_LABELS = dict(models.PLATFORMS)

# Covers watch?v=, youtu.be/, /embed/, /shorts/, /live/ and a bare id.
_YOUTUBE_ID = re.compile(
    r"(?:youtu\.be/|youtube\.com/(?:watch\?(?:.*&)?v=|embed/|shorts/|live/|v/))([\w-]{11})"
)


def extract_youtube_id(url: str) -> str:
    """Return the 11-char video id from any common YouTube URL, else ""."""
    url = (url or "").strip()
    if not url:
        return ""
    match = _YOUTUBE_ID.search(url)
    if match:
        return match.group(1)
    if re.fullmatch(r"[\w-]{11}", url):
        return url
    return ""


def split_tags(raw: str) -> list[str]:
    return [t.strip() for t in (raw or "").split(",") if t.strip()]


def split_paragraphs(body: str) -> list[str]:
    """Blank line separates paragraphs; a lone newline is treated as a soft wrap."""
    blocks = re.split(r"\n\s*\n", (body or "").strip())
    return [" ".join(line.strip() for line in b.splitlines()).strip() for b in blocks if b.strip()]


def get_profile(db: Session) -> models.Profile:
    profile = db.get(models.Profile, 1)
    if profile is None:
        profile = models.Profile(id=1)
        db.add(profile)
        db.commit()
        db.refresh(profile)
    return profile


def profile_out(row: models.Profile) -> schemas.ProfileOut:
    return schemas.ProfileOut(
        name=row.name,
        shortName=row.short_name,
        kicker=row.kicker,
        role=row.role,
        location=row.location,
        bio=row.bio,
        photo=row.photo or None,
        photoAlt=row.photo_alt,
        resume=row.resume or None,
    )


def about_out(db: Session, profile: models.Profile) -> schemas.AboutOut:
    sections = db.scalars(
        select(models.AboutSection).order_by(
            models.AboutSection.sort_order, models.AboutSection.id
        )
    ).all()
    interests = db.scalars(
        select(models.Interest).order_by(models.Interest.sort_order, models.Interest.id)
    ).all()
    return schemas.AboutOut(
        lead=profile.about_lead,
        sections=[
            schemas.AboutSectionOut(heading=s.heading, paragraphs=split_paragraphs(s.body))
            for s in sections
        ],
        interests=[i.label for i in interests],
    )


def education_out(db: Session) -> list[schemas.EducationOut]:
    rows = db.scalars(
        select(models.Education).order_by(models.Education.sort_order, models.Education.id)
    ).all()
    return [
        schemas.EducationOut(
            degree=r.degree, school=r.school, note=r.note or None, year=r.year
        )
        for r in rows
    ]


def content_item_out(row: models.ContentItem) -> schemas.ContentItemOut:
    thumbnail = row.thumbnail or (
        f"https://i.ytimg.com/vi/{row.video_id}/hqdefault.jpg" if row.video_id else ""
    )
    return schemas.ContentItemOut(
        id=row.id,
        platform=row.platform,
        platformLabel=_PLATFORM_LABELS.get(row.platform, row.platform.title()),
        title=row.title,
        description=row.description,
        url=row.url,
        videoId=row.video_id or None,
        thumbnail=thumbnail or None,
        publishedAt=row.published_at,
        tags=split_tags(row.tags),
        featured=row.featured,
    )


def content_out(db: Session, *, published_only: bool = True) -> list[schemas.ContentItemOut]:
    stmt = select(models.ContentItem)
    if published_only:
        stmt = stmt.where(models.ContentItem.is_published.is_(True))
    rows = db.scalars(
        stmt.order_by(
            models.ContentItem.featured.desc(),
            models.ContentItem.sort_order,
            models.ContentItem.id.desc(),
        )
    ).all()
    return [content_item_out(r) for r in rows]


def site_out(db: Session) -> schemas.SiteOut:
    profile = get_profile(db)
    return schemas.SiteOut(
        profile=profile_out(profile),
        about=about_out(db, profile),
        education=education_out(db),
        content=content_out(db),
    )
