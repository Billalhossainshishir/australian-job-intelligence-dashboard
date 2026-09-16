from backend.app.services.skill_extractor import compare_skills, extract_skills


def test_normalises_skill_variants():
    text = "Python3, PowerBI, k8s, GitHub and Amazon Web Services are used in this role."
    skills = extract_skills(text)
    assert "Python" in skills
    assert "Power BI" in skills
    assert "Kubernetes" in skills
    assert "Git" in skills
    assert "AWS" in skills


def test_skill_coverage_is_transparent():
    result = compare_skills(
        "I use Python, SQL and GitHub.",
        "Required: Python, SQL, AWS, Docker and Git.",
    )
    assert result["matched_skills"] == ["Git", "Python", "SQL"]
    assert result["missing_skills"] == ["AWS", "Docker"]
    assert result["technical_skill_coverage"] == 60.0


def test_no_job_skills_returns_zero_not_hiring_probability():
    result = compare_skills("Python", "Strong communication skills required")
    assert result["job_skills"] == []
    assert result["technical_skill_coverage"] == 0.0
