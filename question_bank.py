from __future__ import annotations

from copy import deepcopy
from typing import Any


MAX_QUESTIONS = 10
VISUAL_QUESTION_SLOTS = {2, 4, 6, 8}

INTEREST_DIMENSIONS = [
    "analytical",
    "technical",
    "scientific",
    "people",
    "business",
    "creative",
    "communication",
    "practical",
    "leadership",
    "research",
]

APTITUDE_SKILLS = [
    "numerical",
    "logical",
    "verbal",
    "scientific",
    "analytical",
    "spatial",
    "computational",
    "problem_solving",
]


# The question bank is intentionally fixed. CrewAI agents choose the next item,
# but they never invent the actual question or correct answer.
INTEREST_QUESTIONS: list[dict[str, Any]] = [
    {
        "id": "INT01",
        "visual": False,
        "ui": "radio",
        "text": "A school club gives you a difficult real-world problem with no single correct solution. Which part would you enjoy most?",
        "options": [
            {"id": "A", "label": "Break the problem into smaller parts", "weights": {"analytical": 3, "research": 2}},
            {"id": "B", "label": "Build or test something that could solve it", "weights": {"technical": 3, "practical": 2}},
            {"id": "C", "label": "Understand the science behind it", "weights": {"scientific": 3, "research": 2}},
            {"id": "D", "label": "Coordinate people and present the solution", "weights": {"leadership": 2, "communication": 3}},
        ],
    },
    {
        "id": "INT02",
        "visual": True,
        "ui": "cards",
        "text": "Choose the project card that would make you most curious on a free Saturday.",
        "options": [
            {"id": "A", "emoji": "🤖", "label": "Build a small robot", "weights": {"technical": 3, "practical": 2}},
            {"id": "B", "emoji": "🧬", "label": "Investigate a biology experiment", "weights": {"scientific": 3, "research": 2}},
            {"id": "C", "emoji": "📈", "label": "Analyze a business dataset", "weights": {"analytical": 3, "business": 2}},
            {"id": "D", "emoji": "🎨", "label": "Create a visual campaign", "weights": {"creative": 3, "communication": 2}},
        ],
    },
    {
        "id": "INT03",
        "visual": False,
        "ui": "radio",
        "text": "Your team is stuck. What role do you naturally move toward?",
        "options": [
            {"id": "A", "label": "Find the evidence everyone is missing", "weights": {"research": 3, "analytical": 2}},
            {"id": "B", "label": "Try a technical prototype", "weights": {"technical": 3, "practical": 2}},
            {"id": "C", "label": "Get everyone aligned and moving", "weights": {"leadership": 3, "people": 2}},
            {"id": "D", "label": "Explain the idea in a simpler way", "weights": {"communication": 3, "creative": 1}},
        ],
    },
    {
        "id": "INT04",
        "visual": True,
        "ui": "slider",
        "text": "Move the slider toward the kind of work that feels more satisfying.",
        "min": 0,
        "max": 100,
        "default": 50,
        "left_label": "Clear rules and structure",
        "right_label": "Open-ended exploration",
        "targets": {"left": {"analytical": 2, "practical": 1}, "right": {"research": 2, "creative": 2}},
    },
    {
        "id": "INT05",
        "visual": False,
        "ui": "radio",
        "text": "Suppose a community project needs improvement. Which feedback would you most want to receive?",
        "options": [
            {"id": "A", "label": "A clearer explanation of the evidence", "weights": {"research": 2, "analytical": 2}},
            {"id": "B", "label": "A better technical implementation", "weights": {"technical": 3}},
            {"id": "C", "label": "A more useful experience for people", "weights": {"people": 3, "practical": 1}},
            {"id": "D", "label": "A more memorable design or story", "weights": {"creative": 3, "communication": 2}},
        ],
    },
    {
        "id": "INT06",
        "visual": True,
        "ui": "cards",
        "text": "Pick the challenge that feels most rewarding.",
        "options": [
            {"id": "A", "emoji": "🧩", "label": "Solve a complex logic puzzle", "weights": {"analytical": 3, "problem_solving": 1}},
            {"id": "B", "emoji": "🛠️", "label": "Fix or improve a device", "weights": {"technical": 2, "practical": 3}},
            {"id": "C", "emoji": "👩‍🏫", "label": "Help someone understand a hard topic", "weights": {"people": 2, "communication": 3}},
            {"id": "D", "emoji": "🚀", "label": "Pitch a new idea to a team", "weights": {"business": 2, "leadership": 3}},
        ],
    },
    {
        "id": "INT07",
        "visual": False,
        "ui": "radio",
        "text": "You receive an unfamiliar topic for a two-week project. What do you do first?",
        "options": [
            {"id": "A", "label": "Search for reliable sources and compare them", "weights": {"research": 3, "analytical": 2}},
            {"id": "B", "label": "Open a tool and start experimenting", "weights": {"technical": 2, "practical": 3}},
            {"id": "C", "label": "Talk with people who know the topic", "weights": {"people": 3, "communication": 2}},
            {"id": "D", "label": "Sketch possible ideas and directions", "weights": {"creative": 3, "business": 1}},
        ],
    },
    {
        "id": "INT08",
        "visual": True,
        "ui": "cards",
        "text": "Which team role looks most attractive to you?",
        "options": [
            {"id": "A", "emoji": "🔎", "label": "Data detective", "weights": {"analytical": 3, "research": 2}},
            {"id": "B", "emoji": "💻", "label": "System builder", "weights": {"technical": 3, "practical": 1}},
            {"id": "C", "emoji": "🤝", "label": "People problem-solver", "weights": {"people": 3, "communication": 2}},
            {"id": "D", "emoji": "📣", "label": "Idea leader", "weights": {"leadership": 3, "business": 2}},
        ],
    },
    {
        "id": "INT09",
        "visual": False,
        "ui": "radio",
        "text": "A project suddenly changes direction. Which response sounds most like you?",
        "options": [
            {"id": "A", "label": "Rebuild the plan using the new information", "weights": {"analytical": 3, "practical": 1}},
            {"id": "B", "label": "Prototype several alternatives", "weights": {"technical": 2, "creative": 2}},
            {"id": "C", "label": "Check how the change affects people", "weights": {"people": 3}},
            {"id": "D", "label": "Find the opportunity hidden in the change", "weights": {"business": 2, "leadership": 2}},
        ],
    },
    {
        "id": "INT10",
        "visual": False,
        "ui": "radio",
        "text": "Which kind of success would make you most proud after six months?",
        "options": [
            {"id": "A", "label": "A system that works reliably", "weights": {"technical": 3, "practical": 2}},
            {"id": "B", "label": "A discovery nobody on the team expected", "weights": {"scientific": 2, "research": 3}},
            {"id": "C", "label": "A group of people helped by your work", "weights": {"people": 3, "communication": 2}},
            {"id": "D", "label": "A new venture, campaign, or initiative you led", "weights": {"business": 3, "leadership": 2}},
        ],
    },
    {
        "id": "INT11",
        "visual": False,
        "ui": "radio",
        "text": "When learning a difficult topic, which activity keeps you engaged longest?",
        "options": [
            {"id": "A", "label": "Solving progressively harder problems", "weights": {"analytical": 3, "problem_solving": 2}},
            {"id": "B", "label": "Building a small working example", "weights": {"technical": 2, "practical": 3}},
            {"id": "C", "label": "Discussing it with another person", "weights": {"people": 2, "communication": 3}},
            {"id": "D", "label": "Connecting it to a broader idea or trend", "weights": {"research": 2, "creative": 2}},
        ],
    },
    {
        "id": "INT12",
        "visual": False,
        "ui": "radio",
        "text": "Imagine you are choosing an after-school project with friends. What would you push the group toward?",
        "options": [
            {"id": "A", "label": "A data-driven investigation", "weights": {"analytical": 2, "research": 2}},
            {"id": "B", "label": "A technology prototype", "weights": {"technical": 3}},
            {"id": "C", "label": "A community or education activity", "weights": {"people": 3, "communication": 1}},
            {"id": "D", "label": "A startup, event, or campaign", "weights": {"business": 3, "leadership": 2}},
        ],
    },
    {
        "id": "INT13",
        "visual": False,
        "ui": "radio",
        "text": "A teacher offers you a choice of feedback. Which one would you value most?",
        "options": [
            {"id": "A", "label": "Your reasoning was rigorous", "weights": {"analytical": 3}},
            {"id": "B", "label": "Your implementation was robust", "weights": {"technical": 3}},
            {"id": "C", "label": "You communicated clearly", "weights": {"communication": 3}},
            {"id": "D", "label": "You showed originality", "weights": {"creative": 3}},
        ],
    },
    {
        "id": "INT14",
        "visual": False,
        "ui": "radio",
        "text": "You are given access to a lab, makerspace, studio, and business incubator for one month. Where are you most likely to spend extra time?",
        "options": [
            {"id": "A", "label": "Lab", "weights": {"scientific": 3, "research": 2}},
            {"id": "B", "label": "Makerspace", "weights": {"technical": 2, "practical": 3}},
            {"id": "C", "label": "Studio", "weights": {"creative": 3, "communication": 1}},
            {"id": "D", "label": "Business incubator", "weights": {"business": 3, "leadership": 2}},
        ],
    },
    {
        "id": "INT15",
        "visual": False,
        "ui": "radio",
        "text": "Which statement best describes your ideal working day?",
        "options": [
            {"id": "A", "label": "Time to think deeply and solve challenging problems", "weights": {"analytical": 3, "research": 1}},
            {"id": "B", "label": "Time to build, test, and improve things", "weights": {"technical": 2, "practical": 3}},
            {"id": "C", "label": "Time with people, collaboration, and communication", "weights": {"people": 2, "communication": 3}},
            {"id": "D", "label": "Time to create, influence, or lead", "weights": {"creative": 2, "leadership": 3}},
        ],
    },
    {
        "id": "INT16",
        "visual": False,
        "ui": "radio",
        "text": "A long project becomes repetitive. What keeps you motivated?",
        "options": [
            {"id": "A", "label": "Finding a smarter method", "weights": {"analytical": 3, "technical": 1}},
            {"id": "B", "label": "Seeing a practical improvement each week", "weights": {"practical": 3}},
            {"id": "C", "label": "Seeing people benefit from progress", "weights": {"people": 3}},
            {"id": "D", "label": "Keeping the bigger vision and opportunity in mind", "weights": {"business": 2, "leadership": 2}},
        ],
    },
    {
        "id": "INT17",
        "visual": False,
        "ui": "radio",
        "text": "A friend asks for help choosing between two solutions. What do you naturally do?",
        "options": [
            {"id": "A", "label": "Compare evidence and trade-offs", "weights": {"analytical": 3}},
            {"id": "B", "label": "Test both solutions in practice", "weights": {"practical": 3, "technical": 2}},
            {"id": "C", "label": "Ask what matters most to the people involved", "weights": {"people": 3}},
            {"id": "D", "label": "Look for a creative third option", "weights": {"creative": 3}},
        ],
    },
    {
        "id": "INT18",
        "visual": False,
        "ui": "radio",
        "text": "If a topic suddenly becomes popular online, what most interests you?",
        "options": [
            {"id": "A", "label": "Whether the claims are supported by evidence", "weights": {"research": 3, "analytical": 2}},
            {"id": "B", "label": "How the technology behind it works", "weights": {"technical": 3}},
            {"id": "C", "label": "How it changes people's behavior", "weights": {"people": 3}},
            {"id": "D", "label": "How it could become a business or campaign", "weights": {"business": 3}},
        ],
    },
]


APTITUDE_QUESTIONS: list[dict[str, Any]] = [
    {"id": "APT01", "visual": False, "ui": "radio", "skill": "numerical", "difficulty": 1, "text": "A car travels 180 km in 3 hours. What is its average speed?", "options": [{"id": "A", "label": "40 km/h"}, {"id": "B", "label": "50 km/h"}, {"id": "C", "label": "60 km/h"}, {"id": "D", "label": "70 km/h"}], "correct": "C"},
    {"id": "APT02", "visual": True, "ui": "cards", "skill": "logical", "difficulty": 1, "text": "Complete the pattern: 2, 4, 8, 16, ?", "options": [{"id": "A", "emoji": "18", "label": "18"}, {"id": "B", "emoji": "24", "label": "24"}, {"id": "C", "emoji": "30", "label": "30"}, {"id": "D", "emoji": "32", "label": "32"}], "correct": "D"},
    {"id": "APT03", "visual": False, "ui": "radio", "skill": "verbal", "difficulty": 1, "text": "Choose the word closest in meaning to 'brief'.", "options": [{"id": "A", "label": "Short"}, {"id": "B", "label": "Difficult"}, {"id": "C", "label": "Bright"}, {"id": "D", "label": "Late"}], "correct": "A"},
    {"id": "APT04", "visual": True, "ui": "cards", "skill": "analytical", "difficulty": 1, "text": "A team must arrange tasks in the correct order: test before launch, design before test, research before design. Which order is correct?", "options": [{"id": "A", "emoji": "1-2-3-4", "label": "Research -> Design -> Test -> Launch"}, {"id": "B", "emoji": "2-1-3-4", "label": "Design -> Research -> Test -> Launch"}, {"id": "C", "emoji": "1-3-2-4", "label": "Research -> Test -> Design -> Launch"}, {"id": "D", "emoji": "3-1-2-4", "label": "Test -> Research -> Design -> Launch"}], "correct": "A"},
    {"id": "APT05", "visual": False, "ui": "radio", "skill": "scientific", "difficulty": 1, "text": "Plants release oxygen during photosynthesis mainly as a result of splitting which molecule?", "options": [{"id": "A", "label": "Carbon dioxide"}, {"id": "B", "label": "Water"}, {"id": "C", "label": "Glucose"}, {"id": "D", "label": "Oxygen"}], "correct": "B"},
    {"id": "APT06", "visual": True, "ui": "cards", "skill": "spatial", "difficulty": 1, "text": "Which pair is most likely to remain identical after a 180-degree rotation?", "options": [{"id": "A", "emoji": "●□", "label": "An asymmetric arrow"}, {"id": "B", "emoji": "○□", "label": "A circle beside a square"}, {"id": "C", "emoji": "⊕", "label": "A four-way symmetric cross"}, {"id": "D", "emoji": "▶", "label": "A right-pointing triangle"}], "correct": "C"},
    {"id": "APT07", "visual": False, "ui": "radio", "skill": "computational", "difficulty": 1, "text": "If a program repeats a block 5 times and each block takes 2 seconds, ignoring overhead, how long does it take?", "options": [{"id": "A", "label": "5 seconds"}, {"id": "B", "label": "7 seconds"}, {"id": "C", "label": "10 seconds"}, {"id": "D", "label": "12 seconds"}], "correct": "C"},
    {"id": "APT08", "visual": True, "ui": "cards", "skill": "problem_solving", "difficulty": 1, "text": "You need exactly 10 liters using a 7-liter and a 3-liter container. Which first move helps?", "options": [{"id": "A", "emoji": "7L", "label": "Fill the 7-liter container"}, {"id": "B", "emoji": "3L", "label": "Fill only the 3-liter container"}, {"id": "C", "emoji": "0L", "label": "Do nothing"}, {"id": "D", "emoji": "1L", "label": "Use a 1-liter container that does not exist"}], "correct": "A"},
    {"id": "APT09", "visual": False, "ui": "radio", "skill": "numerical", "difficulty": 2, "text": "A product price rises from Rs. 800 to Rs. 920. What is the percentage increase?", "options": [{"id": "A", "label": "10%"}, {"id": "B", "label": "12%"}, {"id": "C", "label": "15%"}, {"id": "D", "label": "20%"}], "correct": "C"},
    {"id": "APT10", "visual": False, "ui": "radio", "skill": "logical", "difficulty": 2, "text": "All engineers in a team know Python. Sana is an engineer. What must be true?", "options": [{"id": "A", "label": "Sana knows Python"}, {"id": "B", "label": "Sana knows Java"}, {"id": "C", "label": "Everyone who knows Python is an engineer"}, {"id": "D", "label": "No engineer knows Java"}], "correct": "A"},
    {"id": "APT11", "visual": False, "ui": "radio", "skill": "verbal", "difficulty": 2, "text": "Choose the best completion: 'Although the experiment failed initially, the team remained ___.'", "options": [{"id": "A", "label": "persistent"}, {"id": "B", "label": "careless"}, {"id": "C", "label": "silent"}, {"id": "D", "label": "random"}], "correct": "A"},
    {"id": "APT12", "visual": False, "ui": "radio", "skill": "scientific", "difficulty": 2, "text": "If force is doubled while mass stays constant, what happens to acceleration according to F = ma?", "options": [{"id": "A", "label": "It halves"}, {"id": "B", "label": "It stays the same"}, {"id": "C", "label": "It doubles"}, {"id": "D", "label": "It becomes zero"}], "correct": "C"},
    {"id": "APT13", "visual": False, "ui": "radio", "skill": "analytical", "difficulty": 2, "text": "A survey shows 60 students prefer A, 40 prefer B, and 20 prefer both. How many prefer at least one?", "options": [{"id": "A", "label": "80"}, {"id": "B", "label": "100"}, {"id": "C", "label": "120"}, {"id": "D", "label": "140"}], "correct": "B"},
    {"id": "APT14", "visual": False, "ui": "radio", "skill": "computational", "difficulty": 2, "text": "What is the binary representation of decimal 5?", "options": [{"id": "A", "label": "101"}, {"id": "B", "label": "110"}, {"id": "C", "label": "111"}, {"id": "D", "label": "100"}], "correct": "A"},
    {"id": "APT15", "visual": False, "ui": "radio", "skill": "problem_solving", "difficulty": 2, "text": "A student has 3 hours. Task A needs 75 minutes and Task B needs 90 minutes. How many minutes remain?", "options": [{"id": "A", "label": "5"}, {"id": "B", "label": "15"}, {"id": "C", "label": "20"}, {"id": "D", "label": "25"}], "correct": "B"},
    {"id": "APT16", "visual": False, "ui": "radio", "skill": "numerical", "difficulty": 3, "text": "If 3 notebooks cost Rs. 450, what is the cost of 7 notebooks at the same rate?", "options": [{"id": "A", "label": "Rs. 950"}, {"id": "B", "label": "Rs. 1,000"}, {"id": "C", "label": "Rs. 1,050"}, {"id": "D", "label": "Rs. 1,100"}], "correct": "C"},
    {"id": "APT17", "visual": False, "ui": "radio", "skill": "logical", "difficulty": 3, "text": "Four students P, Q, R and S stand in a line. P is before Q. R is after Q. S is before P. Which order is possible?", "options": [{"id": "A", "label": "P-S-Q-R"}, {"id": "B", "label": "S-P-Q-R"}, {"id": "C", "label": "Q-P-S-R"}, {"id": "D", "label": "R-S-P-Q"}], "correct": "B"},
    {"id": "APT18", "visual": False, "ui": "radio", "skill": "analytical", "difficulty": 3, "text": "A factory makes 120 units in 4 hours. At the same rate, how many units are made in 7 hours?", "options": [{"id": "A", "label": "180"}, {"id": "B", "label": "200"}, {"id": "C", "label": "210"}, {"id": "D", "label": "240"}], "correct": "C"},
    {"id": "APT19", "visual": False, "ui": "radio", "skill": "scientific", "difficulty": 3, "text": "Which condition generally increases the rate of most enzyme-catalyzed reactions up to an optimum?", "options": [{"id": "A", "label": "Moderately increasing temperature"}, {"id": "B", "label": "Removing all substrate"}, {"id": "C", "label": "Freezing the system",}, {"id": "D", "label": "Eliminating all water"}], "correct": "A"},
    {"id": "APT20", "visual": False, "ui": "radio", "skill": "verbal", "difficulty": 3, "text": "Which sentence is the clearest?", "options": [{"id": "A", "label": "The report, which was written yesterday, was reviewed by the team."}, {"id": "B", "label": "Yesterday the team reviewed the report that was written."}, {"id": "C", "label": "The team yesterday reviewed that the report was written."}, {"id": "D", "label": "Written was the report yesterday reviewed by team."}], "correct": "A"},
    {"id": "APT21", "visual": False, "ui": "radio", "skill": "spatial", "difficulty": 3, "text": "A cube has all six faces painted. If it is cut into 8 equal smaller cubes, how many small cubes have paint on exactly three faces?", "options": [{"id": "A", "label": "2"}, {"id": "B", "label": "4"}, {"id": "C", "label": "8"}, {"id": "D", "label": "12"}], "correct": "C"},
    {"id": "APT22", "visual": False, "ui": "radio", "skill": "computational", "difficulty": 3, "text": "A loop starts with i = 1 and doubles i each time until i > 16. Which values of i are visited?", "options": [{"id": "A", "label": "1, 2, 4, 8, 16"}, {"id": "B", "label": "1, 3, 5, 7, 9"}, {"id": "C", "label": "2, 4, 6, 8, 10"}, {"id": "D", "label": "1, 2, 3, 4, 5"}], "correct": "A"},
    {"id": "APT23", "visual": True, "ui": "cards", "skill": "problem_solving", "difficulty": 2, "text": "A schedule is overloaded. Which change gives the biggest immediate reduction in total time?", "options": [{"id": "A", "emoji": "-10", "label": "Remove a 10-minute task"}, {"id": "B", "emoji": "-45", "label": "Remove a 45-minute task"}, {"id": "C", "emoji": "-15", "label": "Remove a 15-minute task"}, {"id": "D", "emoji": "-5", "label": "Remove a 5-minute task"}], "correct": "B"},
    {"id": "APT24", "visual": True, "ui": "cards", "skill": "logical", "difficulty": 3, "text": "Which sequence follows the rule +2, +3, +2, +3...?", "options": [{"id": "A", "emoji": "5-7-10-12", "label": "5, 7, 10, 12"}, {"id": "B", "emoji": "5-8-10-13", "label": "5, 8, 10, 13"}, {"id": "C", "emoji": "5-6-8-9", "label": "5, 6, 8, 9"}, {"id": "D", "emoji": "5-8-11-14", "label": "5, 8, 11, 14"}], "correct": "A"},
]


def _by_id(bank: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {item["id"]: item for item in bank}


INTEREST_BY_ID = _by_id(INTEREST_QUESTIONS)
APTITUDE_BY_ID = _by_id(APTITUDE_QUESTIONS)


def get_question(bank_name: str, question_id: str) -> dict[str, Any]:
    bank = INTEREST_BY_ID if bank_name == "interest" else APTITUDE_BY_ID
    if question_id not in bank:
        raise KeyError(f"Unknown {bank_name} question: {question_id}")
    return deepcopy(bank[question_id])


def _answered_ids(history: list[dict[str, Any]]) -> set[str]:
    return {str(item.get("question_id")) for item in history}


def get_candidate_questions(
    bank_name: str,
    history: list[dict[str, Any]],
    question_number: int,
) -> list[dict[str, Any]]:
    bank = INTEREST_QUESTIONS if bank_name == "interest" else APTITUDE_QUESTIONS
    answered = _answered_ids(history)
    available = [deepcopy(q) for q in bank if q["id"] not in answered]

    if question_number in VISUAL_QUESTION_SLOTS:
        visual = [q for q in available if q.get("visual")]
        if visual:
            return visual

    return available
