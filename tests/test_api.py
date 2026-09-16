from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_compare_endpoint():
    response = client.post(
        "/compare",
        json={
            "cv_text": "Python SQL Git Docker",
            "job_description": "Python SQL AWS Docker Git",
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["technical_skill_coverage"] == 80.0
    assert payload["missing_skills"] == ["AWS"]


def test_skills_endpoint_contains_core_dictionary():
    response = client.get("/skills")
    assert response.status_code == 200
    skills = response.json()["skills"]
    assert "Python" in skills
    assert "SQL" in skills
    assert "AWS" in skills
