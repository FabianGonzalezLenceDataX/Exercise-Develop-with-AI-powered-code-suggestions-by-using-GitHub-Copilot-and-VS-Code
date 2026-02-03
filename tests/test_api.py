"""
Tests for the High School Management System API
"""
import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from app import app, activities


@pytest.fixture
def client():
    """Create a test client"""
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """Reset activities to initial state before each test"""
    # Store original state
    original_state = {
        name: {
            "description": details["description"],
            "schedule": details["schedule"],
            "max_participants": details["max_participants"],
            "participants": details["participants"].copy()
        }
        for name, details in activities.items()
    }
    
    yield
    
    # Restore original state after test
    for name, details in original_state.items():
        activities[name]["participants"] = details["participants"].copy()


def test_root_redirect(client):
    """Test that root redirects to static index.html"""
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities(client):
    """Test getting all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    
    # Check that we have activities
    assert len(data) > 0
    assert "Chess Club" in data
    assert "Programming Class" in data
    
    # Check structure of an activity
    chess_club = data["Chess Club"]
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club


def test_signup_for_activity_success(client, reset_activities):
    """Test successful signup for an activity"""
    activity_name = "Basketball Team"
    test_email = "test@mergington.edu"
    
    response = client.post(
        f"/activities/{activity_name}/signup?email={test_email}"
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert test_email in data["message"]
    assert activity_name in data["message"]
    
    # Verify participant was added
    assert test_email in activities[activity_name]["participants"]


def test_signup_activity_not_found(client):
    """Test signup for non-existent activity"""
    response = client.post(
        "/activities/NonExistent Club/signup?email=test@mergington.edu"
    )
    
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Activity not found"


def test_signup_duplicate_participant(client, reset_activities):
    """Test signing up the same participant twice"""
    activity_name = "Chess Club"
    test_email = "michael@mergington.edu"  # Already in Chess Club
    
    response = client.post(
        f"/activities/{activity_name}/signup?email={test_email}"
    )
    
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Student already signed up for this activity"


def test_unregister_from_activity_success(client, reset_activities):
    """Test successful unregistration from an activity"""
    activity_name = "Chess Club"
    test_email = "michael@mergington.edu"  # Already in Chess Club
    
    # Verify participant is registered
    assert test_email in activities[activity_name]["participants"]
    
    response = client.delete(
        f"/activities/{activity_name}/unregister?email={test_email}"
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert test_email in data["message"]
    assert activity_name in data["message"]
    
    # Verify participant was removed
    assert test_email not in activities[activity_name]["participants"]


def test_unregister_activity_not_found(client):
    """Test unregistration from non-existent activity"""
    response = client.delete(
        "/activities/NonExistent Club/unregister?email=test@mergington.edu"
    )
    
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Activity not found"


def test_unregister_participant_not_registered(client, reset_activities):
    """Test unregistering a participant who is not registered"""
    activity_name = "Basketball Team"
    test_email = "notregistered@mergington.edu"
    
    response = client.delete(
        f"/activities/{activity_name}/unregister?email={test_email}"
    )
    
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Student is not registered for this activity"


def test_signup_and_unregister_flow(client, reset_activities):
    """Test complete flow of signing up and then unregistering"""
    activity_name = "Soccer Club"
    test_email = "flowtest@mergington.edu"
    
    # Initial state - not registered
    assert test_email not in activities[activity_name]["participants"]
    
    # Sign up
    signup_response = client.post(
        f"/activities/{activity_name}/signup?email={test_email}"
    )
    assert signup_response.status_code == 200
    assert test_email in activities[activity_name]["participants"]
    
    # Unregister
    unregister_response = client.delete(
        f"/activities/{activity_name}/unregister?email={test_email}"
    )
    assert unregister_response.status_code == 200
    assert test_email not in activities[activity_name]["participants"]


def test_activities_have_correct_structure(client):
    """Test that all activities have the expected structure"""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    
    required_fields = ["description", "schedule", "max_participants", "participants"]
    
    for activity_name, activity_details in data.items():
        for field in required_fields:
            assert field in activity_details, f"{activity_name} missing {field}"
        
        # Check data types
        assert isinstance(activity_details["description"], str)
        assert isinstance(activity_details["schedule"], str)
        assert isinstance(activity_details["max_participants"], int)
        assert isinstance(activity_details["participants"], list)


def test_multiple_signups_different_activities(client, reset_activities):
    """Test that a student can sign up for multiple activities"""
    test_email = "multisport@mergington.edu"
    activities_to_join = ["Basketball Team", "Soccer Club"]
    
    for activity_name in activities_to_join:
        response = client.post(
            f"/activities/{activity_name}/signup?email={test_email}"
        )
        assert response.status_code == 200
        assert test_email in activities[activity_name]["participants"]
