from __future__ import annotations

from crewai import Agent, Crew, Process, Task

from config import get_llm
from models import PakistanPerspective
from pakistan_data import DATA_LAST_VERIFIED, DATA_VERSION, THE_TOP_3_PAKISTAN, CAREER_PROFILES, top_three_the_text


def create_pakistan_agent() -> Agent:
    return Agent(
        role="Pakistan Higher-Education and Career Context Specialist",
        goal=(
            "Translate a student's interest and aptitude results into realistic Pakistani undergraduate degree, "
            "university, and future-job pathways using only the supplied verified reference data."
        ),
        backstory=(
            "You advise Pakistani intermediate students about education pathways. You distinguish overall THE ranking "
            "from degree-specific fit, avoid inventing university rankings, and prefer concise, practical guidance."
        ),
        llm=get_llm(),
        allow_delegation=False,
        verbose=False,
    )


def build_pakistan_perspective(
    student_profile: dict,
    interest_summary: dict,
    aptitude_summary: dict,
    career_candidates: list[dict],
) -> PakistanPerspective:
    agent = create_pakistan_agent()
    task = Task(
        description=(
            "Create the Pakistan perspective for the student's strongest career candidates.\n"
            f"Student profile: {student_profile}\n"
            f"Interest assessment: {interest_summary}\n"
            f"Aptitude assessment: {aptitude_summary}\n"
            f"Ranked career candidates from deterministic scoring: {career_candidates[:6]}\n\n"
            f"Verified THE WUR {DATA_VERSION} top 3 Pakistan list: {top_three_the_text()}\n"
            f"Data last verified: {DATA_LAST_VERIFIED}\n"
            f"Career reference catalog: {CAREER_PROFILES}\n\n"
            "Rules:\n"
            "1. Do not change any supplied rank band.\n"
            "2. Do not invent a university as being in the overall THE top 3.\n"
            "3. You may explain why degree-fit universities are worth considering, but do not call them overall THE top 3 unless supplied.\n"
            "4. Focus on the top 3 career candidates.\n"
            "5. Target jobs should come from the supplied career reference catalog.\n"
            "6. Keep guidance student-friendly and practical."
        ),
        expected_output="A structured PakistanPerspective with top-3 THE universities and career-specific fits.",
        agent=agent,
        output_pydantic=PakistanPerspective,
    )
    result = Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=False).kickoff()
    if not result.pydantic:
        raise RuntimeError("Pakistan perspective generation failed.")
    perspective = result.pydantic
    perspective.ranking_year = int(THE_TOP_3_PAKISTAN[0]["year"])
    return perspective
