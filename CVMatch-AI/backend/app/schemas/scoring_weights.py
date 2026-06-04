from pydantic import BaseModel, model_validator
import math

class ScoringWeightsBase(BaseModel):
    skills: float
    experience: float
    education: float
    soft_skills: float

    @model_validator(mode='after')
    def check_sum(self) -> 'ScoringWeightsBase':
        total = self.skills + self.experience + self.education + self.soft_skills
        if not math.isclose(total, 1.0, rel_tol=1e-5):
            raise ValueError('The sum of weights must be exactly 1.0')
        return self

class ScoringWeightsCreate(ScoringWeightsBase):
    pass

class ScoringWeightsResponse(ScoringWeightsBase):
    class Config:
        from_attributes = True
