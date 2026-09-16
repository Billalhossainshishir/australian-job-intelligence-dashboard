import re

SKILL_VARIANTS: dict[str, list[str]] = {
    "Python": ["python", "python3", "python programming"],
    "Java": ["java"],
    "JavaScript": ["javascript", "java script", "js"],
    "TypeScript": ["typescript", "type script"],
    "C#": ["c#", "c sharp"],
    "C++": ["c++", "cpp"],
    "SQL": ["sql", "postgresql", "postgres", "mysql", "sql server"],
    "AWS": ["aws", "amazon web services"],
    "Azure": ["azure", "microsoft azure"],
    "GCP": ["gcp", "google cloud", "google cloud platform"],
    "Docker": ["docker", "containerisation", "containerization"],
    "Kubernetes": ["kubernetes", "k8s"],
    "Power BI": ["power bi", "powerbi"],
    "Tableau": ["tableau"],
    "Linux": ["linux", "ubuntu"],
    "Git": ["git", "github", "gitlab"],
    "Machine Learning": ["machine learning", "ml model", "scikit-learn", "sklearn"],
    "Artificial Intelligence": ["artificial intelligence", "generative ai", "genai", " ai "],
    "Cybersecurity": ["cybersecurity", "cyber security", "security operations", "soc"],
    "FastAPI": ["fastapi"],
    "Django": ["django"],
    "React": ["react", "react.js", "reactjs"],
    "Node.js": ["node.js", "nodejs", "node js"],
    "REST APIs": ["rest api", "restful", "apis", "api integration"],
    "ETL": ["etl", "elt", "data pipeline", "data pipelines"],
    "Spark": ["spark", "pyspark", "apache spark"],
    "Kafka": ["kafka", "apache kafka"],
    "Terraform": ["terraform", "infrastructure as code", "iac"],
    "CI/CD": ["ci/cd", "ci cd", "continuous integration", "continuous delivery"],
    "Networking": ["networking", "tcp/ip", "dns", "dhcp"],
    "IT Support": ["it support", "service desk", "help desk", "helpdesk"],
    "Microsoft 365": ["microsoft 365", "office 365", "m365"],
}


def _contains(text: str, variant: str) -> bool:
    if variant.strip() == "ai":
        return bool(re.search(r"\bai\b", text, flags=re.IGNORECASE))
    pattern = r"(?<![A-Za-z0-9])" + re.escape(variant) + r"(?![A-Za-z0-9])"
    return bool(re.search(pattern, text, flags=re.IGNORECASE))


def extract_skills(text: str) -> list[str]:
    found = []
    for canonical, variants in SKILL_VARIANTS.items():
        if any(_contains(text, variant.strip()) for variant in variants):
            found.append(canonical)
    return sorted(found)


def compare_skills(cv_text: str, job_description: str) -> dict:
    cv_skills = extract_skills(cv_text)
    job_skills = extract_skills(job_description)
    matched = sorted(set(cv_skills) & set(job_skills))
    missing = sorted(set(job_skills) - set(cv_skills))
    coverage = round((len(matched) / len(job_skills) * 100), 1) if job_skills else 0.0
    return {
        "cv_skills": cv_skills,
        "job_skills": job_skills,
        "matched_skills": matched,
        "missing_skills": missing,
        "technical_skill_coverage": coverage,
    }
