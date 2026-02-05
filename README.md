# Mergington High School Activities Management System

A modern, full-stack web application for managing extracurricular activities at Mergington High School. Built with FastAPI (Python) backend and vanilla JavaScript frontend, this system allows students to browse available activities, sign up for them, and manage their registrations.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.68+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Testing](#testing)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

## Features

✨ **Core Functionality**
- Browse all available extracurricular activities with detailed information
- Real-time display of available spots for each activity
- Student signup system using email identification
- Participant management with unregistration capability
- Responsive web interface with modern UI

🛠️ **Technical Features**
- RESTful API built with FastAPI
- Interactive API documentation (Swagger UI)
- In-memory data storage
- Comprehensive test suite
- Client-side form validation
- Event delegation for dynamic content
- Error handling and user feedback

## Project Structure

```
Exercise-Develop-with-AI-powered-code-suggestions-by-using-GitHub-Copilot-and-VS-Code/
├── LICENSE                 # MIT License
├── README.md              # This file
├── requirements.txt       # Python dependencies
├── pytest.ini            # Pytest configuration
├── src/                  # Source code
│   ├── app.py           # FastAPI backend application
│   ├── README.md        # Source directory documentation
│   └── static/          # Frontend static files
│       ├── app.js       # Client-side JavaScript
│       ├── index.html   # Main HTML page
│       └── styles.css   # CSS styling
├── tests/               # Test suite
│   ├── __init__.py
│   └── test_api.py     # API endpoint tests
└── docs/               # Additional documentation
    ├── API.md         # Detailed API documentation
    └── ARCHITECTURE.md # Architecture overview
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/FabianGonzalezLenceDataX/Exercise-Develop-with-AI-powered-code-suggestions-by-using-GitHub-Copilot-and-VS-Code.git
   cd Exercise-Develop-with-AI-powered-code-suggestions-by-using-GitHub-Copilot-and-VS-Code
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   This will install:
   - `fastapi` - Modern web framework for building APIs
   - `uvicorn` - ASGI server for running FastAPI
   - `pytest` - Testing framework
   - `httpx` - HTTP client for testing

3. **Verify installation:**
   ```bash
   python -m pytest
   ```

## Usage

### Starting the Application

1. **Run the server:**
   ```bash
   cd src
   python app.py
   ```
   
   Or using uvicorn directly:
   ```bash
   uvicorn src.app:app --reload
   ```

2. **Access the application:**
   - Main application: http://localhost:8000
   - Interactive API docs (Swagger): http://localhost:8000/docs
   - Alternative API docs (ReDoc): http://localhost:8000/redoc

### Using the Web Interface

1. **Browse Activities:** View all available extracurricular activities with their descriptions, schedules, and available spots.

2. **Sign Up:** Fill out the signup form with your email and select an activity from the dropdown menu.

3. **Manage Registrations:** Click the delete button next to your name in the participants list to unregister from an activity.

### Example API Usage

**Get all activities:**
```bash
curl http://localhost:8000/activities
```

**Sign up for an activity:**
```bash
curl -X POST "http://localhost:8000/activities/Chess%20Club/signup?email=student@mergington.edu"
```

**Unregister from an activity:**
```bash
curl -X DELETE "http://localhost:8000/activities/Chess%20Club/unregister?email=student@mergington.edu"
```

## API Reference

For detailed API documentation, see [docs/API.md](docs/API.md).

### Quick Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Redirects to the main application page |
| GET | `/activities` | Retrieves all activities with details |
| POST | `/activities/{activity_name}/signup` | Sign up a student for an activity |
| DELETE | `/activities/{activity_name}/unregister` | Unregister a student from an activity |

### Available Activities

The system includes the following extracurricular activities:
- **Chess Club** - Strategy and tournament competitions
- **Programming Class** - Learn coding and build projects
- **Gym Class** - Physical education and sports
- **Basketball Team** - Competitive basketball league
- **Soccer Club** - Soccer skills and friendly matches
- **Drama Club** - Theater productions and acting
- **Art Workshop** - Painting, drawing, and visual arts
- **Math Olympiad** - Math competitions and problem-solving
- **Science Club** - Experiments and scientific exploration

## Testing

The project includes a comprehensive test suite using pytest.

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_api.py
```

### Test Coverage

The test suite covers:
- Root endpoint redirection
- Activity retrieval
- Successful signups
- Error handling (activity not found, duplicate signups)
- Participant unregistration
- Edge cases and validation

## Documentation

### Code Documentation

All source files include comprehensive documentation:

- **Python files** (`app.py`): Complete docstrings with parameter types, return values, and examples
- **JavaScript files** (`app.js`): JSDoc comments for all functions and event handlers
- **Standardized headers**: All source files include university project headers

### Additional Documentation

- [API.md](docs/API.md) - Detailed API endpoint documentation
- [ARCHITECTURE.md](docs/ARCHITECTURE.md) - System architecture and design decisions
- [src/README.md](src/README.md) - Source code overview

## Contributing

Contributions are welcome! This is a university internship project, but suggestions and improvements are appreciated.

### Development Setup

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes and add tests
4. Ensure all tests pass (`pytest`)
5. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
6. Push to the branch (`git push origin feature/AmazingFeature`)
7. Open a Pull Request

### Code Style

- Python: Follow PEP 8 guidelines
- JavaScript: Use ES6+ features
- Include docstrings/JSDoc for all functions
- Add tests for new features

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**Fabián González Lence**
- Email: fabian.gonzalez@datax.world
- University: University of La Laguna
- Program: Degree in Computer Engineering - External Internships (PE)

## Acknowledgments

- University of La Laguna - School of Engineering and Technology
- FastAPI framework for the excellent documentation and developer experience
- GitHub Copilot exercise framework

---

&copy; 2026 Fabián González Lence &bull; [MIT License](LICENSE)

