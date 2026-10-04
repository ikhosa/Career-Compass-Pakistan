from __future__ import annotations

from crewai import Agent, Crew, Process, Task

from config import get_llm
from models import FinalReport


def create_recommendation_agent() -> Agent:
    return Agent(
        role="Senior Career Guidance Recommendation Specialist",
        goal=(
            "Synthesize interest, aptitude, career-fit scoring, and Pakistan context into exactly three "
            "clear, justified career pathways for an intermediate student."
        ),
        backstory=(
            "You are the final decision-support layer for a Pakistani student career guidance application. "
            "You do not invent test scores or ranking facts. You explain trade-offs and convert structured evidence "
            "into an actionable study plan."
        ),
        llm=get_llm(),
        allow_delegation=False,
        verbose=False,
    )


def build_final_report(
    student_profile: dict,
    interest_summary: dict,
    aptitude_summary: dict,
    career_candidates: list[dict],
    pakistan_perspective: dict,
) -> FinalReport:
    agent = create_recommendation_agent()
    task = Task(
        description=(
            "Produce the final student career guidance report.\n"
            f"Student profile: {student_profile}\n"
            f"Interest summary: {interest_summary}\n"
            f"Aptitude summary: {aptitude_summary}\n"
            f"Deterministic career candidates: {career_candidates[:6]}\n"
            f"Pakistan perspective: {pakistan_perspective}\n\n"
            "Rules:\n"
            "1. Return exactly 3 recommendations, ranked 1, 2, 3.\n"
            "2. Use the deterministic fit_score as the fit_score; do not alter it.\n"
            "3. Explain why each path fits the evidence.\n"
            "4. Include practical BS degree choices, universities to consider, and future jobs.\n"
            "5. Distinguish overall THE-ranked universities from degree-fit university examples.\n"
            "6. Avoid promises of employment, admission, salary, or guaranteed success.\n"
            "7. Use plain English suitable for a Grade 12 student in Pakistan."
        ),
        expected_output="A structured FinalReport containing exactly three ranked recommendations.",
        agent=agent,
        output_pydantic=FinalReport,
    )
    result = Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=False).kickoff()
    if not result.pydantic:
        raise RuntimeError("Final recommendation generation failed.")
    report = result.pydantic
    if len(report.top_3) != 3:
        raise RuntimeError("Final report must contain exactly three recommendations.")
    for expected_rank, item in enumerate(report.top_3, start=1):
        item.rank = expected_rank
    return report
