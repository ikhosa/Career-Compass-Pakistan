from __future__ import annotations

from crewai import Agent, Crew, Process, Task

from config import get_llm
from models import AptitudeSummary, QuestionDecision
from question_bank import APTITUDE_SKILLS, get_candidate_questions


def create_aptitude_agent() -> Agent:
    return Agent(
        role="Adaptive Academic Aptitude Assessment Specialist",
        goal=(
            "Select validated aptitude questions that reveal numerical, logical, verbal, scientific, "
            "spatial, computational, analytical, and problem-solving strengths."
        ),
        backstory=(
            "You are an educational assessment specialist. You choose from a fixed question bank with known answers. "
            "You do not invent questions, answer keys, or scores. You adapt difficulty using the supplied response history."
        ),
        llm=get_llm(),
        allow_delegation=False,
        verbose=False,
    )


def choose_aptitude_question(
    student_profile: dict,
    history: list[dict],
    question_number: int,
) -> QuestionDecision:
    candidates = get_candidate_questions("aptitude", history, question_number)
    if not candidates:
        raise RuntimeError("No unused aptitude questions remain.")

    skill_results = [item for item in history if item.get("question_id")]
    recent = skill_results[-3:]

    agent = create_aptitude_agent()
    task = Task(
        description=(
            "Select the single best next aptitude question from the candidate list.\n"
            f"Question number: {question_number}/10\n"
            f"Student profile: {student_profile}\n"
            f"Previous scored responses: {history}\n"
            f"Recent responses: {recent}\n"
            f"Candidate questions: {[q['id'] + ': ' + q['text'] + ' (difficulty ' + str(q['difficulty']) + ')' for q in candidates]}\n\n"
            "Rules:\n"
            "1. Return exactly one question_id from the candidates.\n"
            "2. Never repeat a prior question.\n"
            "3. Adjust difficulty sensibly from recent performance; do not jump more than one level when possible.\n"
            "4. The application reserves questions 2, 4, 6 and 8 for visual interaction.\n"
            "5. Do not evaluate correctness yourself; the application uses the fixed answer key."
        ),
        expected_output="A structured QuestionDecision containing a valid question_id.",
        agent=agent,
        output_pydantic=QuestionDecision,
    )
    result = Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=False).kickoff()
    decision = result.pydantic
    if not decision:
        raise RuntimeError("Aptitude agent returned no structured decision.")
    valid_ids = {q["id"] for q in candidates}
    if decision.question_id not in valid_ids:
        raise RuntimeError("Aptitude agent selected an invalid question ID.")
    return decision


def summarize_aptitude(
    student_profile: dict,
    scores: dict[str, float],
    history: list[dict],
) -> AptitudeSummary:
    agent = create_aptitude_agent()
    task = Task(
        description=(
            "Summarize a student's aptitude results. Do not change the supplied scores or infer a diagnosis.\n"
            f"Student profile: {student_profile}\n"
            f"Skill scores: {scores}\n"
            f"Question history: {history}\n"
            f"Allowed skills: {APTITUDE_SKILLS}\n"
            "Identify strengths and improvement areas, using simple language appropriate for a Grade 12 student."
        ),
        expected_output="A structured AptitudeSummary with skill scores, strengths, improvement areas, and narrative.",
        agent=agent,
        output_pydantic=AptitudeSummary,
    )
    result = Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=False).kickoff()
    if not result.pydantic:
        raise RuntimeError("Aptitude summary generation failed.")
    return result.pydantic
