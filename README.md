# Career Compass Pakistan

A flat-repository Streamlit + CrewAI Flow application for career guidance for Pakistani intermediate / Grade 12 students.

## Architecture

- `app.py` - Streamlit entry point and session-state controller
- `ui.py` - high-contrast visual interface
- `career_flow.py` - CrewAI Flow orchestration
- `interest_agent.py` - Agent 1: adaptive interest questioning + summary
- `aptitude_agent.py` - Agent 2: adaptive aptitude questioning + summary
- `pakistan_agent.py` - Agent 3: Pakistan degree/university/job context
- `recommendation_agent.py` - Agent 4: final top-3 recommendations
- `models.py` - Pydantic structured outputs and Flow state
- `config.py` - Grok configuration
- `scoring.py` - deterministic scoring and career-fit formula
- `question_bank.py` - validated fixed question bank
- `pakistan_data.py` - verified Pakistan ranking/context dataset
- `requirements.txt` - Streamlit + CrewAI/LiteLLM dependencies

## LLM

The application uses xAI Grok 4.7 through CrewAI's LiteLLM path.

## No local installation required

Push these files to GitHub and deploy with Streamlit Community Cloud.

## Streamlit secret

In Streamlit Cloud, add one secret:

```toml
XAI_API_KEY = "your-xai-api-key"
```

Never commit the API key to GitHub.

## Deployment

1. Create a GitHub repository.
2. Upload every file in this repository to the repository root. No subfolders are required.
3. Open Streamlit Community Cloud.
4. Create a new app and select the GitHub repository.
5. Select `app.py` as the entry point.
6. Use Python 3.12.
7. Add `XAI_API_KEY` in Streamlit Secrets.
8. Deploy.

## Questioning design

Each assessment uses exactly 10 questions, which satisfies the maximum of 10 while guaranteeing four visual interactions at questions 2, 4, 6, and 8. The LLM agent dynamically chooses each question from the approved bank based on the student's previous answers.

## Scoring

Final career fit is deterministic:

`40% Interest + 35% Aptitude + 25% Pakistan alignment`

The LLM does not invent test scores, correct answers, or university rank bands.

## Important data note

`pakistan_data.py` currently stores the Times Higher Education World University Rankings 2027 top three Pakistan entries verified on 2026-10-04. Review/update this file when a new ranking edition becomes available.
