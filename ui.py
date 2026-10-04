from __future__ import annotations

from typing import Any, Callable

import streamlit as st


CSS = """
<style>
:root {
    --cc-navy: #0b1f3a;
    --cc-blue: #2563eb;
    --cc-cyan: #0891b2;
    --cc-bg: #f5f8fc;
    --cc-card: #ffffff;
    --cc-muted: #5b6472;
    --cc-border: #d8e0ea;
    --cc-green: #0f766e;
}
.stApp { background: linear-gradient(180deg, #f8fbff 0%, #f4f7fb 100%); }
.block-container { max-width: 1200px; padding-top: 1.5rem; padding-bottom: 3rem; }
.hero {
  background: linear-gradient(135deg, #0b1f3a 0%, #164e8f 55%, #0f766e 100%);
  color: white; padding: 2rem 2.2rem; border-radius: 24px; margin-bottom: 1.5rem;
  box-shadow: 0 14px 40px rgba(11,31,58,.18);
}
.hero h1 { margin: 0 0 .45rem 0; font-size: 2.35rem; }
.hero p { margin: 0; color: #edf5ff; font-size: 1.05rem; }
.badge { display:inline-block; padding:.35rem .7rem; border:1px solid rgba(255,255,255,.25); border-radius:999px; margin-bottom: .8rem; font-size:.82rem; }
.card { background:#fff; border:1px solid #dce5ef; border-radius:18px; padding:1.15rem 1.25rem; margin:.75rem 0; box-shadow:0 8px 24px rgba(11,31,58,.06); }
.question-card { background:#fff; border:1px solid #d8e0ea; border-radius:22px; padding:1.4rem; box-shadow:0 12px 28px rgba(11,31,58,.07); }
.question-number { color:#2563eb; font-weight:700; font-size:.9rem; text-transform:uppercase; letter-spacing:.05em; }
.question-text { color:#0b1f3a; font-size:1.45rem; line-height:1.35; font-weight:700; margin:.4rem 0 1rem; }
.option-note { color:#5b6472; font-size:.9rem; }
.result-card { background:white; border:1px solid #dce5ef; border-radius:20px; padding:1.35rem; margin:1rem 0; box-shadow:0 10px 25px rgba(11,31,58,.06); }
.rank { color:#2563eb; font-weight:800; font-size:.95rem; }
.metric-card { background:white; border:1px solid #dce5ef; border-radius:18px; padding:1rem; text-align:center; box-shadow:0 8px 18px rgba(11,31,58,.05); }
.metric-value { color:#0b1f3a; font-size:1.8rem; font-weight:800; }
.metric-label { color:#5b6472; font-size:.9rem; }
.small { color:#5b6472; font-size:.88rem; }
[data-testid="stButton"] button { border-radius:14px !important; min-height:46px; font-weight:650; }
</style>
"""


def inject_css() -> None:
    st.markdown(CSS, unsafe_allow_html=True)


def render_header() -> None:
    st.markdown(
        """
        <div class="hero">
          <div class="badge">AI-assisted career guidance for Pakistani intermediate students</div>
          <h1>Career Compass Pakistan</h1>
          <p>Discover career paths that align with your interests, aptitude and Pakistan's higher-education landscape.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_profile_form() -> dict[str, Any] | None:
    st.markdown('<div class="card"><h3>Before we begin</h3><p class="small">These background details are not counted as assessment questions.</p></div>', unsafe_allow_html=True)
    with st.form("profile_form"):
        name = st.text_input("Your name (optional)")
        col1, col2 = st.columns(2)
        with col1:
            stream = st.selectbox(
                "Current intermediate stream",
                ["ICS", "FSc Pre-Engineering", "FSc Pre-Medical", "ICom", "FA / Humanities", "Other"],
            )
            percentage = st.selectbox(
                "Expected percentage",
                ["90-100%", "80-89%", "70-79%", "60-69%", "Below 60%", "Not sure"],
            )
        with col2:
            region = st.selectbox(
                "Preferred study region",
                ["Anywhere in Pakistan", "Punjab", "Sindh", "Khyber Pakhtunkhwa", "Balochistan", "Islamabad / Rawalpindi"],
            )
            university_type = st.selectbox("University preference", ["Either", "Public", "Private"])
        submitted = st.form_submit_button("Start assessment", type="primary", use_container_width=True)
    if submitted:
        return {
            "name": name.strip() or "Student",
            "stream": stream,
            "expected_percentage": percentage,
            "preferred_region": region,
            "university_type": university_type,
        }
    return None


def render_progress(phase: str, question_number: int) -> None:
    phase_label = "Interest assessment" if phase == "interest" else "Aptitude assessment"
    progress = max(0.0, min(1.0, (question_number - 1) / 10.0))
    st.progress(progress, text=f"{phase_label} - Question {question_number} of 10")


def render_question(
    question: dict[str, Any],
    question_number: int,
    on_answer: Callable[[str, Any], None],
) -> None:
    st.markdown(
        f'<div class="question-card"><div class="question-number">Question {question_number} of 10</div><div class="question-text">{question["text"]}</div></div>',
        unsafe_allow_html=True,
    )

    if question.get("ui") == "cards":
        st.markdown("<div class='option-note'>Choose one card.</div>", unsafe_allow_html=True)
        cols = st.columns(len(question["options"]))
        for idx, option in enumerate(question["options"]):
            with cols[idx]:
                emoji = option.get("emoji", "")
                label = f"{emoji}\n{option['label']}" if emoji else option["label"]
                if st.button(label, key=f"answer_{question['id']}_{option['id']}", use_container_width=True):
                    on_answer(option["id"], option["label"])
        return

    if question.get("ui") == "slider":
        value = st.slider(
            "",
            min_value=int(question.get("min", 0)),
            max_value=int(question.get("max", 100)),
            value=int(question.get("default", 50)),
            label_visibility="collapsed",
        )
        c1, c2 = st.columns(2)
        with c1:
            st.caption(question.get("left_label", "Left"))
        with c2:
            st.caption(question.get("right_label", "Right"))
        if st.button("Continue", type="primary", use_container_width=True, key=f"continue_{question['id']}"):
            on_answer("SLIDER", value)
        return

    options = question.get("options", [])
    choice = st.radio(
        "Select one answer",
        options,
        format_func=lambda x: x["label"],
        key=f"radio_{question['id']}",
    )
    if st.button("Continue", type="primary", use_container_width=True, key=f"continue_{question['id']}"):
        on_answer(choice["id"], choice["label"])


def render_assessment_metric_cards(
    interest_score: float,
    aptitude_score: float,
) -> None:
    cols = st.columns(2)
    with cols[0]:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{interest_score:.0f}%</div><div class="metric-label">Interest fit</div></div>', unsafe_allow_html=True)
    with cols[1]:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{aptitude_score:.0f}%</div><div class="metric-label">Aptitude fit</div></div>', unsafe_allow_html=True)


def render_final_report(report: dict[str, Any]) -> None:
    st.markdown("## Your Top 3 Career Paths")
    st.markdown(
        f'<div class="card"><h3>Your profile</h3><p>{report.get("student_profile_summary", "")}</p><p class="small">{report.get("assessment_summary", "")}</p></div>',
        unsafe_allow_html=True,
    )

    for item in report.get("top_3", []):
        st.markdown(
            f'''<div class="result-card">
                <div class="rank">#{item.get("rank", "")} &nbsp; | &nbsp; FIT SCORE {float(item.get("fit_score", 0)):.0f}%</div>
                <h2>{item.get("career_path", "")}</h2>
                <p>{item.get("why", "")}</p>
            </div>''',
            unsafe_allow_html=True,
        )
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**BS degrees to consider**")
            for degree in item.get("degrees", []):
                st.write(f"- {degree}")
            st.markdown("**Universities to consider**")
            for uni in item.get("universities", []):
                st.write(f"- {uni}")
        with c2:
            st.markdown("**Target future jobs**")
            for job in item.get("future_jobs", []):
                st.write(f"- {job}")
            st.markdown("**What to do next**")
            for step in item.get("preparation_next_steps", []):
                st.write(f"- {step}")

    if report.get("data_note"):
        st.info(report["data_note"])
    if report.get("disclaimer"):
        st.caption(report["disclaimer"])
