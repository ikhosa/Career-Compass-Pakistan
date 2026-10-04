from __future__ import annotations

from crewai import Agent, Crew, Process, Task

from config import get_llm
from models import InterestSummary, QuestionDecision
from question_bank import INTEREST_DIMENSIONS, get_candidate_questions


def create_interest_agent() -> Agent:
    return Agent(
        role="Adaptive Student Interest Assessment Specialist",
        goal=(
            "Identify a Grade 12/intermediate student's underlying career-interest dimensions "
            "using indirect, age-appropriate scenarios and validated questions."
        ),
        backstory=(
            "You are an educational career-guidance assessor working with Pakistani intermediate students. "
            "You avoid leading questions such as 'Which career do you like?' and instead use situations, choices, "
            "and preferences to uncover interest dimensions. You may select only from the supplied question IDs."
        ),
        llm=get_llm(),
        allow_delegation=False,
        verbose=False,
    )


def choose_interest_question(
    student_profile: dict,
    history: list[dict],
    question_number: int,
) -> QuestionDecision:
    candidates = get_candidate_questions("interest", history, question_number)
    if not candidates:
        raise RuntimeError("No unused interest questions remain.")

    agent = create_interest_agent()
    task = Task(
        description=(
            "Select the single best next interest question from the candidate list.\n"
            f"Question number: {question_number}/10\n"
            f"Student profile: {student_profile}\n"
            f"Previous responses: {history}\n"
            f"Candidate questions: {[q['id'] + ': ' + q['text'] for q in candidates]}\n\n"
            "Rules:\n"
            "1. Return exactly one question_id from the candidates.\n"
            "2. Never repeat a prior question.\n"
            "3. Prefer the question that most reduces uncertainty between the student's emerging dimensions.\n"
            "4. Keep the sequence age-appropriate and non-diagnostic.\n"
            "5. The application reserves questions 2, 4, 6 and 8 for visual interaction; do not select a non-visual item in those slots."
        ),
        expected_output="A QuestionDecision containing a valid question_id and a concise reason.",
        agent=agent,
        output_pydantic=QuestionDecision,
    )
    result = Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=False).kickoff()
    decision = result.pydantic
    if not decision:
        raise RuntimeError("Interest agent returned no structured decision.")
    valid_ids = {q["id"] for q in candidates}
    if decision.question_id not in valid_ids:
        raise RuntimeError("Interest agent selected an invalid question ID.")
    return decision


def summarize_interest(
    student_profile: dict,
    scores: dict[str, float],
    history: list[dict],
) -> InterestSummary:
    agent = create_interest_agent()
    task = Task(
        description=(
            "Summarize the student's interest assessment. Do not invent scores; use the supplied scores as facts.\n"
            f"Student profile: {student_profile}\n"
            f"Interest dimension scores: {scores}\n"
            f"Response history: {history}\n"
            f"Allowed dimensions: {INTEREST_DIMENSIONS}\n"
            "Explain the pattern in plain language suitable for a Grade 12 student. Avoid diagnosing personality or psychology."
        ),
        expected_output="A structured InterestSummary with scores, top dimensions, and a clear narrative.",
        agent=agent,
        output_pydantic=InterestSummary,
    )
    result = Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=False).kickoff()
    if not result.pydantic:
        raise RuntimeError("Interest summary generation failed.")
    return result.pydantic
