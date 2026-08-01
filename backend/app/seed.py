"""First-run seeding.

Only ever inserts into empty tables, so restarting the server never clobbers
edits made through the admin panel.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from . import models
from .config import settings
from .security import hash_password

_PROFILE = {
    "name": "H M Taseen Jubair Bhuiyan",
    "short_name": "T. J. Bhuiyan",
    "kicker": "Public Health · Data Science · Artificial Intelligence · Research",
    "role": "Public Health & Development Research",
    "location": "Dhaka, Bangladesh",
    "bio": (
        "Research associate working across public health, WASH, and disaster resilience, "
        "turning field data into evidence for planning and policy."
    ),
    "photo": "",
    "photo_alt": "Portrait of H M Taseen Jubair Bhuiyan",
    "resume": "",
    "about_lead": (
        "Public health and development research professional with experience supporting "
        "healthcare, WASH, and disaster resilience projects through data-driven analysis, "
        "field coordination, and technical reporting."
    ),
}

_ABOUT_SECTIONS = [
    (
        "Background",
        "I began in civil engineering at RUET and moved toward public health and development "
        "research, where infrastructure, environment, and population health intersect. That path "
        "now runs through an M.Sc. in Applied Statistics and Data Science at Jahangirnagar "
        "University.\n\n"
        "My work sits between the field and the analysis: designing collection instruments, "
        "running KIIs and FGDs, validating what comes back, and turning it into something a "
        "planner or a policymaker can act on.",
    ),
    (
        "Current work",
        "At Daffodil International University I support public health research on healthcare data "
        "analysis, disease patterns, and health monitoring systems, from study design through "
        "statistical interpretation and reporting.\n\n"
        "Recent work with the Cox's Bazar Development Authority covered WASH infrastructure and "
        "cyclone shelter assessments, with GIS-based vulnerability and risk mapping feeding "
        "directly into emergency response strategy.",
    ),
]

_INTERESTS = [
    "Public Health Research",
    "WASH & Environmental Health",
    "Disaster Risk Reduction",
    "Geospatial Vulnerability Analysis",
    "Applied Statistics",
    "AI in Health Prediction",
]

_EDUCATION = [
    ("M.Sc. Applied Statistics & Data Science", "Jahangirnagar University, Dhaka", "Thesis programme", "Expected 2026"),
    ("B.Sc. Civil Engineering", "Rajshahi University of Engineering & Technology (RUET)", "", "2021"),
    ("Higher Secondary Certificate", "Notre Dame College, Dhaka", "", "2013"),
]


def seed(db: Session) -> None:
    if db.scalar(select(models.AdminUser).limit(1)) is None:
        db.add(
            models.AdminUser(
                username=settings.admin_username,
                password_hash=hash_password(settings.admin_password),
            )
        )

    if db.get(models.Profile, 1) is None:
        db.add(models.Profile(id=1, **_PROFILE))

    if db.scalar(select(models.AboutSection).limit(1)) is None:
        for order, (heading, body) in enumerate(_ABOUT_SECTIONS):
            db.add(models.AboutSection(heading=heading, body=body, sort_order=order))

    if db.scalar(select(models.Interest).limit(1)) is None:
        for order, label in enumerate(_INTERESTS):
            db.add(models.Interest(label=label, sort_order=order))

    if db.scalar(select(models.Education).limit(1)) is None:
        for order, (degree, school, note, year) in enumerate(_EDUCATION):
            db.add(
                models.Education(
                    degree=degree, school=school, note=note, year=year, sort_order=order
                )
            )

    db.commit()
