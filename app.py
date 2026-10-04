from __future__ import annotations

import os
from typing import Any

import streamlit as st

from career_flow import run_flow
from question_bank import get_question
from scoring import calculate_aptitude_scores, calculate_interest_scores, overall_aptitude_score, overall_interest_score
from ui import inject_css, render_assessment_metric_cards, render_final_report, render_header, render_profile_form, render_progress, render_question


st.set_page_config(
    page_title="Career Compass Pakistan",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)
inject_css()

# Streamlit Secrets are promoted to an environment variable so config.py stays
# framework-neutral and the agents can be tested outside Streamlit later.
if "XAI_API_KEY" in st.secrets:
    os.environ["XAI_API_KEY"] = str(st.secrets["XAI_API_KEY"])


def init_state() -> None:
    defaults: dict[str, Any] = {
        "started": False,
        "student_profile": {},
        "phase": "interest",
        "question_number": 1,
        "current_question_id": "",
        "history": [],
        "interest_scores": {},
        "aptitude_scores": {},
        "interest_summary": {},
        "aptitude_summary": {},
        "pakistan_perspective": {},
        "final_report": {},
        "error": "",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_app() -> None:
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()


def call_next_question() -> None:
    phase = st.session_state.phase
    action = "next_interest_question" if phase == "interest" else "next_aptitude_question"
    result = run_flow(
        action=action,
        student_profile=st.session_state.student_profile,
        history=st.session_state.history,
        question_number=st.session_state.question_number,
        phase=phase,
        interest_scores=st.session_state.interest_scores,
        aptitude_scores=st.session_state.aptitude_scores,
        interest_summary=st.session_state.interest_summary,
        aptitude_summary=st.session_state.aptitude_summary,
        pakistan_perspective=st.session_state.pakistan_perspective,
    )
    st.session_state.current_question_id = result["question_id"]


def handle_answer(answer_id: str, answer_value: Any) -> None:
    phase = st.session_state.phase
    question_id = st.session_state.current_question_id
    record = {
        "phase": phase,
        "question_id": question_id,
        "answer": answer_id,
        "answer_value": answer_value,
        "question_number": st.session_state.question_number,
    }
    st.session_state.history.append(record)

    if st.session_state.question_number < 10:
        st.session_state.question_number += 1
        call_next_question()
        st.rerun()
        return

    try:
        if phase == "interest":
            result = run_flow(
                action="summarize_interest",
                student_profile=st.session_state.student_profile,
                history=st.session_state.history,
                question_number=10,
                phase="interest",
            )
            st.session_state.interest_scores = calculate_interest_scores(st.session_state.history)
            st.session_state.interest_summary = result["summary"]
            st.session_state.phase = "aptitude"
            st.session_state.question_number = 1
            call_next_question()
        else:
            result = run_flow(
                action="summarize_aptitude",
                student_profile=st.session_state.student_profile,
                history=st.session_state.history,
                question_number=10,
                phase="aptitude",
                interest_scores=st.session_state.interest_scores,
                aptitude_scores=st.session_state.aptitude_scores,
                interest_summary=st.session_state.interest_summary,
                aptitude_summary=st.session_state.aptitude_summary,
            )
            aptitude_history = [x for x in st.session_state.history if x.get("phase") == "aptitude"]
            st.session_state.aptitude_scores = calculate_aptitude_scores(aptitude_history)
            st.session_state.aptitude_summary = result["summary"]
            st.session_state.pakistan_perspective = result["pakistan"]
            final = run_flow(
                action="recommend",
                student_profile=st.session_state.student_profile,
                history=st.session_state.history,
                question_number=10,
                phase="pakistan",
                interest_scores=st.session_state.interest_scores,
                aptitude_scores=st.session_state.aptitude_scores,
                interest_summary=st.session_state.interest_summary,
                aptitude_summary=st.session_state.aptitude_summary,
                pakistan_perspective=st.session_state.pakistan_perspective,
            )
            st.session_state.final_report = final["report"]
            st.session_state.phase = "complete"
    except Exception as exc:
        st.session_state.error = str(exc)

    st.rerun()


init_state()
render_header()

if st.session_state.error:
    st.error(st.session_state.error)
    st.caption("Check that XAI_API_KEY is present in Streamlit Secrets and that the deployment has internet access to the xAI API.")
    if st.button("Reset assessment"):
        reset_app()
    st.stop()

with st.sidebar:
    st.markdown("### Career Compass Pakistan")
    st.caption("Four-agent CrewAI Flow")
    st.caption("10 interest + 10 aptitude questions")
    st.caption("4 visual interactions in each assessment")
    if st.session_state.started and st.button("Restart"):
        reset_app()

if not st.session_state.started:
    profile = render_profile_form()
    if profile:
        st.session_state.started = True
        st.session_state.student_profile = profile
        try:
            call_next_question()
        except Exception as exc:
            st.session_state.error = str(exc)
        st.rerun()
    st.stop()

if st.session_state.phase in {"interest", "aptitude"}:
    render_progress(st.session_state.phase, st.session_state.question_number)
    render_assessment_metric_cards(
        overall_interest_score(calculate_interest_scores([x for x in st.session_state.history if x.get("phase") == "interest"])),
        overall_aptitude_score(calculate_aptitude_scores([x for x in st.session_state.history if x.get("phase") == "aptitude"]), [x for x in st.session_state.history if x.get("phase") == "aptitude"]),
    )
    st.write("")

    if not st.session_state.current_question_id:
        try:
            call_next_question()
        except Exception as exc:
            st.session_state.error = str(exc)
            st.rerun()

    bank_name = st.session_state.phase
    question = get_question(bank_name, st.session_state.current_question_id)
    render_question(question, st.session_state.question_number, handle_answer)

elif st.session_state.phase == "complete":
    render_final_report(st.session_state.final_report)
    st.write("")
    if st.button("Start a new assessment", type="primary", use_container_width=True):
        reset_app()
