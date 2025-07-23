Here is a detailed development plan for the chatbot system, based on the project brief and existing memory bank documentation:

## Development Plan: Chatbot System

### 1. Project Setup and Environment Configuration

**Goal:** Establish the foundational project structure and ensure all necessary dependencies are in place for both frontend and backend development.

**Tasks:**
*   **Create Project Directory Structure:**
    *   `/src` (main source code)
    *   `/src/backend` (FastAPI application)
    *   `/src/frontend` (Streamlit application)
    *   `/src/database` (Database initialization and models)
    *   `/src/utils` (Utility functions, e.g., password hashing, JWT handling)
    *   `/src/api` (Gemini API integration)
*   **Initialize Python Virtual Environment:** Create and activate a virtual environment for dependency management.
*   **Install Backend Dependencies:** Install FastAPI, Uvicorn, SQLAlchemy, python-jose[cryptography], passlib[bcrypt], and python-dotenv.
*   **Install Frontend Dependencies:** Install Streamlit.
*   **Create `requirements.txt`:** Document all Python dependencies for easy environment replication.
*   **Create `.env` file (for development):** Placeholder for environment variables like `GEMINI_API_KEY` and `SECRET_KEY` for JWT. (Note: This file will not be read or modified by Cline for security reasons, but its existence is part of the plan).

### 2. Backend Development (FastAPI)

**Goal:** Implement the core API endpoints for user authentication and chatbot interaction.

**Tasks:**

#### 2.1. Database Setup (SQLite & SQLAlchemy)
*   **Define SQLAlchemy Models:** Create models for `User` (username, hashed password).
*   **Database Initialization:** Implement a function to create the SQLite database file and tables if they don't exist.
*   **Database Session Management:** Set up dependency injection for database sessions in FastAPI.

#### 2.2. User Authentication
*   **Password Hashing Utility:** Implement a utility function using `passlib[bcrypt]` to hash and verify passwords.
*   **JWT Token Utilities:**
    *   Function to create JWT access tokens (encoding user ID/username, expiration).
    *   Function to decode and verify JWT tokens.
*   **Authentication Endpoints:**
    *   **`/register` (POST):**
        *   Accept username and password.
        *   Hash password.
        *   Store user in SQLite database.
        *   Return success message or JWT token upon registration.
    *   **`/login` (POST):**
        *   Accept username and password.
        *   Verify password against hashed password in DB.
        *   Generate and return a JWT access token.
    *   **`/logout` (POST):** (Optional, as JWTs are stateless, but can be used for client-side token invalidation or session management if needed).
*   **Authentication Dependency:** Create a FastAPI dependency to protect routes, requiring a valid JWT token.

#### 2.3. Chatbot API Endpoint
*   **`/chat` (POST):**
    *   Accept user query and potentially conversation history.
    *   Require authentication (JWT).
    *   Integrate with Gemini API to get a response.
    *   Return the chatbot's response.

### 3. Frontend Development (Streamlit)

**Goal:** Build an intuitive user interface for authentication and chatbot interaction.

**Tasks:**

#### 3.1. Streamlit Application Structure
*   **Main Application File:** `app.py` in `/src/frontend`.
*   **Page Navigation:** Implement conditional rendering or Streamlit's multipage feature for different views (Login/Register, Chat).

#### 3.2. User Authentication Interface
*   **Login Page:**
    *   Input fields for username and password.
    *   Login button.
    *   Display error messages for invalid credentials.
    *   Navigation to registration page.
*   **Registration Page:**
    *   Input fields for username and password.
    *   Register button.
    *   Display success/error messages.
    *   Navigation back to login page.
*   **Session Management:** Store JWT token in Streamlit's session state after successful login.

#### 3.3. Chat Interface
*   **Chat Input:** Text area for users to type queries.
*   **Send Button:** To submit queries.
*   **Conversation Display:** Area to show the history of queries and responses.
*   **Logout Button:** To clear session and navigate to login page.
*   **Conversation History Management:** Store chat messages in Streamlit's session state.

### 4. Gemini API Integration

**Goal:** Connect the FastAPI backend to the Gemini API for generating chatbot responses.

**Tasks:**
*   **API Client Setup:** Initialize the Gemini API client in the backend.
*   **Request Handling:** Format user queries for the Gemini API.
*   **Response Parsing:** Extract and return the chatbot's response from the Gemini API.
*   **Error Handling:** Implement robust error handling for Gemini API calls (e.g., rate limits, invalid API key, network issues).

### 5. Error Handling and Security

**Goal:** Ensure the system is robust, secure, and provides clear feedback.

**Tasks:**
*   **Backend Error Handling:** Implement FastAPI exception handlers for common errors (e.g., 401 Unauthorized, 400 Bad Request, 404 Not Found, 500 Internal Server Error).
*   **Frontend Error Display:** Display user-friendly error messages in the Streamlit interface.
*   **Password Security:** Ensure bcrypt is correctly used for hashing and verification.
*   **JWT Security:**
    *   Use a strong, securely stored `SECRET_KEY`.
    *   Set appropriate expiration times for tokens.
    *   Consider refresh tokens for long-lived sessions (if required for scalability, currently out of scope based on brief).
*   **Input Validation:** Validate all user inputs on both frontend and backend to prevent injection attacks and ensure data integrity.

### 6. Testing Strategy

**Goal:** Verify the functionality and robustness of the system.

**Tasks:**
*   **Unit Tests:**
    *   Test password hashing/verification utilities.
    *   Test JWT token generation/verification.
    *   Test database operations (user creation, retrieval).
    *   Test Gemini API integration (mocking external calls).
*   **Integration Tests:**
    *   Test authentication flow (register, login, access protected route).
    *   Test chat interaction from frontend to backend to Gemini API and back.
*   **Security Testing:** Basic checks for common vulnerabilities (e.g., unhashed passwords, exposed API keys).

### 7. Deployment Considerations (Brief)

**Goal:** Outline steps for future deployment.

**Tasks:**
*   **Containerization (Optional but Recommended):** Create a Dockerfile for the FastAPI backend.
*   **Vercel Deployment:** Understand how to deploy Streamlit applications and FastAPI backends on Vercel.
*   **Environment Variables:** Ensure secure handling of `GEMINI_API_KEY` and `SECRET_KEY` in production environments (e.g., Vercel environment variables).

This plan provides a clear roadmap for developing the chatbot system. Please let me know if you would like any adjustments or further details on specific sections. Once you are satisfied with the plan, please toggle to Act mode to begin implementation.