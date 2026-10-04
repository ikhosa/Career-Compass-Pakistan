from __future__ import annotations

from collections import defaultdict
from typing import Any

from question_bank import (
    APTITUDE_BY_ID,
    INTEREST_BY_ID,
    INTEREST_DIMENSIONS,
    APTITUDE_SKILLS,
)
from pakistan_data import CAREER_PROFILES


def calculate_interest_scores(history: list[dict[str, Any]]) -> dict[str, float]:
    totals = {dimension: 0.0 for dimension in INTEREST_DIMENSIONS}
    possible = {dimension: 0.0 for dimension in INTEREST_DIMENSIONS}

    for item in history:
        q = INTEREST_BY_ID.get(str(item.get("question_id")))
        if not q or "answer" not in item:
            continue
        answer = next((opt for opt in q.get("options", []) if opt["id"] == item["answer"]), None)
        if answer:
            for key in INTEREST_DIMENSIONS:
                weights = [opt.get("weights", {}).get(key, 0) for opt in q.get("options", [])]
                possible[key] += max(weights) if weights else 0
                totals[key] += answer.get("weights", {}).get(key, 0)
        elif q.get("ui") == "slider":
            value = float(item.get("answer_value", 50))
            left = q["targets"]["left"]
            right = q["targets"]["right"]
            for key in set(left) | set(right):
                max_w = max(left.get(key, 0), right.get(key, 0))
                possible[key] += max_w
                blend = (1 - value / 100) * left.get(key, 0) + (value / 100) * right.get(key, 0)
                totals[key] += blend

    scores: dict[str, float] = {}
    for key in INTEREST_DIMENSIONS:
        if possible[key] <= 0:
            scores[key] = 0.0
        else:
            scores[key] = round(min(100.0, 100.0 * totals[key] / possible[key]), 1)
    return scores


def calculate_aptitude_scores(history: list[dict[str, Any]]) -> dict[str, float]:
    correct = defaultdict(int)
    total = defaultdict(int)
    for item in history:
        q = APTITUDE_BY_ID.get(str(item.get("question_id")))
        if not q:
            continue
        skill = q["skill"]
        total[skill] += 1
        if str(item.get("answer")) == q.get("correct"):
            correct[skill] += 1

    scores: dict[str, float] = {}
    for skill in APTITUDE_SKILLS:
        scores[skill] = round(100.0 * correct[skill] / total[skill], 1) if total[skill] else 0.0
    return scores


def overall_interest_score(scores: dict[str, float]) -> float:
    populated = [v for v in scores.values() if v > 0]
    return round(sum(populated) / len(populated), 1) if populated else 0.0


def overall_aptitude_score(scores: dict[str, float], history: list[dict[str, Any]]) -> float:
    relevant_skills = {APTITUDE_BY_ID[item["question_id"]]["skill"] for item in history if item.get("question_id") in APTITUDE_BY_ID}
    values = [scores.get(skill, 0.0) for skill in relevant_skills]
    return round(sum(values) / len(values), 1) if values else 0.0


def _weighted_match(scores: dict[str, float], weights: dict[str, float]) -> float:
    total_weight = sum(weights.values())
    if total_weight <= 0:
        return 0.0
    return sum(scores.get(key, 0.0) * weight for key, weight in weights.items()) / total_weight


def build_career_candidates(
    interest_scores: dict[str, float],
    aptitude_scores: dict[str, float],
    interest_overall: float,
    aptitude_overall: float,
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for career, profile in CAREER_PROFILES.items():
        interest_fit = _weighted_match(interest_scores, profile["interest_weights"])
        aptitude_fit = _weighted_match(aptitude_scores, profile["aptitude_weights"])
        pakistan_fit = float(profile["pakistan_fit"])
        final = round(0.40 * interest_fit + 0.35 * aptitude_fit + 0.25 * pakistan_fit, 1)
        results.append(
            {
                "career_path": career,
                "fit_score": final,
                "interest_fit": round(interest_fit, 1),
                "aptitude_fit": round(aptitude_fit, 1),
                "pakistan_fit": pakistan_fit,
                "aligned_degrees": profile["degrees"],
                "universities_to_consider": profile["universities"],
                "target_jobs": profile["jobs"],
            }
        )
    return sorted(results, key=lambda x: x["fit_score"], reverse=True)
