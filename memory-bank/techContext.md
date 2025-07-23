# Technical Context

## Technologies Used

### Frontend
- **Streamlit**: Used for building the interactive chatbot interface
- **HTML/CSS/JavaScript**: For custom UI components if needed

### Backend
- **FastAPI**: Primary backend framework for API endpoints
- **Python**: Main programming language for backend logic

### Database
- **SQLite**: Lightweight database for storing user credentials
- **SQLAlchemy**: ORM for database interactions

### APIs
- **Gemini API**: For generating chatbot responses
- **FastAPI Authentication**: For handling JWT tokens

## Development Setup
- Python 3.12+ environment
- pip for package management
- Virtual environment recommended
- Streamlit for local development server

## Technical Constraints
- Must support user authentication
- Need to handle streaming responses from Gemini API
- Should maintain conversation history per session
