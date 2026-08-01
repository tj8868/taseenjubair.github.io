"""Shapes returned by the public API.

Field names deliberately match `src/data/site.ts` so the Astro loader can drop
the payload straight in where the hand-written fallback used to be.
"""

from pydantic import BaseModel


class ProfileOut(BaseModel):
    name: str
    shortName: str
    kicker: str
    role: str
    location: str
    bio: str
    photo: str | None
    photoAlt: str
    resume: str | None


class AboutSectionOut(BaseModel):
    heading: str
    paragraphs: list[str]


class AboutOut(BaseModel):
    lead: str
    sections: list[AboutSectionOut]
    interests: list[str]


class EducationOut(BaseModel):
    degree: str
    school: str
    note: str | None
    year: str


class ContentItemOut(BaseModel):
    id: int
    platform: str
    platformLabel: str
    title: str
    description: str
    url: str
    videoId: str | None
    thumbnail: str | None
    publishedAt: str
    tags: list[str]
    featured: bool


class SiteOut(BaseModel):
    profile: ProfileOut
    about: AboutOut
    education: list[EducationOut]
    content: list[ContentItemOut]
