from __future__ import annotations

from html import escape
from typing import Any, Callable

import streamlit as st


CSS = """
<style>
/* =========================================================
   Career Compass Pakistan - high-contrast light UI
   The application intentionally uses a light canvas so that
   labels, headings, controls, and results remain readable
   regardless of the user's Streamlit browser theme.
   ========================================================= */

:root {
    --cc-navy: #102a43;
    --cc-blue: #1d4ed8;
    --cc-blue-dark: #163fae;
    --cc-cyan: #0e7490;
    --cc-bg: #f4f7fb;
    --cc-card: #ffffff;
    --cc-text: #102a43;
    --cc-muted: #486581;
    --cc-border: #cbd5e1;
    --cc-soft-blue: #eff6ff;
    --cc-soft-green: #ecfdf5;
    --cc-green: #047857;
}

/* App canvas */
.stApp {
    background: #f4f7fb !important;
}

[data-testid="stAppViewContainer"] {
    background: #f4f7fb !important;
}

[data-testid="stHeader"] {
    background: transparent !important;
}

.block-container {
    max-width: 1200px !important;
    padding-top: 1.4rem !important;
    padding-bottom: 3rem !important;
}

/* Generic native Streamlit text */
[data-testid="stMarkdownContainer"],
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li,
[data-testid="stCaptionContainer"] {
    color: var(--cc-text);
}

/* Hero */
.hero {
    background: linear-gradient(135deg, #102a43 0%, #1e40af 56%, #0e7490 100%);
    color: #ffffff !important;
    padding: 2rem 2.2rem;
    border-radius: 24px;
    margin-bottom: 1.4rem;
    box-shadow: 0 14px 40px rgba(16, 42, 67, 0.18);
}

.hero * {
    color: #ffffff !important;
}

.hero h1 {
    margin: 0 0 0.45rem 0;
    font-size: 2.35rem;
    line-height: 1.15;
    font-weight: 800;
}

.hero p {
    margin: 0;
    color: #eef6ff !important;
    font-size: 1.05rem;
    line-height: 1.55;
}

.badge {
    display: inline-block;
    padding: 0.35rem 0.7rem;
    border: 1px solid rgba(255,255,255,0.35);
    background: rgba(255,255,255,0.10);
    border-radius: 999px;
    margin-bottom: 0.8rem;
    font-size: 0.82rem;
    font-weight: 650;
    color: #ffffff !important;
}

/* Cards */
.card,
.question-card,
.result-card,
.metric-card {
    background: #ffffff !important;
    color: var(--cc-text) !important;
    border: 1px solid var(--cc-border);
}

.card {
    border-radius: 18px;
    padding: 1.2rem 1.3rem;
    margin: 0.75rem 0;
    box-shadow: 0 8px 24px rgba(16,42,67,0.06);
}

.card h3,
.card h2,
.card h1 {
    color: var(--cc-navy) !important;
    margin-top: 0;
}

.card p,
.card li,
.card span,
.card div {
    color: var(--cc-text) !important;
}

.card .small {
    color: var(--cc-muted) !important;
}

.question-card {
    border-radius: 22px;
    padding: 1.4rem 1.45rem;
    margin-bottom: 0.95rem;
    box-shadow: 0 12px 28px rgba(16,42,67,0.07);
}

.question-card .question-number {
    color: var(--cc-blue) !important;
}

.question-number {
    font-weight: 800;
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.question-text {
    color: var(--cc-navy) !important;
    font-size: 1.45rem;
    line-height: 1.4;
    font-weight: 800;
    margin: 0.4rem 0 0.2rem;
}

.option-note,
.small {
    color: var(--cc-muted) !important;
    font-size: 0.9rem;
}

.result-card {
    border-radius: 20px;
    padding: 1.35rem;
    margin: 1rem 0;
    box-shadow: 0 10px 25px rgba(16,42,67,0.06);
}

.result-card h2,
.result-card h3 {
    color: var(--cc-navy) !important;
}

.result-card p,
.result-card li {
    color: var(--cc-text) !important;
}

.rank {
    color: var(--cc-blue) !important;
    font-weight: 850;
    font-size: 0.95rem;
}

.metric-card {
    border-radius: 18px;
    padding: 1rem;
    text-align: center;
    box-shadow: 0 8px 18px rgba(16,42,67,0.05);
}

.metric-value {
    color: var(--cc-navy) !important;
    font-size: 1.8rem;
    font-weight: 850;
}

.metric-label {
    color: var(--cc-muted) !important;
    font-size: 0.9rem;
}

.section-title {
    color: var(--cc-navy) !important;
    font-size: 1.55rem;
    font-weight: 850;
    margin: 1rem 0 0.6rem;
}

/* =========================================================
   FORM LABELS - this is the main visibility fix
   ========================================================= */

[data-testid="stTextInput"] label,
[data-testid="stSelectbox"] label,
[data-testid="stNumberInput"] label,
[data-testid="stRadio"] label,
[data-testid="stSlider"] label,
[data-testid="stTextArea"] label {
    color: var(--cc-navy) !important;
    opacity: 1 !important;
    font-weight: 750 !important;
    font-size: 0.96rem !important;
}

[data-testid="stTextInput"] label p,
[data-testid="stSelectbox"] label p,
[data-testid="stNumberInput"] label p,
[data-testid="stRadio"] label p,
[data-testid="stSlider"] label p,
[data-testid="stTextArea"] label p {
    color: var(--cc-navy) !important;
    opacity: 1 !important;
    font-weight: 750 !important;
}

/* Form control surfaces */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea,
[data-testid="stNumberInput"] input {
    background: #ffffff !important;
    color: var(--cc-navy) !important;
    border: 1px solid #94a3b8 !important;
    border-radius: 12px !important;
    opacity: 1 !important;
}

[data-testid="stTextInput"] input::placeholder,
[data-testid="stTextArea"] textarea::placeholder {
    color: #64748b !important;
    opacity: 1 !important;
}

[data-testid="stSelectbox"] > div > div {
    background: #ffffff !important;
    color: var(--cc-navy) !important;
    border-color: #94a3b8 !important;
    border-radius: 12px !important;
}

[data-testid="stSelectbox"] [role="combobox"] {
    color: var(--cc-navy) !important;
}

[data-testid="stSelectbox"] svg {
    fill: var(--cc-navy) !important;
}

/* Radio text */
[data-testid="stRadio"] [role="radiogroup"] label,
[data-testid="stRadio"] [role="radiogroup"] label p,
[data-testid="stRadio"] [role="radiogroup"] div {
    color: var(--cc-navy) !important;
    opacity: 1 !important;
}

/* Slider captions and value */
[data-testid="stSlider"] div,
[data-testid="stSlider"] p {
    color: var(--cc-navy) !important;
}

/* Captions under sliders */
[data-testid="stCaptionContainer"] p {
    color: var(--cc-muted) !important;
    opacity: 1 !important;
    font-weight: 600 !important;
}

/* Buttons */
[data-testid="stButton"] button,
[data-testid="stFormSubmitButton"] button {
    border-radius: 12px !important;
    min-height: 46px !important;
    font-weight: 750 !important;
    font-size: 0.95rem !important;
}

[data-testid="stButton"] button p,
[data-testid="stFormSubmitButton"] button p {
    font-weight: 750 !important;
}

/* Card-style answer buttons */
.answer-card-button button {
    min-height: 92px !important;
    white-space: pre-line !important;
    border: 1px solid #bfdbfe !important;
    background: #eff6ff !important;
    color: var(--cc-navy) !important;
    box-shadow: 0 4px 12px rgba(29,78,216,0.05);
}

.answer-card-button button:hover {
    border-color: var(--cc-blue) !important;
    background: #dbeafe !important;
}

/* Progress */
[data-testid="stProgressBar"] {
    margin-top: 0.4rem;
    margin-bottom: 1rem;
}

/* Info / warning / success boxes */
[data-testid="stAlert"] p,
[data-testid="stAlert"] div {
    color: var(--cc-navy) !important;
    opacity: 1 !important;
}

/* Native headings used outside our HTML */
h1, h2, h3, h4, h5, h6 {
    color: var(--cc-navy) !important;
    opacity: 1 !important;
}

/* Markdown links */
a {
    color: var(--cc-blue-dark) !important;
}

@media (max-width: 768px) {
    .block-container {
        padding-left: 0.8rem !important;
        padding-right: 0.8rem !important;
    }

    .hero {
        padding: 1.4rem;
        border-radius: 18px;
    }

    .hero h1 {
        font-size: 1.8rem;
    }

    .question-text {
        font-size: 1.2rem;
    }
}
</style>
"""


def inject_css() -> None:
    """Inject application-wide high-contrast CSS."""
    st.markdown(CSS, unsafe_allow_html=True)


def render_header() -> None:
    """Render the application header."""
    st.markdown(
        """
        <div class="hero">
            <div class="badge">AI-assisted career guidance for Pakistani intermediate students</div>
            <h1>Career Compass Pakistan</h1>
            <p>
                Discover career paths that align with your interests, aptitude and Pakistan's
                higher-education landscape.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_profile_form() -> dict[str, Any] | None:
    """Render the student onboarding form and return the submitted profile."""
    # Use explicit classes and a dedicated heading instead of relying on
    # Streamlit's theme for visibility.
    st.markdown(
        """
        <div class="card">
            <h3 style="color:#102a43 !important; margin-bottom:0.25rem;">Before we begin</h3>
            <p class="small" style="color:#486581 !important; margin-top:0;">
                Tell us a little about yourself. These background details are not counted
                as assessment questions.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("profile_form", clear_on_submit=False):
        st.markdown('<div class="section-title">Student details</div>', unsafe_allow_html=True)

        name = st.text_input(
            "Your name (optional)",
            placeholder="e.g., Ali Khan",
        )

        col1, col2 = st.columns(2)

        with col1:
            stream = st.selectbox(
                "Current intermediate stream",
                [
                    "ICS",
                    "FSc Pre-Engineering",
                    "FSc Pre-Medical",
                    "ICom",
                    "FA / Humanities",
                    "Other",
                ],
            )

            percentage = st.selectbox(
                "Expected percentage",
                [
                    "90-100%",
                    "80-89%",
                    "70-79%",
                    "60-69%",
                    "Below 60%",
                    "Not sure",
                ],
            )

        with col2:
            region = st.selectbox(
                "Preferred study region",
                [
                    "Anywhere in Pakistan",
                    "Punjab",
                    "Sindh",
                    "Khyber Pakhtunkhwa",
                    "Balochistan",
                    "Islamabad / Rawalpindi",
                ],
            )

            university_type = st.selectbox(
                "University preference",
                ["Either", "Public", "Private"],
            )

        st.markdown(
            '<p class="small" style="color:#486581 !important; margin-top:0.75rem;">'
            "You can leave your name blank if you prefer."
            "</p>",
            unsafe_allow_html=True,
        )

        submitted = st.form_submit_button(
            "Start assessment →",
            type="primary",
            use_container_width=True,
        )

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
    """Render the current assessment stage and progress."""
    phase_label = "Interest assessment" if phase == "interest" else "Aptitude assessment"
    progress = max(0.0, min(1.0, question_number / 10.0))

    st.markdown(
        f'<div class="section-title" style="margin-top:0.4rem;">{escape(phase_label)}</div>',
        unsafe_allow_html=True,
    )
    st.progress(
        progress,
        text=f"Question {question_number} of 10",
    )


def render_question(
    question: dict[str, Any],
    question_number: int,
    on_answer: Callable[[str, Any], None],
) -> None:
    """Render one adaptive question."""
    question_text = escape(str(question.get("text", "")))

    st.markdown(
        f'''
        <div class="question-card">
            <div class="question-number">Question {question_number} of 10</div>
            <div class="question-text">{question_text}</div>
        </div>
        ''',
        unsafe_allow_html=True,
    )

    if question.get("ui") == "cards":
        st.markdown(
            '<div class="option-note" style="color:#486581 !important;">Choose one option.</div>',
            unsafe_allow_html=True,
        )

        options = question.get("options", [])
        cols = st.columns(len(options))

        for idx, option in enumerate(options):
            with cols[idx]:
                emoji = str(option.get("emoji", ""))
                label = f"{emoji}\n{option['label']}" if emoji else str(option["label"])

                # HTML wrapper gives us a reliable hook for the visual cards.
                st.markdown('<div class="answer-card-button">', unsafe_allow_html=True)
                clicked = st.button(
                    label,
                    key=f"answer_{question['id']}_{option['id']}",
                    use_container_width=True,
                )
                st.markdown('</div>', unsafe_allow_html=True)

                if clicked:
                    on_answer(str(option["id"]), option["label"])
        return

    if question.get("ui") == "slider":
        # Do not hide the label entirely; an accessible label is retained while
        # the surrounding question card supplies the visual hierarchy.
        value = st.slider(
            "How would you rate this preference?",
            min_value=int(question.get("min", 0)),
            max_value=int(question.get("max", 100)),
            value=int(question.get("default", 50)),
            key=f"slider_{question['id']}",
        )

        c1, c2 = st.columns(2)
        with c1:
            st.caption(question.get("left_label", "Left"))
        with c2:
            st.caption(question.get("right_label", "Right"))

        if st.button(
            "Continue →",
            type="primary",
            use_container_width=True,
            key=f"continue_{question['id']}",
        ):
            on_answer("SLIDER", value)
        return

    # Standard multiple-choice question.
    options = question.get("options", [])

    choice = st.radio(
        "Select one answer",
        options,
        format_func=lambda x: x["label"] if isinstance(x, dict) else str(x),
        key=f"radio_{question['id']}",
    )

    if st.button(
        "Continue →",
        type="primary",
        use_container_width=True,
        key=f"continue_{question['id']}",
    ):
        if isinstance(choice, dict):
            on_answer(str(choice["id"]), choice["label"])
        else:
            on_answer(str(choice), choice)


def render_assessment_metric_cards(
    interest_score: float,
    aptitude_score: float,
) -> None:
    """Render two headline assessment metrics."""
    cols = st.columns(2)

    with cols[0]:
        st.markdown(
            f'''
            <div class="metric-card">
                <div class="metric-value">{interest_score:.0f}%</div>
                <div class="metric-label">Interest fit</div>
            </div>
            ''',
            unsafe_allow_html=True,
        )

    with cols[1]:
        st.markdown(
            f'''
            <div class="metric-card">
                <div class="metric-value">{aptitude_score:.0f}%</div>
                <div class="metric-label">Aptitude fit</div>
            </div>
            ''',
            unsafe_allow_html=True,
        )


def render_final_report(report: dict[str, Any]) -> None:
    """Render the final Top-3 recommendation report."""
    st.markdown(
        '<div class="section-title" style="font-size:1.8rem; margin-top:1.5rem;">'
        "Your Top 3 Career Paths"
        "</div>",
        unsafe_allow_html=True,
    )

    profile_summary = escape(str(report.get("student_profile_summary", "")))
    assessment_summary = escape(str(report.get("assessment_summary", "")))

    st.markdown(
        f'''
        <div class="card">
            <h3 style="color:#102a43 !important; margin-bottom:0.35rem;">Your profile</h3>
            <p style="color:#102a43 !important;">{profile_summary}</p>
            <p class="small" style="color:#486581 !important;">{assessment_summary}</p>
        </div>
        ''',
        unsafe_allow_html=True,
    )

    for item in report.get("top_3", []):
        rank = escape(str(item.get("rank", "")))
        fit_score = float(item.get("fit_score", 0) or 0)
        career_path = escape(str(item.get("career_path", "")))
        why = escape(str(item.get("why", "")))

        st.markdown(
            f'''
            <div class="result-card">
                <div class="rank">#{rank} &nbsp; | &nbsp; FIT SCORE {fit_score:.0f}%</div>
                <h2 style="color:#102a43 !important;">{career_path}</h2>
                <p style="color:#102a43 !important;">{why}</p>
            </div>
            ''',
            unsafe_allow_html=True,
        )

        c1, c2 = st.columns(2)

        with c1:
            st.markdown("### BS degrees to consider")
            for degree in item.get("degrees", []):
                st.write(f"- {degree}")

            st.markdown("### Universities to consider")
            for uni in item.get("universities", []):
                st.write(f"- {uni}")

        with c2:
            st.markdown("### Target future jobs")
            for job in item.get("future_jobs", []):
                st.write(f"- {job}")

            st.markdown("### What to do next")
            for step in item.get("preparation_next_steps", []):
                st.write(f"- {step}")

    if report.get("data_note"):
        st.info(report["data_note"])

    if report.get("disclaimer"):
        st.caption(report["disclaimer"])
