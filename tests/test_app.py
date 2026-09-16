from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def reset_activity(name="Test Activity"):
    activities[name] = {
        "description": "For testing",
        "schedule": "Mondays, 4:00 PM - 5:00 PM",
        "max_participants": 10,
        "participants": [],
    }
    return name


def test_signup_rejects_duplicate_registration():
    activity_name = reset_activity()

    first = client.post(f"/activities/{activity_name}/signup?email=student@example.com")
    second = client.post(f"/activities/{activity_name}/signup?email=student@example.com")

    assert first.status_code == 200
    assert second.status_code == 400
    assert second.json()["detail"] == "Student is already signed up"

    del activities[activity_name]


def test_unregister_participant_removes_email():
    activity_name = reset_activity()

    client.post(f"/activities/{activity_name}/signup?email=student@example.com")
    response = client.delete(f"/activities/{activity_name}/unregister?email=student@example.com")

    assert response.status_code == 200
    assert "student@example.com" not in activities[activity_name]["participants"]

    del activities[activity_name]
