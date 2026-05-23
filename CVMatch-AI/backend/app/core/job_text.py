def build_job_text(
    title: str = "",
    description: str = "",
    required_hard_skills: list[str] | None = None,
    required_soft_skills: list[str] | None = None,
    min_experience_years: int | float = 0,
    required_degree: str | None = None,
) -> str:
    hard_skills = ", ".join(required_hard_skills or [])
    soft_skills = ", ".join(required_soft_skills or [])
    return "\n".join(
        [
            f"Title: {title or ''}",
            f"Description: {description or ''}",
            f"Required hard skills: {hard_skills}",
            f"Required soft skills: {soft_skills}",
            f"Minimum experience years: {min_experience_years or 0}",
            f"Required education level: {required_degree or ''}",
        ]
    ).strip()
