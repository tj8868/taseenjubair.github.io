"""Read-only API consumed by the Astro build."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import schemas, serialize
from ..database import get_db

router = APIRouter(prefix="/api", tags=["public"])


@router.get("/site", response_model=schemas.SiteOut)
def read_site(db: Session = Depends(get_db)) -> schemas.SiteOut:
    """Everything the static build needs, in one request."""
    return serialize.site_out(db)


@router.get("/profile", response_model=schemas.ProfileOut)
def read_profile(db: Session = Depends(get_db)) -> schemas.ProfileOut:
    return serialize.profile_out(serialize.get_profile(db))


@router.get("/about", response_model=schemas.AboutOut)
def read_about(db: Session = Depends(get_db)) -> schemas.AboutOut:
    return serialize.about_out(db, serialize.get_profile(db))


@router.get("/education", response_model=list[schemas.EducationOut])
def read_education(db: Session = Depends(get_db)) -> list[schemas.EducationOut]:
    return serialize.education_out(db)


@router.get("/content", response_model=list[schemas.ContentItemOut])
def read_content(db: Session = Depends(get_db)) -> list[schemas.ContentItemOut]:
    return serialize.content_out(db)
