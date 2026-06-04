import json
import os
import re
from typing import Any

from pydantic import BaseModel, Field


class Skill(BaseModel):
    name: str


class Experience(BaseModel):
    company: str = ""
    role: str = ""
    start: str = ""
    end: str = "Present"
    description: list[str] = Field(default_factory=list)


class Education(BaseModel):
    degree: str = ""
    institution: str = ""
    year: str = ""


class CVProfile(BaseModel):
    full_name: str | None = None
    email: str | None = None
    phone: str | None = None
    location: str | None = None
    education: list[Education] = Field(default_factory=list)
    experience: list[Experience] = Field(default_factory=list)
    skills: dict[str, list[Skill]] = Field(default_factory=dict)
    languages: list[str] = Field(default_factory=list)
    summary: str = ""
    total_experience_years: float = 0.0
    raw_text: str = ""

    @property
    def flat_skills(self) -> list[str]:
        names: list[str] = []
        for values in self.skills.values():
            names.extend(skill.name for skill in values if skill.name)
        return names


def _coerce_profile(data: dict[str, Any], fallback_text: str) -> CVProfile:
    contact = data.get("contact") if isinstance(data.get("contact"), dict) else {}
    skills = data.get("skills") if isinstance(data.get("skills"), dict) else {}
    normalized_skills: dict[str, list[dict[str, str]]] = {}
    
    def clean_skill(name: str) -> str:
        name = name.strip()
        if name.endswith(')') and not name.startswith('('):
            name = name[:-1]
        if name.startswith('(') and not name.endswith(')'):
            name = name[1:]
        return name.strip()

    for category, values in skills.items():
        if isinstance(values, list):
            normalized_skills[category] = [
                {"name": clean_skill(item.get("name", "") if isinstance(item, dict) else str(item))}
                for item in values
            ]

    return CVProfile(
        full_name=data.get("full_name") or data.get("name"),
        email=data.get("email") or contact.get("email"),
        phone=data.get("phone") or contact.get("phone"),
        location=data.get("location") or contact.get("location"),
        education=data.get("education") or [],
        experience=data.get("experience") or [],
        skills=normalized_skills,
        languages=data.get("languages") or [],
        summary=data.get("summary") or fallback_text[:1000],
        total_experience_years=float(data.get("total_experience_years") or 0.0),
        raw_text=fallback_text,
    )


class ExtractorService:
    """Notebook phase 2, packaged as an async backend service."""

    def __init__(self) -> None:
        self.model = os.getenv("OLLAMA_MODEL", "llama3:8b")

    async def extract_cv(self, text: str) -> CVProfile:
        llm_profile = self._extract_with_ollama(text)
        if llm_profile:
            return llm_profile
        return self._extract_with_regex(text)

    def _extract_with_ollama(self, text: str) -> CVProfile | None:
        try:
            import ollama

            response = ollama.chat(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a specialized CV parsing NER system. Return only JSON matching this structure exactly:\n"
                            "{\n"
                            "  \"full_name\": \"Candidate Full Name\",\n"
                            "  \"email\": \"candidate.email@example.com\",\n"
                            "  \"phone\": \"+1234567890\",\n"
                            "  \"location\": \"City, Country\",\n"
                            "  \"education\": [{\"degree\": \"Master in CS\", \"institution\": \"University Name\", \"year\": \"2024\"}],\n"
                            "  \"experience\": [{\"company\": \"Company A\", \"role\": \"Software Engineer\", \"start\": \"2021\", \"end\": \"2023\", \"description\": [\"Built APIs\", \"Optimized database\"]}],\n"
                            "  \"skills\": {\"technical\": [{\"name\": \"Python\"}, {\"name\": \"PostgreSQL\"}]},\n"
                            "  \"languages\": [\"English\", \"French\"],\n"
                            "  \"summary\": \"Professional summary...\",\n"
                            "  \"total_experience_years\": 3.5\n"
                            "}"
                        ),
                    },
                    {"role": "user", "content": f"EXTRACT FROM THIS CV TEXT:\n{text}"},
                ],
                format="json",
                options={"temperature": 0},
            )
            data = json.loads(response["message"]["content"])
            return _coerce_profile(data, text)
        except Exception:
            return None

    def _extract_with_regex(self, text: str) -> CVProfile:
        email_match = re.search(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+", text)
        phone_match = re.search(r"(?:\+?\d[\d\s().-]{7,}\d)", text)
        lines = [line.strip(" #\t") for line in text.splitlines() if line.strip()]
        name = next((line for line in lines[:8] if not re.search(r"@|\d{4,}", line)), None)

        skill_bank = [
            "python",
            "java",
            "javascript",
            "typescript",
            "react",
            "sql",
            "postgresql",
            "docker",
            "fastapi",
            "machine learning",
            "deep learning",
            "nlp",
            "excel",
            "développeur web",
            "developpeur web",
            "full stack",
            "bases de données",
            "base de données",
            "programmation",
            "systèmes d'exploitation",
            "systemes d'exploitation",
            "réseau",
            "reseau",
            "sécurité",
            "securite",
            "leadership",
            "communication",
            "teamwork",
        ]
        lower_text = text.lower()
        found_skills = [{"name": skill} for skill in skill_bank if skill in lower_text]

        years = [int(year) for year in re.findall(r"\b(19\d{2}|20\d{2})\b", text)]
        total_years = 0.0
        if len(years) >= 2:
            total_years = float(max(years) - min(years))

        return CVProfile(
            full_name=name,
            email=email_match.group(0) if email_match else None,
            phone=phone_match.group(0).strip() if phone_match else None,
            skills={"technical": found_skills},
            education=[{"degree": "Master", "institution": "", "year": ""}]
            if re.search(r"\b(master|licence|bachelor|degree|dipl[oô]me|formation)\b", lower_text)
            else [],
            summary=text[:1000],
            total_experience_years=total_years,
            raw_text=text,
        )


extractor_service = ExtractorService()
