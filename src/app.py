"""
University of La Laguna
School of Engineering and Technology
Degree in Computer Engineering
External Internships (PE)

@author Fabián González Lence <fabian.gonzalez@datax.world>
@since 2026-02-05
@file app.py
@desc High School Management System API - A FastAPI application that allows students 
      to view and sign up for extracurricular activities at Mergington High School.
      Provides REST endpoints for managing activity registrations.
@see {@link https://github.com/FabianGonzalezLenceDataX/Exercise-Develop-with-AI-powered-code-suggestions-by-using-GitHub-Copilot-and-VS-Code}
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

# Constants
STATIC_DIR_NAME = "static"
INDEX_PATH = "/static/index.html"
ERROR_ACTIVITY_NOT_FOUND = "Activity not found"
ERROR_ALREADY_SIGNED_UP = "Student already signed up for this activity"
ERROR_NOT_REGISTERED = "Student is not registered for this activity"
ERROR_ACTIVITY_FULL = "Activity is full (maximum capacity reached)"

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
app.mount(f"/{STATIC_DIR_NAME}", StaticFiles(directory=os.path.join(Path(__file__).parent,
          STATIC_DIR_NAME)), name=STATIC_DIR_NAME)

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Join the school's basketball team and compete in local leagues",
        "schedule": "Mondays and Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 15,
        "participants": []
    },
    "Soccer Club": {
        "description": "Practice soccer skills and play friendly matches",
        "schedule": "Wednesdays, 3:30 PM - 5:30 PM",
        "max_participants": 18,
        "participants": []
    },
    "Drama Club": {
        "description": "Participate in theater productions and acting workshops",
        "schedule": "Tuesdays, 4:00 PM - 5:30 PM",
        "max_participants": 25,
        "participants": []
    },
    "Art Workshop": {
        "description": "Explore painting, drawing, and other visual arts",
        "schedule": "Fridays, 2:00 PM - 3:30 PM",
        "max_participants": 20,
        "participants": []
    },
    "Math Olympiad": {
        "description": "Prepare for math competitions and solve challenging problems",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 10,
        "participants": []
    },
    "Science Club": {
        "description": "Conduct experiments and explore scientific concepts",
        "schedule": "Wednesdays, 4:00 PM - 5:00 PM",
        "max_participants": 15,
        "participants": []
    }
}


def get_activity(activity_name: str) -> dict:
    """Retrieve an activity by name or raise 404 if not found.
    
    Helper function to validate activity existence and retrieve activity data.
    Centralizes activity validation logic to avoid duplication.
    
    Args:
        activity_name (str): The name of the activity to retrieve.
    
    Returns:
        dict: The activity details dictionary containing description, schedule,
              max_participants, and participants list.
    
    Raises:
        HTTPException: 404 error if the activity name does not exist.
    
    Example:
        >>> activity = get_activity("Chess Club")
        >>> # Returns: {"description": "...", "schedule": "...", ...}
    """
    if activity_name not in activities:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                          detail=ERROR_ACTIVITY_NOT_FOUND)
    return activities[activity_name]


@app.get("/")
def root():
    """Redirect root URL to the static index page.
    
    This endpoint handles requests to the root path and redirects users
    to the main application interface served from the static files.
    
    Returns:
        RedirectResponse: A redirect response to /static/index.html
        
    Example:
        >>> # When accessing http://localhost:8000/
        >>> # User is redirected to http://localhost:8000/static/index.html
    """
    return RedirectResponse(url=INDEX_PATH)


@app.get("/activities")
def get_activities():
    """Retrieve all available extracurricular activities.
    
    Returns a dictionary containing all activities with their details including
    description, schedule, maximum participants, and current participant list.
    
    Returns:
        dict: A dictionary where keys are activity names and values are dictionaries
              containing:
              - description (str): Activity description
              - schedule (str): When the activity takes place
              - max_participants (int): Maximum number of participants allowed
              - participants (list[str]): List of registered participant emails
              
    Example:
        >>> response = get_activities()
        >>> # Returns: {"Chess Club": {"description": "...", ...}, ...}
    """
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an extracurricular activity.
    
    Registers a student (identified by email) for a specific activity.
    Validates that the activity exists and the student is not already registered.
    
    Args:
        activity_name (str): The name of the activity to sign up for.
                           Must match an existing activity key in the activities dictionary.
        email (str): The student's email address (e.g., "student@mergington.edu").
                    Used as a unique identifier for the student.
    
    Returns:
        dict: A success message dictionary with the following structure:
              {"message": "Signed up {email} for {activity_name}"}
    
    Raises:
        HTTPException: 404 error if the activity name does not exist in the system.
        HTTPException: 400 error if the student is already signed up for the activity.
    
    Example:
        >>> signup_for_activity("Chess Club", "john@mergington.edu")
        >>> # Returns: {"message": "Signed up john@mergington.edu for Chess Club"}
    """
    # Get and validate activity exists
    activity = get_activity(activity_name)

    # Validate activity is not at capacity
    if len(activity["participants"]) >= activity["max_participants"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{ERROR_ACTIVITY_FULL} ({activity['max_participants']} participants)"
        )

    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                          detail=ERROR_ALREADY_SIGNED_UP)

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str):
    """Unregister a student from an extracurricular activity.
    
    Removes a student's registration from a specific activity.
    Validates that the activity exists and the student is currently registered.
    
    Args:
        activity_name (str): The name of the activity to unregister from.
                           Must match an existing activity key in the activities dictionary.
        email (str): The student's email address (e.g., "student@mergington.edu").
                    Used to identify which student to remove from the activity.
    
    Returns:
        dict: A success message dictionary with the following structure:
              {"message": "Unregistered {email} from {activity_name}"}
    
    Raises:
        HTTPException: 404 error if the activity name does not exist in the system.
        HTTPException: 400 error if the student is not registered for the activity.
    
    Example:
        >>> unregister_from_activity("Chess Club", "john@mergington.edu")
        >>> # Returns: {"message": "Unregistered john@mergington.edu from Chess Club"}
    """
    # Get and validate activity exists
    activity = get_activity(activity_name)

    # Validate student is registered
    if email not in activity["participants"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                          detail=ERROR_NOT_REGISTERED)

    # Remove student
    activity["participants"].remove(email)
    return {"message": f"Unregistered {email} from {activity_name}"}
