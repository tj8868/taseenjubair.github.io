from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


def _now() -> datetime:
    return datetime.now(timezone.utc)


class AdminUser(Base):
    __tablename__ = "admin_users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now)


class Profile(Base):
    """Single row (id=1). The sidebar / hero identity block."""

    __tablename__ = "profile"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(160), default="")
    short_name: Mapped[str] = mapped_column(String(80), default="")
    kicker: Mapped[str] = mapped_column(String(240), default="")
    role: Mapped[str] = mapped_column(String(160), default="")
    location: Mapped[str] = mapped_column(String(120), default="")
    bio: Mapped[str] = mapped_column(Text, default="")
    photo: Mapped[str] = mapped_column(String(255), default="")
    photo_alt: Mapped[str] = mapped_column(String(255), default="")
    resume: Mapped[str] = mapped_column(String(255), default="")
    about_lead: Mapped[str] = mapped_column(Text, default="")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=_now, onupdate=_now)


class AboutSection(Base):
    """A headed block of prose on the About page. Paragraphs are blank-line separated."""

    __tablename__ = "about_sections"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    heading: Mapped[str] = mapped_column(String(160))
    body: Mapped[str] = mapped_column(Text, default="")
    sort_order: Mapped[int] = mapped_column(Integer, default=0)


class Interest(Base):
    __tablename__ = "interests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    label: Mapped[str] = mapped_column(String(120))
    sort_order: Mapped[int] = mapped_column(Integer, default=0)


class Education(Base):
    __tablename__ = "education"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    degree: Mapped[str] = mapped_column(String(240))
    school: Mapped[str] = mapped_column(String(240), default="")
    note: Mapped[str] = mapped_column(String(240), default="")
    year: Mapped[str] = mapped_column(String(60), default="")
    sort_order: Mapped[int] = mapped_column(Integer, default=0)


class ContentItem(Base):
    """A published piece of work: a YouTube video, a LinkedIn post, an article."""

    __tablename__ = "content_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    platform: Mapped[str] = mapped_column(String(32), default="youtube")
    title: Mapped[str] = mapped_column(String(300))
    description: Mapped[str] = mapped_column(Text, default="")
    url: Mapped[str] = mapped_column(String(600), default="")
    # For YouTube only: the 11-character video id, derived from `url` on save.
    video_id: Mapped[str] = mapped_column(String(32), default="")
    # Overrides the auto-derived YouTube thumbnail when set.
    thumbnail: Mapped[str] = mapped_column(String(600), default="")
    published_at: Mapped[str] = mapped_column(String(40), default="")
    tags: Mapped[str] = mapped_column(String(400), default="")
    featured: Mapped[bool] = mapped_column(Boolean, default=False)
    is_published: Mapped[bool] = mapped_column(Boolean, default=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=_now)


PLATFORMS = [
    ("youtube", "YouTube"),
    ("linkedin", "LinkedIn"),
    ("article", "Article / Blog"),
    ("talk", "Talk / Presentation"),
    ("other", "Other work"),
]
