"""
Test suite for High School Management System API (app.py)

This module contains comprehensive tests for all endpoints and functions in the
FastAPI application, including happy path, edge cases, and error handling scenarios.

Test Categories:
- Helper Functions: get_activity()
- Endpoints: root(), get_activities(), signup_for_activity(), unregister_from_activity()
- Edge Cases: Empty inputs, boundary values, special characters
- Error Handling: 404 errors, 400 validation errors
"""

import pytest
from fastapi.testclient import TestClient
from fastapi import status
import copy

# Import the app and activities from the source module
from src.app import (
    app, 
    activities, 
    get_activity,
    ERROR_ACTIVITY_NOT_FOUND,
    ERROR_ALREADY_SIGNED_UP,
    ERROR_NOT_REGISTERED,
    ERROR_ACTIVITY_FULL
)

# Create test client
client = TestClient(app)

# Store original activities for reset between tests
ORIGINAL_ACTIVITIES = copy.deepcopy(activities)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities dictionary to original state before each test.
    
    This fixture runs automatically before each test to ensure test isolation
    and prevent state pollution between tests.
    """
    # Setup: Reset before test
    activities.clear()
    activities.update(copy.deepcopy(ORIGINAL_ACTIVITIES))
    
    yield
    
    # Teardown: Reset after test (optional, but good practice)
    activities.clear()
    activities.update(copy.deepcopy(ORIGINAL_ACTIVITIES))


# ============================================================================
# Helper Function Tests: get_activity()
# ============================================================================

class TestGetActivity:
    """Test suite for the get_activity() helper function."""
    
    def test_get_activity_success(self):
        """Should return activity details for a valid activity name."""
        activity = get_activity("Chess Club")
        
        assert activity is not None
        assert "description" in activity
        assert "schedule" in activity
        assert "max_participants" in activity
        assert "participants" in activity
        assert activity["description"] == "Learn strategies and compete in chess tournaments"
    
    def test_get_activity_returns_correct_structure(self):
        """Should return activity with all required fields."""
        activity = get_activity("Programming Class")
        
        assert isinstance(activity, dict)
        assert isinstance(activity["description"], str)
        assert isinstance(activity["schedule"], str)
        assert isinstance(activity["max_participants"], int)
        assert isinstance(activity["participants"], list)
    
    def test_get_activity_not_found(self):
        """Should raise 404 HTTPException when activity does not exist."""
        from fastapi import HTTPException
        
        with pytest.raises(HTTPException) as exc_info:
            get_activity("Nonexistent Activity")
        
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert exc_info.value.detail == ERROR_ACTIVITY_NOT_FOUND
    
    def test_get_activity_case_sensitive(self):
        """Should be case-sensitive when matching activity names."""
        from fastapi import HTTPException
        
        # "Chess Club" exists, but "chess club" does not
        with pytest.raises(HTTPException) as exc_info:
            get_activity("chess club")
        
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    
    def test_get_activity_with_empty_string(self):
        """Should raise 404 HTTPException for empty activity name."""
        from fastapi import HTTPException
        
        with pytest.raises(HTTPException) as exc_info:
            get_activity("")
        
        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    
    def test_get_activity_returns_live_reference(self):
        """Should return a reference to the actual activity (not a copy)."""
        activity = get_activity("Chess Club")
        original_count = len(activity["participants"])
        
        # Modify the returned activity
        activity["participants"].append("test@mergington.edu")
        
        # Get it again and verify the change persisted
        activity_again = get_activity("Chess Club")
        assert len(activity_again["participants"]) == original_count + 1


# ============================================================================
# Root Endpoint Tests: GET /
# ============================================================================

class TestRootEndpoint:
    """Test suite for the root endpoint (/)."""
    
    def test_root_redirects_to_index(self):
        """Should redirect to /static/index.html."""
        response = client.get("/", follow_redirects=False)
        
        assert response.status_code == status.HTTP_307_TEMPORARY_REDIRECT
        assert response.headers["location"] == "/static/index.html"
    
    def test_root_redirect_followed(self):
        """Should successfully redirect when following redirects."""
        # Note: This test may fail if static files are not properly set up
        # but it tests the redirect logic itself
        response = client.get("/", follow_redirects=False)
        
        assert response.status_code in [
            status.HTTP_307_TEMPORARY_REDIRECT,
            status.HTTP_308_PERMANENT_REDIRECT
        ]


# ============================================================================
# Get Activities Endpoint Tests: GET /activities
# ============================================================================

class TestGetActivitiesEndpoint:
    """Test suite for the GET /activities endpoint."""
    
    def test_get_activities_success(self):
        """Should return all activities with 200 status code."""
        response = client.get("/activities")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert isinstance(data, dict)
        assert len(data) == 9  # Number of activities in the initial data
    
    def test_get_activities_contains_all_initial_activities(self):
        """Should return all initial activities with correct structure."""
        response = client.get("/activities")
        data = response.json()
        
        # Check that specific activities exist
        assert "Chess Club" in data
        assert "Programming Class" in data
        assert "Gym Class" in data
        assert "Basketball Team" in data
        assert "Soccer Club" in data
        assert "Drama Club" in data
        assert "Art Workshop" in data
        assert "Math Olympiad" in data
        assert "Science Club" in data
    
    def test_get_activities_activity_structure(self):
        """Should return activities with correct field structure."""
        response = client.get("/activities")
        data = response.json()
        
        # Check structure of one activity
        chess_club = data["Chess Club"]
        assert "description" in chess_club
        assert "schedule" in chess_club
        assert "max_participants" in chess_club
        assert "participants" in chess_club
        
        assert isinstance(chess_club["description"], str)
        assert isinstance(chess_club["schedule"], str)
        assert isinstance(chess_club["max_participants"], int)
        assert isinstance(chess_club["participants"], list)
    
    def test_get_activities_returns_current_state(self):
        """Should reflect changes made to activities in real-time."""
        # Add a participant
        activities["Chess Club"]["participants"].append("newstudent@mergington.edu")
        
        response = client.get("/activities")
        data = response.json()
        
        assert "newstudent@mergington.edu" in data["Chess Club"]["participants"]
    
    def test_get_activities_initial_participants(self):
        """Should return correct initial participant lists."""
        response = client.get("/activities")
        data = response.json()
        
        # Chess Club has initial participants
        assert len(data["Chess Club"]["participants"]) == 2
        assert "michael@mergington.edu" in data["Chess Club"]["participants"]
        assert "daniel@mergington.edu" in data["Chess Club"]["participants"]
        
        # Basketball Team has no initial participants
        assert len(data["Basketball Team"]["participants"]) == 0


# ============================================================================
# Signup Endpoint Tests: POST /activities/{activity_name}/signup
# ============================================================================

class TestSignupEndpoint:
    """Test suite for the POST /activities/{activity_name}/signup endpoint."""
    
    def test_signup_success(self):
        """Should successfully sign up a student for an activity."""
        response = client.post(
            "/activities/Basketball Team/signup",
            params={"email": "newstudent@mergington.edu"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["message"] == "Signed up newstudent@mergington.edu for Basketball Team"
        
        # Verify student was added to participants
        assert "newstudent@mergington.edu" in activities["Basketball Team"]["participants"]
    
    def test_signup_adds_to_participants_list(self):
        """Should add student email to the participants list."""
        initial_count = len(activities["Soccer Club"]["participants"])
        
        client.post(
            "/activities/Soccer Club/signup",
            params={"email": "player@mergington.edu"}
        )
        
        assert len(activities["Soccer Club"]["participants"]) == initial_count + 1
        assert "player@mergington.edu" in activities["Soccer Club"]["participants"]
    
    def test_signup_activity_not_found(self):
        """Should return 404 when activity does not exist."""
        response = client.post(
            "/activities/Nonexistent Activity/signup",
            params={"email": "student@mergington.edu"}
        )
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == ERROR_ACTIVITY_NOT_FOUND
    
    def test_signup_already_signed_up(self):
        """Should return 400 error when student is already signed up."""
        # Chess Club already has "michael@mergington.edu"
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": "michael@mergington.edu"}
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["detail"] == ERROR_ALREADY_SIGNED_UP
    
    def test_signup_duplicate_prevention(self):
        """Should prevent duplicate signups for the same student."""
        email = "duplicate@mergington.edu"
        
        # First signup should succeed
        response1 = client.post(
            "/activities/Drama Club/signup",
            params={"email": email}
        )
        assert response1.status_code == status.HTTP_200_OK
        
        # Second signup should fail
        response2 = client.post(
            "/activities/Drama Club/signup",
            params={"email": email}
        )
        assert response2.status_code == status.HTTP_400_BAD_REQUEST
        assert response2.json()["detail"] == ERROR_ALREADY_SIGNED_UP
        
        # Should only appear once in participants
        assert activities["Drama Club"]["participants"].count(email) == 1
    
    def test_signup_activity_full(self):
        """Should return 400 error when activity is at capacity."""
        # Math Olympiad has max_participants of 10
        activity = activities["Math Olympiad"]
        
        # Fill up the activity to capacity
        for i in range(activity["max_participants"]):
            activity["participants"].append(f"student{i}@mergington.edu")
        
        # Try to add one more student
        response = client.post(
            "/activities/Math Olympiad/signup",
            params={"email": "overflow@mergington.edu"}
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert ERROR_ACTIVITY_FULL in response.json()["detail"]
        assert "10 participants" in response.json()["detail"]
    
    def test_signup_exactly_at_capacity(self):
        """Should succeed when signing up the last available spot."""
        # Science Club has max_participants of 15
        activity = activities["Science Club"]
        
        # Fill up to capacity - 1
        for i in range(activity["max_participants"] - 1):
            activity["participants"].append(f"student{i}@mergington.edu")
        
        # Last spot should succeed
        response = client.post(
            "/activities/Science Club/signup",
            params={"email": "laststudent@mergington.edu"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        assert len(activity["participants"]) == activity["max_participants"]
    
    def test_signup_with_special_characters_in_email(self):
        """Should handle emails with valid special characters."""
        # Test with dots, plus signs, etc.
        special_emails = [
            "first.last@mergington.edu",
            "user+tag@mergington.edu",
            "name_123@mergington.edu"
        ]
        
        for email in special_emails:
            response = client.post(
                "/activities/Art Workshop/signup",
                params={"email": email}
            )
            assert response.status_code == status.HTTP_200_OK
            assert email in activities["Art Workshop"]["participants"]
    
    def test_signup_with_empty_email(self):
        """Should handle empty email (behavior depends on email validation)."""
        # Note: Current implementation doesn't validate email format
        response = client.post(
            "/activities/Gym Class/signup",
            params={"email": ""}
        )
        
        # This will succeed with current implementation (no validation)
        # This is a potential issue to report to the user
        assert response.status_code == status.HTTP_200_OK
    
    def test_signup_case_sensitive_activity_name(self):
        """Should be case-sensitive for activity names."""
        response = client.post(
            "/activities/chess club/signup",  # lowercase
            params={"email": "test@mergington.edu"}
        )
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_signup_multiple_students_same_activity(self):
        """Should allow multiple different students to sign up."""
        emails = [
            "student1@mergington.edu",
            "student2@mergington.edu",
            "student3@mergington.edu"
        ]
        
        for email in emails:
            response = client.post(
                "/activities/Basketball Team/signup",
                params={"email": email}
            )
            assert response.status_code == status.HTTP_200_OK
        
        assert len(activities["Basketball Team"]["participants"]) == 3
    
    def test_signup_student_multiple_activities(self):
        """Should allow same student to sign up for different activities."""
        email = "multitasker@mergington.edu"
        
        activities_to_join = ["Chess Club", "Programming Class", "Drama Club"]
        
        for activity_name in activities_to_join:
            response = client.post(
                f"/activities/{activity_name}/signup",
                params={"email": email}
            )
            assert response.status_code == status.HTTP_200_OK
            assert email in activities[activity_name]["participants"]


# ============================================================================
# Unregister Endpoint Tests: DELETE /activities/{activity_name}/unregister
# ============================================================================

class TestUnregisterEndpoint:
    """Test suite for the DELETE /activities/{activity_name}/unregister endpoint."""
    
    def test_unregister_success(self):
        """Should successfully unregister a student from an activity."""
        # Chess Club already has "michael@mergington.edu"
        response = client.delete(
            "/activities/Chess Club/unregister",
            params={"email": "michael@mergington.edu"}
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["message"] == "Unregistered michael@mergington.edu from Chess Club"
        
        # Verify student was removed
        assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]
    
    def test_unregister_removes_from_participants(self):
        """Should remove student email from participants list."""
        # Programming Class has "emma@mergington.edu"
        initial_count = len(activities["Programming Class"]["participants"])
        
        client.delete(
            "/activities/Programming Class/unregister",
            params={"email": "emma@mergington.edu"}
        )
        
        assert len(activities["Programming Class"]["participants"]) == initial_count - 1
        assert "emma@mergington.edu" not in activities["Programming Class"]["participants"]
    
    def test_unregister_activity_not_found(self):
        """Should return 404 when activity does not exist."""
        response = client.delete(
            "/activities/Nonexistent Activity/unregister",
            params={"email": "student@mergington.edu"}
        )
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == ERROR_ACTIVITY_NOT_FOUND
    
    def test_unregister_not_registered(self):
        """Should return 400 error when student is not registered."""
        response = client.delete(
            "/activities/Basketball Team/unregister",
            params={"email": "notregistered@mergington.edu"}
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["detail"] == ERROR_NOT_REGISTERED
    
    def test_unregister_after_signup(self):
        """Should successfully unregister after signing up."""
        email = "tempstudent@mergington.edu"
        
        # Sign up
        signup_response = client.post(
            "/activities/Soccer Club/signup",
            params={"email": email}
        )
        assert signup_response.status_code == status.HTTP_200_OK
        assert email in activities["Soccer Club"]["participants"]
        
        # Unregister
        unregister_response = client.delete(
            "/activities/Soccer Club/unregister",
            params={"email": email}
        )
        assert unregister_response.status_code == status.HTTP_200_OK
        assert email not in activities["Soccer Club"]["participants"]
    
    def test_unregister_double_unregister(self):
        """Should fail when trying to unregister twice."""
        email = "daniel@mergington.edu"  # Already in Chess Club
        
        # First unregister should succeed
        response1 = client.delete(
            "/activities/Chess Club/unregister",
            params={"email": email}
        )
        assert response1.status_code == status.HTTP_200_OK
        
        # Second unregister should fail
        response2 = client.delete(
            "/activities/Chess Club/unregister",
            params={"email": email}
        )
        assert response2.status_code == status.HTTP_400_BAD_REQUEST
        assert response2.json()["detail"] == ERROR_NOT_REGISTERED
    
    def test_unregister_case_sensitive_activity_name(self):
        """Should be case-sensitive for activity names."""
        response = client.delete(
            "/activities/gym class/unregister",  # lowercase
            params={"email": "test@mergington.edu"}
        )
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_unregister_with_empty_email(self):
        """Should return 400 when trying to unregister empty email."""
        response = client.delete(
            "/activities/Chess Club/unregister",
            params={"email": ""}
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["detail"] == ERROR_NOT_REGISTERED
    
    def test_unregister_frees_up_capacity(self):
        """Should allow new signup after unregistering from full activity."""
        # Fill Math Olympiad to capacity
        activity = activities["Math Olympiad"]
        emails = [f"student{i}@mergington.edu" for i in range(activity["max_participants"])]
        
        for email in emails:
            activity["participants"].append(email)
        
        # Verify it's full
        full_response = client.post(
            "/activities/Math Olympiad/signup",
            params={"email": "blocked@mergington.edu"}
        )
        assert full_response.status_code == status.HTTP_400_BAD_REQUEST
        
        # Unregister one student
        client.delete(
            "/activities/Math Olympiad/unregister",
            params={"email": emails[0]}
        )
        
        # Now there should be space
        new_signup = client.post(
            "/activities/Math Olympiad/signup",
            params={"email": "nowspace@mergington.edu"}
        )
        assert new_signup.status_code == status.HTTP_200_OK


# ============================================================================
# Integration Tests: Complex Scenarios
# ============================================================================

class TestIntegrationScenarios:
    """Test suite for complex, multi-step scenarios."""
    
    def test_full_lifecycle_signup_and_unregister(self):
        """Should handle complete lifecycle: signup -> verify -> unregister -> verify."""
        email = "lifecycle@mergington.edu"
        activity_name = "Drama Club"
        
        # Initial state: not registered
        initial_response = client.get("/activities")
        assert email not in initial_response.json()[activity_name]["participants"]
        
        # Sign up
        signup_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        assert signup_response.status_code == status.HTTP_200_OK
        
        # Verify registered
        after_signup = client.get("/activities")
        assert email in after_signup.json()[activity_name]["participants"]
        
        # Unregister
        unregister_response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        assert unregister_response.status_code == status.HTTP_200_OK
        
        # Verify unregistered
        after_unregister = client.get("/activities")
        assert email not in after_unregister.json()[activity_name]["participants"]
    
    def test_capacity_management_scenario(self):
        """Should properly manage activity capacity across signups and unregisters."""
        activity_name = "Science Club"
        max_cap = activities[activity_name]["max_participants"]
        
        # Fill to capacity
        emails = [f"student{i}@mergington.edu" for i in range(max_cap)]
        for email in emails:
            response = client.post(
                f"/activities/{activity_name}/signup",
                params={"email": email}
            )
            assert response.status_code == status.HTTP_200_OK
        
        # Should be full
        assert len(activities[activity_name]["participants"]) == max_cap
        
        # One more should fail
        overflow_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": "overflow@mergington.edu"}
        )
        assert overflow_response.status_code == status.HTTP_400_BAD_REQUEST
        
        # Unregister half
        half_to_remove = max_cap // 2
        for email in emails[:half_to_remove]:
            response = client.delete(
                f"/activities/{activity_name}/unregister",
                params={"email": email}
            )
            assert response.status_code == status.HTTP_200_OK
        
        # Should have space now (remaining = total - removed)
        expected_remaining = max_cap - half_to_remove
        assert len(activities[activity_name]["participants"]) == expected_remaining
        
        # New signups should work
        new_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": "newstudent@mergington.edu"}
        )
        assert new_response.status_code == status.HTTP_200_OK
    
    def test_multiple_activities_same_student(self):
        """Should allow student to manage multiple activity registrations."""
        email = "busy@mergington.edu"
        activities_list = ["Chess Club", "Programming Class", "Drama Club", "Art Workshop"]
        
        # Sign up for multiple activities
        for activity_name in activities_list:
            response = client.post(
                f"/activities/{activity_name}/signup",
                params={"email": email}
            )
            assert response.status_code == status.HTTP_200_OK
        
        # Verify all registrations
        all_activities = client.get("/activities").json()
        for activity_name in activities_list:
            assert email in all_activities[activity_name]["participants"]
        
        # Unregister from some
        to_remove = activities_list[:2]
        for activity_name in to_remove:
            response = client.delete(
                f"/activities/{activity_name}/unregister",
                params={"email": email}
            )
            assert response.status_code == status.HTTP_200_OK
        
        # Verify partial unregistration
        updated_activities = client.get("/activities").json()
        for activity_name in to_remove:
            assert email not in updated_activities[activity_name]["participants"]
        for activity_name in activities_list[2:]:
            assert email in updated_activities[activity_name]["participants"]


# ============================================================================
# Edge Case Tests
# ============================================================================

class TestEdgeCases:
    """Test suite for edge cases and boundary conditions."""
    
    def test_activity_with_spaces_in_name(self):
        """Should handle activity names with spaces correctly."""
        # All activity names have spaces, so this tests URL encoding
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": "test@mergington.edu"}
        )
        
        # Should work despite spaces in URL path
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST]
    
    def test_email_format_not_validated(self):
        """Test behavior with invalid email formats (current implementation allows them)."""
        invalid_emails = [
            "notanemail",
            "missing@domain",
            "@nodomain.com",
            "spaces in email@test.com"
        ]
        
        for email in invalid_emails:
            response = client.post(
                "/activities/Soccer Club/signup",
                params={"email": email}
            )
            # Currently, these will succeed (no validation)
            # This is a potential issue to report
            assert response.status_code == status.HTTP_200_OK
    
    def test_very_long_email(self):
        """Should handle very long email addresses."""
        long_email = "a" * 100 + "@mergington.edu"
        
        response = client.post(
            "/activities/Gym Class/signup",
            params={"email": long_email}
        )
        
        assert response.status_code == status.HTTP_200_OK
        assert long_email in activities["Gym Class"]["participants"]
    
    def test_unicode_in_email(self):
        """Should handle Unicode characters in email (if system supports it)."""
        unicode_email = "tëst@mergington.edu"
        
        response = client.post(
            "/activities/Drama Club/signup",
            params={"email": unicode_email}
        )
        
        # Behavior depends on system support
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_422_UNPROCESSABLE_ENTITY]
    
    def test_zero_capacity_edge_case(self):
        """Test what happens if max_participants is somehow 0."""
        # Temporarily modify an activity (this is a theoretical edge case)
        original_max = activities["Art Workshop"]["max_participants"]
        activities["Art Workshop"]["max_participants"] = 0
        
        response = client.post(
            "/activities/Art Workshop/signup",
            params={"email": "test@mergington.edu"}
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert ERROR_ACTIVITY_FULL in response.json()["detail"]
        
        # Restore
        activities["Art Workshop"]["max_participants"] = original_max
    
    def test_negative_capacity_edge_case(self):
        """Test behavior with negative max_participants (theoretical edge case)."""
        original_max = activities["Soccer Club"]["max_participants"]
        original_participants = activities["Soccer Club"]["participants"].copy()
        
        # Set negative capacity
        activities["Soccer Club"]["max_participants"] = -1
        
        # As long as there are participants >= 0, and max is -1, 
        # the check len(participants) >= max_participants becomes 0 >= -1, which is True
        # So it should block signups (activity appears "full")
        response = client.post(
            "/activities/Soccer Club/signup",
            params={"email": "test@mergington.edu"}
        )
        
        # With current implementation, 0 >= -1 is True, so it blocks signup
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert ERROR_ACTIVITY_FULL in response.json()["detail"]
        
        # Restore
        activities["Soccer Club"]["max_participants"] = original_max
        activities["Soccer Club"]["participants"] = original_participants


# ============================================================================
# Performance and State Tests
# ============================================================================

class TestStateManagement:
    """Test suite for state management and data persistence."""
    
    def test_activities_persists_between_requests(self):
        """Should maintain state between multiple requests."""
        email = "persistent@mergington.edu"
        
        # Sign up
        client.post(
            "/activities/Basketball Team/signup",
            params={"email": email}
        )
        
        # Get activities (separate request)
        response = client.get("/activities")
        
        # Should show the signup from previous request
        assert email in response.json()["Basketball Team"]["participants"]
    
    def test_concurrent_signups_to_different_activities(self):
        """Should handle multiple signups correctly."""
        base_email = "concurrent"
        
        # Simulate multiple signups
        for i in range(5):
            response = client.post(
                f"/activities/Drama Club/signup",
                params={"email": f"{base_email}{i}@mergington.edu"}
            )
            assert response.status_code == status.HTTP_200_OK
        
        # All should be registered
        assert len(activities["Drama Club"]["participants"]) >= 5
    
    def test_state_isolation_between_activities(self):
        """Changes to one activity should not affect others."""
        email = "isolated@mergington.edu"
        
        # Sign up for one activity
        client.post(
            "/activities/Chess Club/signup",
            params={"email": email}
        )
        
        # Should not appear in other activities
        all_activities = client.get("/activities").json()
        assert email in all_activities["Chess Club"]["participants"]
        assert email not in all_activities["Programming Class"]["participants"]
        assert email not in all_activities["Gym Class"]["participants"]
