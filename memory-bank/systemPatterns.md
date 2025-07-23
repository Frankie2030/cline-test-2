# System Patterns

## Architecture Overview
1. **Frontend Layer**:
   - Streamlit application for UI
   - Handles user input and displays responses
   - Manages conversation history in session state

2. **Backend Layer**:
   - FastAPI routes for authentication
   - API endpoints for chatbot interactions
   - Session management middleware

3. **Data Layer**:
   - SQLite database for user credentials
   - SQLAlchemy models for data access

## Key Technical Decisions
- **Authentication**: JWT tokens for stateless authentication
- **API Integration**: Async calls to Gemini API
- **State Management**: Streamlit session state for conversation history
- **Security**: bcrypt for password hashing

## Component Relationships
- Frontend communicates with backend via REST API
- Backend integrates with Gemini API for responses
- Database stores only user credentials (not chat history)

## Critical Paths
1. User Registration:
   Frontend → FastAPI → Database (create user)

2. Chat Interaction:
   Frontend → FastAPI → Gemini API → Frontend

3. Authentication Flow:
   Frontend → FastAPI (login) → JWT token → Frontend
