/**
 * Test suite for app.js - Client-side JavaScript functionality
 * 
 * Tests DOM interactions, API calls, event handlers, and UI updates
 * for the Mergington High School Activities management system.
 */

/**
 * Helper function to load and execute app.js in JSDOM environment
 * Must be called after DOM setup in each test
 */
function loadAppJS() {
  // Read and evaluate app.js in the current JSDOM context
  const fs = require('fs');
  const path = require('path');
  const appJSPath = path.join(__dirname, '../src/static/app.js');
  const appJSCode = fs.readFileSync(appJSPath, 'utf-8');
  
  // Execute the code (which sets up event listeners on DOMContentLoaded)
  eval(appJSCode);
  
  // Trigger DOMContentLoaded event
  const event = new Event('DOMContentLoaded');
  document.dispatchEvent(event);
}

/**
 * Setup DOM with HTML structure from index.html
 */
function setupDOM() {
  document.body.innerHTML = `
    <header>
      <h1>Mergington High School</h1>
      <h2>Extracurricular Activities</h2>
    </header>

    <main>
      <section id="activities-container">
        <h3>Available Activities</h3>
        <div id="activities-list">
          <p>Loading activities...</p>
        </div>
      </section>

      <section id="signup-container">
        <h3>Sign Up for an Activity</h3>
        <form id="signup-form">
          <div class="form-group">
            <label for="email">Student Email:</label>
            <input type="email" id="email" required placeholder="your-email@mergington.edu" />
          </div>
          <div class="form-group">
            <label for="activity">Select Activity:</label>
            <select id="activity" required>
              <option value="">-- Select an activity --</option>
            </select>
          </div>
          <button type="submit">Sign Up</button>
        </form>
        <div id="message" class="hidden"></div>
      </section>
    </main>

    <footer>
      <p>&copy; 2023 Mergington High School</p>
    </footer>
  `;
}

// Mock activities data for testing
const mockActivities = {
  "Chess Club": {
    "description": "Learn strategies and compete in chess tournaments",
    "schedule": "Fridays, 3:30 PM - 5:00 PM",
    "max_participants": 12,
    "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
  },
  "Programming Class": {
    "description": "Learn programming fundamentals",
    "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
    "max_participants": 20,
    "participants": ["emma@mergington.edu"]
  },
  "Basketball Team": {
    "description": "Join the school's basketball team",
    "schedule": "Mondays and Thursdays, 4:00 PM - 6:00 PM",
    "max_participants": 15,
    "participants": []
  }
};

describe('Mergington High School Activities - Frontend Tests', () => {
  
  beforeEach(() => {
    // Setup DOM before each test
    setupDOM();
    
    // Reset fetch mock
    global.fetch = jest.fn();
    
    // Clear all timers
    jest.clearAllTimers();
  });

  describe('DOM Initialization', () => {
    
    test('should have all required DOM elements', () => {
      expect(document.getElementById('activities-list')).toBeTruthy();
      expect(document.getElementById('activity')).toBeTruthy();
      expect(document.getElementById('signup-form')).toBeTruthy();
      expect(document.getElementById('message')).toBeTruthy();
      expect(document.getElementById('email')).toBeTruthy();
    });
    
    test('should start with loading message in activities list', () => {
      const activitiesList = document.getElementById('activities-list');
      expect(activitiesList.textContent).toContain('Loading activities');
    });
    
    test('should have hidden message div initially', () => {
      const messageDiv = document.getElementById('message');
      expect(messageDiv.classList.contains('hidden')).toBe(true);
    });
  });

  describe('Fetch Activities', () => {
    
    test('should fetch activities on page load', async () => {
      // Mock successful fetch response
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockActivities
      });
      
      // Load and execute app.js
      loadAppJS();
      
      // Wait for async operations
      await new Promise(resolve => setTimeout(resolve, 100));
      
      // Verify fetch was called
      expect(global.fetch).toHaveBeenCalledWith('/activities');
    });
    
    test('should display all activities in the list', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockActivities
      });
      
      loadAppJS();
      await new Promise(resolve => setTimeout(resolve, 100));
      
      const activitiesList = document.getElementById('activities-list');
      
      // Should contain activity names
      expect(activitiesList.innerHTML).toContain('Chess Club');
      expect(activitiesList.innerHTML).toContain('Programming Class');
      expect(activitiesList.innerHTML).toContain('Basketball Team');
    });
    
    test('should display activity details correctly', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockActivities
      });
      
      loadAppJS();
      await new Promise(resolve => setTimeout(resolve, 100));
      
      const activitiesList = document.getElementById('activities-list');
      
      // Should contain descriptions
      expect(activitiesList.innerHTML).toContain('Learn strategies and compete in chess tournaments');
      expect(activitiesList.innerHTML).toContain('Learn programming fundamentals');
      
      // Should contain schedules
      expect(activitiesList.innerHTML).toContain('Fridays, 3:30 PM - 5:00 PM');
      expect(activitiesList.innerHTML).toContain('Tuesdays and Thursdays, 3:30 PM - 4:30 PM');
    });
    
    test('should display correct number of spots left', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockActivities
      });
      
      loadAppJS();
      await new Promise(resolve => setTimeout(resolve, 100));
      
      const activitiesList = document.getElementById('activities-list');
      
      // Chess Club: 12 max - 2 participants = 10 spots left
      expect(activitiesList.innerHTML).toContain('10 spots left');
      
      // Programming Class: 20 max - 1 participant = 19 spots left
      expect(activitiesList.innerHTML).toContain('19 spots left');
      
      // Basketball Team: 15 max - 0 participants = 15 spots left
      expect(activitiesList.innerHTML).toContain('15 spots left');
    });
    
    test('should populate activity dropdown options', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockActivities
      });
      
      loadAppJS();
      await new Promise(resolve => setTimeout(resolve, 100));
      
      const activitySelect = document.getElementById('activity');
      const options = Array.from(activitySelect.options).map(opt => opt.value);
      
      // Should have placeholder plus all activities
      expect(options).toContain('');
      expect(options).toContain('Chess Club');
      expect(options).toContain('Programming Class');
      expect(options).toContain('Basketball Team');
      expect(options.length).toBe(4); // 1 placeholder + 3 activities
    });
    
    test('should display participants list for activities with participants', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockActivities
      });
      
      loadAppJS();
      await new Promise(resolve => setTimeout(resolve, 100));
      
      const activitiesList = document.getElementById('activities-list');
      
      // Should show participants for Chess Club
      expect(activitiesList.innerHTML).toContain('michael@mergington.edu');
      expect(activitiesList.innerHTML).toContain('daniel@mergington.edu');
      
      // Should show participant for Programming Class
      expect(activitiesList.innerHTML).toContain('emma@mergington.edu');
    });
    
    test('should display "No participants yet" for empty activities', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockActivities
      });
      
      loadAppJS();
      await new Promise(resolve => setTimeout(resolve, 100));
      
      const activitiesList = document.getElementById('activities-list');
      
      // Basketball Team has no participants
      expect(activitiesList.innerHTML).toContain('No participants yet');
    });
    
    test('should display error message when fetch fails', async () => {
      global.fetch.mockRejectedValueOnce(new Error('Network error'));
      
      loadAppJS();
      await new Promise(resolve => setTimeout(resolve, 100));
      
      const activitiesList = document.getElementById('activities-list');
      
      expect(activitiesList.innerHTML).toContain('Failed to load activities');
    });
    
    test('should render delete buttons for each participant', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockActivities
      });
      
      loadAppJS();
      await new Promise(resolve => setTimeout(resolve, 100));
      
      const deleteButtons = document.querySelectorAll('.delete-btn');
      
      // Chess Club (2) + Programming Class (1) = 3 delete buttons
      expect(deleteButtons.length).toBe(3);
    });
  });

  describe('Signup Form Submission', () => {
    
    beforeEach(async () => {
      // Mock initial activities fetch
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockActivities
      });
      
      loadAppJS();
      await new Promise(resolve => setTimeout(resolve, 100));
      
      // Reset fetch mock for signup tests
      global.fetch.mockClear();
    });
    
    test('should submit signup form with correct data', async () => {
      const email = 'newstudent@mergington.edu';
      const activity = 'Chess Club';
      
      // Mock signup response
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ message: `Signed up ${email} for ${activity}` })
      });
      
      // Mock refresh activities call
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockActivities
      });
      
      // Fill form
      document.getElementById('email').value = email;
      document.getElementById('activity').value = activity;
      
      // Submit form
      const form = document.getElementById('signup-form');
      const submitEvent = new Event('submit', { bubbles: true, cancelable: true });
      form.dispatchEvent(submitEvent);
      
      await new Promise(resolve => setTimeout(resolve, 100));
      
      // Verify fetch was called with correct parameters
      expect(global.fetch).toHaveBeenCalledWith(
        `/activities/${encodeURIComponent(activity)}/signup?email=${encodeURIComponent(email)}`,
        { method: 'POST' }
      );
    });
    
    test('should display success message after successful signup', async () => {
      const email = 'newstudent@mergington.edu';
      const activity = 'Chess Club';
      
      global.fetch
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({ message: `Signed up ${email} for ${activity}` })
        })
        .mockResolvedValueOnce({
          ok: true,
          json: async () => mockActivities
        });
      
      document.getElementById('email').value = email;
      document.getElementById('activity').value = activity;
      
      const form = document.getElementById('signup-form');
      form.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
      
      await new Promise(resolve => setTimeout(resolve, 100));
      
      const messageDiv = document.getElementById('message');
      expect(messageDiv.textContent).toContain('Signed up');
      expect(messageDiv.classList.contains('success')).toBe(true);
      expect(messageDiv.classList.contains('hidden')).toBe(false);
    });
    
    test('should reset form after successful signup', async () => {
      const email = 'newstudent@mergington.edu';
      const activity = 'Chess Club';
      
      global.fetch
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({ message: 'Success' })
        })
        .mockResolvedValueOnce({
          ok: true,
          json: async () => mockActivities
        });
      
      document.getElementById('email').value = email;
      document.getElementById('activity').value = activity;
      
      const form = document.getElementById('signup-form');
      form.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
      
      await new Promise(resolve => setTimeout(resolve, 100));
      
      // Form should be reset
      expect(document.getElementById('email').value).toBe('');
      expect(document.getElementById('activity').value).toBe('');
    });
    
    test('should refresh activities list after successful signup', async () => {
      global.fetch
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({ message: 'Success' })
        })
        .mockResolvedValueOnce({
          ok: true,
          json: async () => mockActivities
        });
      
      document.getElementById('email').value = 'test@test.com';
      document.getElementById('activity').value = 'Chess Club';
      
      const form = document.getElementById('signup-form');
      form.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
      
      await new Promise(resolve => setTimeout(resolve, 100));
      
      // Should have called fetch twice: once for signup, once for refresh
      expect(global.fetch).toHaveBeenCalledTimes(2);
      expect(global.fetch).toHaveBeenNthCalledWith(2, '/activities');
    });
    
    test('should display error message when signup fails', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: false,
        json: async () => ({ detail: 'Activity is full' })
      });
      
      document.getElementById('email').value = 'test@test.com';
      document.getElementById('activity').value = 'Chess Club';
      
      const form = document.getElementById('signup-form');
      form.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
      
      await new Promise(resolve => setTimeout(resolve, 100));
      
      const messageDiv = document.getElementById('message');
      expect(messageDiv.textContent).toContain('Activity is full');
      expect(messageDiv.classList.contains('error')).toBe(true);
    });
    
    test('should display generic error message when signup throws exception', async () => {
      global.fetch.mockRejectedValueOnce(new Error('Network error'));
      
      document.getElementById('email').value = 'test@test.com';
      document.getElementById('activity').value = 'Chess Club';
      
      const form = document.getElementById('signup-form');
      form.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
      
      await new Promise(resolve => setTimeout(resolve, 100));
      
      const messageDiv = document.getElementById('message');
      expect(messageDiv.textContent).toContain('Failed to sign up');
      expect(messageDiv.classList.contains('error')).toBe(true);
    });
    
    test('should handle special characters in email', async () => {
      const email = 'test+tag@mergington.edu';
      const activity = 'Chess Club';
      
      global.fetch
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({ message: 'Success' })
        })
        .mockResolvedValueOnce({
          ok: true,
          json: async () => mockActivities
        });
      
      document.getElementById('email').value = email;
      document.getElementById('activity').value = activity;
      
      const form = document.getElementById('signup-form');
      form.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
      
      await new Promise(resolve => setTimeout(resolve, 100));
      
      // Check that email is properly encoded in URL
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining(encodeURIComponent(email)),
        expect.any(Object)
      );
    });
  });

  describe('Unregister Functionality', () => {
    
    beforeEach(async () => {
      // Mock initial activities fetch
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockActivities
      });
      
      loadAppJS();
      await new Promise(resolve => setTimeout(resolve, 100));
      
      global.fetch.mockClear();
    });
    
    test('should call unregister API when delete button is clicked', async () => {
      // Mock window.confirm
      global.confirm = jest.fn(() => true);
      
      global.fetch
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({ message: 'Unregistered successfully' })
        })
        .mockResolvedValueOnce({
          ok: true,
          json: async () => mockActivities
        });
      
      // Click delete button for michael@mergington.edu in Chess Club
      const deleteButtons = document.querySelectorAll('.delete-btn');
      const firstDeleteBtn = deleteButtons[0];
      
      firstDeleteBtn.click();
      
      await new Promise(resolve => setTimeout(resolve, 100));
      
      // Should show confirm dialog
      expect(global.confirm).toHaveBeenCalled();
      
      // Should call unregister API
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/unregister'),
        expect.objectContaining({ method: 'DELETE' })
      );
    });
    
    test('should not unregister if user cancels confirmation', async () => {
      global.confirm = jest.fn(() => false);
      
      const deleteButtons = document.querySelectorAll('.delete-btn');
      deleteButtons[0].click();
      
      await new Promise(resolve => setTimeout(resolve, 100));
      
      // Should show confirm dialog
      expect(global.confirm).toHaveBeenCalled();
      
      // Should NOT call API
      expect(global.fetch).not.toHaveBeenCalled();
    });
    
    test('should display success message after successful unregister', async () => {
      global.confirm = jest.fn(() => true);
      
      global.fetch
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({ message: 'Unregistered michael@mergington.edu from Chess Club' })
        })
        .mockResolvedValueOnce({
          ok: true,
          json: async () => mockActivities
        });
      
      const deleteButtons = document.querySelectorAll('.delete-btn');
      deleteButtons[0].click();
      
      await new Promise(resolve => setTimeout(resolve, 100));
      
      const messageDiv = document.getElementById('message');
      expect(messageDiv.textContent).toContain('Unregistered');
      expect(messageDiv.classList.contains('success')).toBe(true);
    });
    
    test('should refresh activities list after unregister', async () => {
      global.confirm = jest.fn(() => true);
      
      global.fetch
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({ message: 'Success' })
        })
        .mockResolvedValueOnce({
          ok: true,
          json: async () => mockActivities
        });
      
      const deleteButtons = document.querySelectorAll('.delete-btn');
      deleteButtons[0].click();
      
      await new Promise(resolve => setTimeout(resolve, 100));
      
      // Should call fetch twice: unregister + refresh
      expect(global.fetch).toHaveBeenCalledTimes(2);
      expect(global.fetch).toHaveBeenNthCalledWith(2, '/activities');
    });
    
    test('should display error message when unregister fails', async () => {
      global.confirm = jest.fn(() => true);
      
      global.fetch.mockResolvedValueOnce({
        ok: false,
        json: async () => ({ detail: 'Student is not registered' })
      });
      
      const deleteButtons = document.querySelectorAll('.delete-btn');
      deleteButtons[0].click();
      
      await new Promise(resolve => setTimeout(resolve, 100));
      
      const messageDiv = document.getElementById('message');
      expect(messageDiv.textContent).toContain('Student is not registered');
      expect(messageDiv.classList.contains('error')).toBe(true);
    });
    
    test('should display generic error when unregister throws exception', async () => {
      global.confirm = jest.fn(() => true);
      
      global.fetch.mockRejectedValueOnce(new Error('Network error'));
      
      const deleteButtons = document.querySelectorAll('.delete-btn');
      deleteButtons[0].click();
      
      await new Promise(resolve => setTimeout(resolve, 100));
      
      const messageDiv = document.getElementById('message');
      expect(messageDiv.textContent).toContain('Failed to unregister');
      expect(messageDiv.classList.contains('error')).toBe(true);
    });
    
    test('should correctly extract activity and email from delete button', async () => {
      global.confirm = jest.fn(() => true);
      
      global.fetch
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({ message: 'Success' })
        })
        .mockResolvedValueOnce({
          ok: true,
          json: async () => mockActivities
        });
      
      const deleteButtons = document.querySelectorAll('.delete-btn');
      const secondDeleteBtn = deleteButtons[1]; // daniel@mergington.edu
      
      secondDeleteBtn.click();
      
      await new Promise(resolve => setTimeout(resolve, 100));
      
      // Check that correct data is sent
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('Chess%20Club'),
        expect.any(Object)
      );
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('daniel@mergington.edu'),
        expect.any(Object)
      );
    });
  });

  describe('Message Display', () => {
    
    beforeEach(async () => {
      jest.useFakeTimers();
      
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockActivities
      });
      
      loadAppJS();
      await new Promise(resolve => setTimeout(resolve, 0));
      
      global.fetch.mockClear();
    });
    
    afterEach(() => {
      jest.useRealTimers();
    });
    
    test('should auto-hide message after timeout', async () => {
      global.fetch
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({ message: 'Success' })
        })
        .mockResolvedValueOnce({
          ok: true,
          json: async () => mockActivities
        });
      
      document.getElementById('email').value = 'test@test.com';
      document.getElementById('activity').value = 'Chess Club';
      
      const form = document.getElementById('signup-form');
      form.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
      
      await new Promise(resolve => setTimeout(resolve, 0));
      jest.runAllTimers();
      
      const messageDiv = document.getElementById('message');
      
      // Message should be visible initially
      expect(messageDiv.classList.contains('hidden')).toBe(false);
      
      // Fast-forward time by 5 seconds
      jest.advanceTimersByTime(5000);
      
      // Message should be hidden after timeout
      expect(messageDiv.classList.contains('hidden')).toBe(true);
    });
  });

  describe('Error Handling and Edge Cases', () => {
    
    test('should handle empty activities response', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({})
      });
      
      loadAppJS();
      await new Promise(resolve => setTimeout(resolve, 100));
      
      const activitiesList = document.getElementById('activities-list');
      
      // Should clear loading message but show no activities
      expect(activitiesList.innerHTML).not.toContain('Loading activities');
    });
    
    test('should handle activity with zero max_participants', async () => {
      const weirdActivities = {
        "Full Activity": {
          "description": "This is always full",
          "schedule": "Never",
          "max_participants": 0,
          "participants": []
        }
      };
      
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => weirdActivities
      });
      
      loadAppJS();
      await new Promise(resolve => setTimeout(resolve, 100));
      
      const activitiesList = document.getElementById('activities-list');
      
      // Should show 0 spots left
      expect(activitiesList.innerHTML).toContain('0 spots left');
    });
    
    test('should handle activity with negative spots (overfilled)', async () => {
      const overfullActivities = {
        "Overfull Activity": {
          "description": "Too many people",
          "schedule": "Always",
          "max_participants": 5,
          "participants": ["1@test.com", "2@test.com", "3@test.com", "4@test.com", "5@test.com", "6@test.com"]
        }
      };
      
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => overfullActivities
      });
      
      loadAppJS();
      await new Promise(resolve => setTimeout(resolve, 100));
      
      const activitiesList = document.getElementById('activities-list');
      
      // Should show negative spots (5 - 6 = -1)
      expect(activitiesList.innerHTML).toContain('-1 spots left');
    });
    
    test('should not trigger unregister on non-delete-button clicks', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockActivities
      });
      
      loadAppJS();
      await new Promise(resolve => setTimeout(resolve, 100));
      
      global.fetch.mockClear();
      
      // Click somewhere else in the activities list
      const activitiesList = document.getElementById('activities-list');
      activitiesList.click();
      
      await new Promise(resolve => setTimeout(resolve, 100));
      
      // Should not call any API
      expect(global.fetch).not.toHaveBeenCalled();
    });
  });
});
