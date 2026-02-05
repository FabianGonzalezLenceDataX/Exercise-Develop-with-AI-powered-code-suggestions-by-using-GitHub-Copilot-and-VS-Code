/**
 * University of La Laguna
 * School of Engineering and Technology
 * Degree in Computer Engineering
 * External Internships (PE)
 *
 * @author Fabián González Lence <fabian.gonzalez@datax.world>
 * @since 2026-02-05
 * @file app.js
 * @desc Client-side JavaScript for Mergington High School Activities management system.
 *       Handles fetching activities from the API, displaying them in the UI,
 *       managing activity signups, and handling participant unregistration.
 * @see {@link https://github.com/FabianGonzalezLenceDataX/Exercise-Develop-with-AI-powered-code-suggestions-by-using-GitHub-Copilot-and-VS-Code}
 */

// Constants
const MESSAGE_HIDE_TIMEOUT = 5000;
const ERROR_LOAD_ACTIVITIES = "Failed to load activities. Please try again later.";
const ERROR_UNREGISTER_FAILED = "Failed to unregister. Please try again.";
const ERROR_SIGNUP_FAILED = "Failed to sign up. Please try again.";
const ERROR_GENERIC = "An error occurred";

document.addEventListener("DOMContentLoaded", () => {
  const activitiesList = document.getElementById("activities-list");
  const activitySelect = document.getElementById("activity");
  const signupForm = document.getElementById("signup-form");
  const messageDiv = document.getElementById("message");

  /**
   * Display a message to the user with auto-hide functionality.
   * 
   * Shows a success or error message in the message div and automatically
   * hides it after a specified timeout.
   * 
   * @function displayMessage
   * @param {string} message - The message text to display
   * @param {string} type - The message type: "success" or "error"
   * @param {number} [hideAfter=MESSAGE_HIDE_TIMEOUT] - Milliseconds before hiding (default: 5000)
   * 
   * @example
   * displayMessage("Signup successful!", "success");
   * displayMessage("An error occurred", "error");
   */
  function displayMessage(message, type, hideAfter = MESSAGE_HIDE_TIMEOUT) {
    messageDiv.textContent = message;
    messageDiv.className = type;
    messageDiv.classList.remove("hidden");

    setTimeout(() => {
      messageDiv.classList.add("hidden");
    }, hideAfter);
  }

  /**
   * Fetches all activities from the API and updates the UI.
   * 
   * Retrieves the list of extracurricular activities from the backend API,
   * populates activity cards with details, and fills the signup dropdown menu.
   * Automatically displays participant lists with delete buttons for each.
   * 
   * @async
   * @function fetchActivities
   * @returns {Promise<void>} Resolves when activities are fetched and UI is updated
   * @throws {Error} Logs error to console if API fetch fails
   * 
   * @example
   * // Called automatically on page load and after signup/unregister
   * await fetchActivities();
   */
  async function fetchActivities() {
    try {
      const response = await fetch("/activities");
      const activities = await response.json();

      // Clear loading message
      activitiesList.innerHTML = "";
      
      // Clear and reset activity dropdown
      activitySelect.innerHTML = '<option value="">-- Select an activity --</option>';

      // Populate activities list
      Object.entries(activities).forEach(([name, details]) => {
        const activityCard = document.createElement("div");
        activityCard.className = "activity-card";

        const spotsLeft = details.max_participants - details.participants.length;

        // Participants list HTML
        let participantsHTML = "";
        if (details.participants.length > 0) {
          participantsHTML = `
            <div class="participants-section">
              <strong>Participants:</strong>
              <ul class="participants-list">
                ${details.participants.map(email => `
                  <li>
                    <span class="participant-email">${email}</span>
                    <button class="delete-btn" data-activity="${name}" data-email="${email}" title="Unregister">
                      <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                        <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"/>
                        <path fill-rule="evenodd" d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"/>
                      </svg>
                    </button>
                  </li>
                `).join("")}
              </ul>
            </div>
          `;
        } else {
          participantsHTML = `
            <div class="participants-section">
              <strong>Participants:</strong>
              <p class="no-participants">No participants yet.</p>
            </div>
          `;
        }

        activityCard.innerHTML = `
          <h4>${name}</h4>
          <p>${details.description}</p>
          <p><strong>Schedule:</strong> ${details.schedule}</p>
          <p><strong>Availability:</strong> ${spotsLeft} spots left</p>
          ${participantsHTML}
        `;

        activitiesList.appendChild(activityCard);

        // Add option to select dropdown
        const option = document.createElement("option");
        option.value = name;
        option.textContent = name;
        activitySelect.appendChild(option);
      });
    } catch (error) {
      activitiesList.innerHTML = `<p>${ERROR_LOAD_ACTIVITIES}</p>`;
      console.error("Error fetching activities:", error);
    }
  }

  /**
   * Handles unregistering participants from activities using event delegation.
   * 
   * Listens for clicks on delete buttons within the activities list.
   * Prompts for confirmation before unregistering a student from an activity.
   * Updates the UI and displays success/error messages after the operation.
   * 
   * @event click
   * @async
   * @param {MouseEvent} event - The click event from the activities list
   * @returns {Promise<void>} Resolves when unregistration is complete
   * 
   * @example
   * // Automatically handles clicks on delete buttons in participant lists
   * // User confirms: "Are you sure you want to unregister user@email.com from Chess Club?"
   */
  activitiesList.addEventListener("click", async (event) => {
    const deleteBtn = event.target.closest(".delete-btn");
    if (!deleteBtn) return;

    const activity = deleteBtn.getAttribute("data-activity");
    const email = deleteBtn.getAttribute("data-email");

    if (!confirm(`Are you sure you want to unregister ${email} from ${activity}?`)) {
      return;
    }

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activity)}/unregister?email=${encodeURIComponent(email)}`,
        {
          method: "DELETE",
        }
      );

      const result = await response.json();

      if (response.ok) {
        displayMessage(result.message, "success");
        // Refresh activities list
        await fetchActivities();
      } else {
        displayMessage(result.detail || ERROR_GENERIC, "error");
      }
    } catch (error) {
      displayMessage(ERROR_UNREGISTER_FAILED, "error");
      console.error("Error unregistering:", error);
    }
  });

  /**
   * Handles the activity signup form submission.
   * 
   * Processes student registration for extracurricular activities.
   * Validates form input, sends signup request to API, displays result messages,
   * and refreshes the activities list upon successful registration.
   * 
   * @event submit
   * @async
   * @param {Event} event - The form submission event
   * @returns {Promise<void>} Resolves when signup is complete
   * 
   * @example
   * // User fills form with email "student@mergington.edu" and selects "Chess Club"
   * // Form submits and displays: "Signed up student@mergington.edu for Chess Club"
   */
  signupForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const activity = document.getElementById("activity").value;

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activity)}/signup?email=${encodeURIComponent(email)}`,
        {
          method: "POST",
        }
      );

      const result = await response.json();

      if (response.ok) {
        displayMessage(result.message, "success");
        signupForm.reset();
        // Refresh activities list
        await fetchActivities();
      } else {
        displayMessage(result.detail || ERROR_GENERIC, "error");
      }
    } catch (error) {
      displayMessage(ERROR_SIGNUP_FAILED, "error");
      console.error("Error signing up:", error);
    }
  });

  /**
   * Initialize the application by fetching and displaying activities.
   * Called automatically when the DOM content is fully loaded.
   */
  fetchActivities();
});
