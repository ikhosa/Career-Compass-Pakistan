from __future__ import annotations

from typing import Any

from crewai.flow.flow import Flow, start

from aptitude_agent import choose_aptitude_question, summarize_aptitude
from interest_agent import choose_interest_question, summarize_interest
from models import CareerFlowState
from pakistan_agent import build_pakistan_perspective
from recommendation_agent import build_final_report
from scoring import (
    build_career_candidates,
    calculate_aptitude_scores,
    calculate_interest_scores,
    overall_aptitude_score,
    overall_interest_score,
)


class CareerGuidanceFlow(Flow[CareerFlowState]):
    """Thin CrewAI Flow layer around the four specialist agents.

    Streamlit owns browser interaction and session state. This Flow owns the
    orchestration decision for each user action and can therefore be rerun safely
    after each Streamlit interaction.
    """

    @start()
    def run_step(self) -> dict[str, Any]:
        action = self.state.action

        if action == "next_interest_question":
            decision = choose_interest_question(
                self.state.student_profile,
                self.state.history,
                self.state.question_number,
            )
            self.state.current_question_id = decision.question_id
            self.state.last_output = {
                "type": "question",
                "phase": "interest",
                "question_id": decision.question_id,
                "reason": decision.reason,
            }
            return self.state.last_output

        if action == "summarize_interest":
            scores = calculate_interest_scores(self.state.history)
            self.state.interest_scores = scores
            summary = summarize_interest(self.state.student_profile, scores, self.state.history)
            self.state.interest_summary = summary.model_dump()
            self.state.phase = "aptitude"
            self.state.question_number = 1
            self.state.last_output = {
                "type": "summary",
                "phase": "interest",
                "summary": self.state.interest_summary,
            }
            return self.state.last_output

        if action == "next_aptitude_question":
            aptitude_history = [h for h in self.state.history if h.get("phase") == "aptitude"]
            decision = choose_aptitude_question(
                self.state.student_profile,
                aptitude_history,
                self.state.question_number,
            )
            self.state.current_question_id = decision.question_id
            self.state.last_output = {
                "type": "question",
                "phase": "aptitude",
                "question_id": decision.question_id,
                "reason": decision.reason,
            }
            return self.state.last_output

        if action == "summarize_aptitude":
            aptitude_history = [h for h in self.state.history if h.get("phase") == "aptitude"]
            scores = calculate_aptitude_scores(aptitude_history)
            self.state.aptitude_scores = scores
            summary = summarize_aptitude(self.state.student_profile, scores, aptitude_history)
            self.state.aptitude_summary = summary.model_dump()
            self.state.phase = "pakistan"
            self.state.question_number = 1

            career_candidates = build_career_candidates(
                self.state.interest_scores,
                self.state.aptitude_scores,
                overall_interest_score(self.state.interest_scores),
                overall_aptitude_score(self.state.aptitude_scores, aptitude_history),
            )
            perspective = build_pakistan_perspective(
                self.state.student_profile,
                self.state.interest_summary,
                self.state.aptitude_summary,
                career_candidates,
            )
            self.state.pakistan_perspective = perspective.model_dump()
            self.state.last_output = {
                "type": "summary",
                "phase": "pakistan",
                "summary": self.state.aptitude_summary,
                "pakistan": self.state.pakistan_perspective,
            }
            return self.state.last_output

        if action == "recommend":
            aptitude_history = [h for h in self.state.history if h.get("phase") == "aptitude"]
            career_candidates = build_career_candidates(
                self.state.interest_scores,
                self.state.aptitude_scores,
                overall_interest_score(self.state.interest_scores),
                overall_aptitude_score(self.state.aptitude_scores, aptitude_history),
            )
            report = build_final_report(
                self.state.student_profile,
                self.state.interest_summary,
                self.state.aptitude_summary,
                career_candidates,
                self.state.pakistan_perspective,
            )
            self.state.final_report = report.model_dump()
            self.state.phase = "complete"
            self.state.last_output = {"type": "final", "report": self.state.final_report}
            return self.state.last_output

        raise ValueError(f"Unsupported Flow action: {action}")


def run_flow(
    action: str,
    student_profile: dict[str, Any],
    history: list[dict[str, Any]],
    question_number: int = 1,
    phase: str = "interest",
    interest_scores: dict[str, float] | None = None,
    aptitude_scores: dict[str, float] | None = None,
    interest_summary: dict[str, Any] | None = None,
    aptitude_summary: dict[str, Any] | None = None,
    pakistan_perspective: dict[str, Any] | None = None,
) -> dict[str, Any]:
    payload = {
        "action": action,
        "phase": phase,
        "question_number": question_number,
        "student_profile": student_profile,
        "history": history,
        "interest_scores": interest_scores or {},
        "aptitude_scores": aptitude_scores or {},
        "interest_summary": interest_summary or {},
        "aptitude_summary": aptitude_summary or {},
        "pakistan_perspective": pakistan_perspective or {},
    }
    flow = CareerGuidanceFlow()
    result = flow.kickoff(inputs=payload)
    return result
