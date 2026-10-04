from __future__ import annotations

from typing import Any
from pydantic import BaseModel, Field


class QuestionDecision(BaseModel):
    question_id: str
    reason: str = ""
    confidence: float = Field(default=0.8, ge=0.0, le=1.0)


class InterestSummary(BaseModel):
    overall_score: float = Field(default=0.0, ge=0.0, le=100.0)
    dimension_scores: dict[str, float] = Field(default_factory=dict)
    top_dimensions: list[str] = Field(default_factory=list)
    narrative: str = ""


class AptitudeSummary(BaseModel):
    overall_score: float = Field(default=0.0, ge=0.0, le=100.0)
    skill_scores: dict[str, float] = Field(default_factory=dict)
    strengths: list[str] = Field(default_factory=list)
    improvement_areas: list[str] = Field(default_factory=list)
    narrative: str = ""


class PakistanCareerFit(BaseModel):
    career_path: str
    aligned_degrees: list[str] = Field(default_factory=list)
    universities_to_consider: list[str] = Field(default_factory=list)
    target_jobs: list[str] = Field(default_factory=list)
    pakistan_context: str = ""


class PakistanPerspective(BaseModel):
    ranking_year: int = 2027
    top_3_the_universities: list[str] = Field(default_factory=list)
    career_fits: list[PakistanCareerFit] = Field(default_factory=list)
    note: str = ""


class FinalRecommendation(BaseModel):
    rank: int = Field(ge=1, le=3)
    career_path: str
    fit_score: float = Field(default=0.0, ge=0.0, le=100.0)
    why: str
    degrees: list[str] = Field(default_factory=list)
    universities: list[str] = Field(default_factory=list)
    future_jobs: list[str] = Field(default_factory=list)
    preparation_next_steps: list[str] = Field(default_factory=list)


class FinalReport(BaseModel):
    student_profile_summary: str
    assessment_summary: str
    top_3: list[FinalRecommendation] = Field(default_factory=list)
    data_note: str = ""
    disclaimer: str = (
        "This tool provides educational career guidance. It is not a guarantee of admission, "
        "employment, income, or professional/psychological diagnosis."
    )


class CareerFlowState(BaseModel):
    action: str = ""
    phase: str = "interest"
    question_number: int = 1
    current_question_id: str = ""
    student_profile: dict[str, Any] = Field(default_factory=dict)
    history: list[dict[str, Any]] = Field(default_factory=list)
    interest_scores: dict[str, float] = Field(default_factory=dict)
    aptitude_scores: dict[str, float] = Field(default_factory=dict)
    interest_summary: dict[str, Any] = Field(default_factory=dict)
    aptitude_summary: dict[str, Any] = Field(default_factory=dict)
    pakistan_perspective: dict[str, Any] = Field(default_factory=dict)
    final_report: dict[str, Any] = Field(default_factory=dict)
    last_output: dict[str, Any] = Field(default_factory=dict)
