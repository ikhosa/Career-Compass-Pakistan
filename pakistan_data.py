from __future__ import annotations

DATA_VERSION = "2027"
DATA_LAST_VERIFIED = "2026-10-04"
THE_SOURCE_URL = "https://www.timeshighereducation.com/world-university-rankings/latest/world-ranking"
THE_PAKISTAN_SOURCE_URL = "https://www.timeshighereducation.com/student/where-to-study/study-in-pakistan?page=3"

# Current overall THE World University Rankings 2027 Pakistan leaders, verified
# from THE's country listing on 2026-10-04.
THE_TOP_3_PAKISTAN = [
    {
        "name": "Quaid-i-Azam University",
        "rank_band": "551-600",
        "year": 2027,
    },
    {
        "name": "National University of Sciences and Technology",
        "rank_band": "601-650",
        "year": 2027,
    },
    {
        "name": "COMSATS University Islamabad",
        "rank_band": "651-700",
        "year": 2027,
    },
]

THE_TOP_5_PAKISTAN = THE_TOP_3_PAKISTAN + [
    {"name": "Bahauddin Zakariya University", "rank_band": "701-800", "year": 2027},
    {"name": "University of Agriculture, Faisalabad", "rank_band": "701-800", "year": 2027},
]


# These are degree-fit university examples, not claims that they are all top-3
# overall by THE. The app deliberately keeps that distinction visible.
DEGREE_FIT_UNIVERSITIES = {
    "computing": [
        "National University of Sciences and Technology",
        "COMSATS University Islamabad",
        "FAST-NUCES",
        "LUMS",
        "Ghulam Ishaq Khan Institute of Engineering Sciences and Technology",
    ],
    "engineering": [
        "National University of Sciences and Technology",
        "University of Engineering and Technology Lahore",
        "Ghulam Ishaq Khan Institute of Engineering Sciences and Technology",
        "Pakistan Institute of Engineering and Applied Sciences",
    ],
    "medicine": [
        "Aga Khan University",
        "King Edward Medical University",
        "Dow University of Health Sciences",
        "National University of Medical Sciences",
    ],
    "business": [
        "Lahore University of Management Sciences",
        "Institute of Business Administration Karachi",
        "National University of Sciences and Technology",
    ],
    "natural_sciences": [
        "Quaid-i-Azam University",
        "Pakistan Institute of Engineering and Applied Sciences",
        "National University of Sciences and Technology",
        "University of the Punjab",
    ],
    "social_sciences": [
        "Quaid-i-Azam University",
        "Lahore University of Management Sciences",
        "Institute of Business Administration Karachi",
        "University of the Punjab",
    ],
    "creative": [
        "National College of Arts",
        "Beaconhouse National University",
        "Lahore University of Management Sciences",
    ],
}


CAREER_PROFILES = {
    "Software Engineering": {
        "interest_weights": {"technical": 1.0, "analytical": 0.9, "practical": 0.6, "research": 0.3},
        "aptitude_weights": {"computational": 1.0, "logical": 0.9, "problem_solving": 0.9, "analytical": 0.8},
        "pakistan_fit": 92,
        "degrees": ["BS Computer Science", "BS Software Engineering", "BS Information Technology"],
        "universities": DEGREE_FIT_UNIVERSITIES["computing"],
        "jobs": ["Software Engineer", "Backend/Frontend Developer", "Cloud Engineer", "QA Automation Engineer", "Freelance Software Developer"],
    },
    "AI & Data Science": {
        "interest_weights": {"analytical": 1.0, "technical": 0.8, "research": 0.8, "scientific": 0.5},
        "aptitude_weights": {"analytical": 1.0, "numerical": 1.0, "computational": 0.9, "logical": 0.8},
        "pakistan_fit": 94,
        "degrees": ["BS Artificial Intelligence", "BS Data Science", "BS Computer Science", "BS Statistics"],
        "universities": DEGREE_FIT_UNIVERSITIES["computing"],
        "jobs": ["Data Scientist", "Machine Learning Engineer", "AI Engineer", "Data Analyst", "Freelance Data Analyst"],
    },
    "Cybersecurity": {
        "interest_weights": {"technical": 1.0, "analytical": 0.9, "research": 0.6, "practical": 0.5},
        "aptitude_weights": {"logical": 1.0, "problem_solving": 1.0, "computational": 0.9, "analytical": 0.8},
        "pakistan_fit": 89,
        "degrees": ["BS Cyber Security", "BS Computer Science", "BS Information Technology"],
        "universities": DEGREE_FIT_UNIVERSITIES["computing"],
        "jobs": ["Security Analyst", "SOC Analyst", "Penetration Tester", "Security Engineer", "Cybersecurity Consultant"],
    },
    "Engineering & Robotics": {
        "interest_weights": {"technical": 0.9, "practical": 0.9, "analytical": 0.8, "scientific": 0.6},
        "aptitude_weights": {"problem_solving": 1.0, "numerical": 0.9, "spatial": 0.9, "scientific": 0.8},
        "pakistan_fit": 86,
        "degrees": ["BS Electrical Engineering", "BS Mechatronics Engineering", "BS Mechanical Engineering", "BS Electronics Engineering"],
        "universities": DEGREE_FIT_UNIVERSITIES["engineering"],
        "jobs": ["Robotics Engineer", "Embedded Systems Engineer", "Electrical Engineer", "Automation Engineer", "Systems Engineer"],
    },
    "Medicine & Healthcare": {
        "interest_weights": {"scientific": 0.9, "people": 1.0, "research": 0.6, "communication": 0.6},
        "aptitude_weights": {"scientific": 1.0, "analytical": 0.8, "verbal": 0.6, "problem_solving": 0.7},
        "pakistan_fit": 88,
        "degrees": ["MBBS", "Doctor of Physical Therapy", "Pharm-D", "BS Nursing"],
        "universities": DEGREE_FIT_UNIVERSITIES["medicine"],
        "jobs": ["Physician", "Healthcare Practitioner", "Clinical Researcher", "Pharmacist", "Health Services Manager"],
    },
    "Biotechnology & Life Sciences": {
        "interest_weights": {"scientific": 1.0, "research": 0.9, "analytical": 0.7, "people": 0.3},
        "aptitude_weights": {"scientific": 1.0, "analytical": 0.8, "problem_solving": 0.6, "numerical": 0.5},
        "pakistan_fit": 77,
        "degrees": ["BS Biotechnology", "BS Biochemistry", "BS Microbiology", "BS Bioinformatics"],
        "universities": DEGREE_FIT_UNIVERSITIES["natural_sciences"],
        "jobs": ["Biotech Researcher", "Laboratory Scientist", "Bioinformatics Analyst", "Quality Control Scientist", "Research Assistant"],
    },
    "Finance & Economics": {
        "interest_weights": {"analytical": 0.9, "business": 0.9, "communication": 0.4, "leadership": 0.4},
        "aptitude_weights": {"numerical": 1.0, "analytical": 0.9, "logical": 0.8, "verbal": 0.5},
        "pakistan_fit": 84,
        "degrees": ["BS Accounting & Finance", "BS Economics", "BS Finance", "BBA"],
        "universities": DEGREE_FIT_UNIVERSITIES["business"],
        "jobs": ["Financial Analyst", "Investment Analyst", "Risk Analyst", "Economist", "FinTech Analyst"],
    },
    "Business & Entrepreneurship": {
        "interest_weights": {"business": 1.0, "leadership": 0.9, "communication": 0.8, "people": 0.6},
        "aptitude_weights": {"verbal": 0.8, "analytical": 0.7, "problem_solving": 0.8, "numerical": 0.6},
        "pakistan_fit": 86,
        "degrees": ["BBA", "BS Management", "BS Marketing", "BS Entrepreneurship"],
        "universities": DEGREE_FIT_UNIVERSITIES["business"],
        "jobs": ["Business Analyst", "Product Manager", "Marketing Specialist", "Entrepreneur", "Growth Manager"],
    },
    "Education & Research": {
        "interest_weights": {"people": 0.8, "communication": 0.9, "research": 0.9, "scientific": 0.4},
        "aptitude_weights": {"verbal": 1.0, "analytical": 0.8, "scientific": 0.6, "problem_solving": 0.7},
        "pakistan_fit": 75,
        "degrees": ["BS Education", "BS Psychology", "BS Mathematics", "BS Physics", "BS Chemistry"],
        "universities": DEGREE_FIT_UNIVERSITIES["social_sciences"],
        "jobs": ["Teacher", "Curriculum Specialist", "Education Researcher", "Academic Researcher", "Instructional Designer"],
    },
    "Creative & Digital Media": {
        "interest_weights": {"creative": 1.0, "communication": 0.9, "business": 0.5, "leadership": 0.4},
        "aptitude_weights": {"verbal": 0.8, "spatial": 0.8, "problem_solving": 0.7, "analytical": 0.4},
        "pakistan_fit": 82,
        "degrees": ["Bachelor of Design", "BS Media Studies", "BS Communication Design", "Bachelor of Fine Arts"],
        "universities": DEGREE_FIT_UNIVERSITIES["creative"],
        "jobs": ["UX/UI Designer", "Digital Content Strategist", "Motion Designer", "Creative Producer", "Freelance Designer"],
    },
}


def top_three_the_text() -> list[str]:
    return [f"{x['name']} ({x['rank_band']}, THE WUR {x['year']})" for x in THE_TOP_3_PAKISTAN]
