# Chatbot System Usage Documentation

This document provides instructions on how to set up, run, and use the Chatbot System, which includes a FastAPI backend and a Streamlit frontend.

## 1. Initial Setup Guide

To get started with the Chatbot System, follow these steps:

### 1.1. Prerequisites

Ensure you have the following software installed on your system:

*   **Python 3.x**: It is recommended to use Python 3.8 or higher.
*   **pip**: Python's package installer (usually comes with Python).
*   **Virtual Environment**: Recommended for managing project dependencies.

### 1.2. Project Setup

1.  **Clone the Repository (or download project files):**
    If you have the project in a Git repository, clone it using:
    ```bash
    git clone <repository_url>
    cd <project_directory>
    ```
    Otherwise, navigate to the directory where you have downloaded the project files.

2.  **Create and Activate a Python Virtual Environment:**
    It's good practice to create a virtual environment to isolate project dependencies.
    ```bash
    python3 -m venv venv
    ```
    Activate the virtual environment:
    *   **macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```
    *   **Windows (Command Prompt):**
        ```bash
        .\venv\Scripts\activate.bat
        ```
    *   **Windows (PowerShell):**
        ```bash
        .\venv\Scripts\Activate.ps1
        ```

3.  **Install Dependencies:**
    Install all required Python packages using `pip`:
    ```bash
    pip install -r requirements.txt
    ```

### 1.3. Environment Variables

The system requires a `GEMINI_API_KEY` to interact with the Gemini API.

1.  **Create a `.env` file:**
    In the root directory of your project, create a file named `.env`.

2.  **Set `GEMINI_API_KEY`:**
    Add your Gemini API key to the `.env` file in the following format:
    ```
    GEMINI_API_KEY="your_gemini_api_key_here"
    ```
    Replace `"your_gemini_api_key_here"` with your actual Gemini API key.

### 1.4. Database Initialization

The project uses SQLite for user data. You need to initialize the database schema:

```bash
python -c "from src.database.database import init_db; init_db()"
```
This command will create the `test.db` file and set up the necessary tables.

## 2. Running the Backend (FastAPI)

The FastAPI backend handles user authentication and chatbot interactions.

1.  **Start the FastAPI Server:**
    Ensure your virtual environment is activated, then run:
    ```bash
    uvicorn src.backend.main:app --reload --log-level debug
    ```
    This will start the backend server, typically accessible at `http://127.0.0.1:8000`. The `--reload` flag enables auto-reloading on code changes, and `--log-level debug` provides detailed logs.

2.  **Access API Documentation:**
    Once the backend is running, you can access the interactive API documentation:
    *   **Swagger UI:** Navigate to `http://127.0.0.1:8000/docs` in your web browser.
    *   **ReDoc:** Navigate to `http://127.0.0.1:8000/redoc` in your web browser.
    These interfaces allow you to test the API endpoints directly.

## 3. Running the Frontend (Streamlit)

The Streamlit frontend provides the interactive chatbot user interface.

1.  **Start the Streamlit Application:**
    **Important:** This command should be run in a **separate terminal** from the backend server.
    Ensure your virtual environment is activated, then run:
    ```bash
    streamlit run src/frontend/app.py
    ```
    This will launch the Streamlit application, usually opening in your default web browser at `http://localhost:8501`.

## 4. Using the System via FastAPI UI (Swagger/ReDoc)

You can interact with the backend API directly using the Swagger UI.

1.  **Access Swagger UI:** Open `http://127.0.0.1:8000/docs` in your browser.

2.  **User Registration (`/register`):**
    *   Expand the `/register` endpoint (POST method).
    *   Click "Try it out".
    *   In the "Request body" section, provide a `username`, `email`, and `password`.
    *   Click "Execute".
    *   A successful response will show `200 OK` and a message like `{"message": "User created successfully"}`.

3.  **User Login (`/login`):**
    *   Expand the `/login` endpoint (POST method).
    *   Click "Try it out".
    *   Enter the `username` and `password` you registered with.
    *   Click "Execute".
    *   A successful response will return a `200 OK` with an `access_token` and `token_type`. Copy the `access_token` (the long string after "Bearer ").

4.  **Accessing Protected Route (`/protected`):**
    *   Expand the `/protected` endpoint (GET method).
    *   Click "Try it out".
    *   In the `token` field, paste the `access_token` you obtained from login.
    *   Click "Execute".
    *   A successful response will show `200 OK` and a message like `{"message": "This is a protected route", "user": "your_username"}`.

5.  **Chat Interaction (`/chat`):**
    *   Expand the `/chat` endpoint (POST method).
    *   Click "Try it out".
    *   Click the "Authorize" button (usually a lock icon) and paste your `access_token` in the "Value" field (prefixed with `Bearer ` if not already there, e.g., `Bearer your_access_token`).
    *   In the "Request body" section, provide a `text` message for the chatbot.
    *   Click "Execute".
    *   The response will contain the chatbot's reply in the `response` field.

## 5. Using the System via Streamlit UI

The Streamlit UI provides a user-friendly interface for the chatbot.

1.  **Access the UI:** Open `http://localhost:8501` in your web browser.

2.  **Registration/Login:**
    *   On the initial screen, you will see fields for "Username" and "Password".
    *   To **Register**: Enter a new username and password, then click the "Register" button. You should see a success message.
    *   To **Login**: Enter your registered username and password, then click the "Login" button. Upon successful login, the interface will switch to the chat screen.

3.  **Chat Interaction:**
    *   Once logged in, you will see a chat input field at the bottom.
    *   Type your message into the input field and press Enter or click the send icon.
    *   The conversation history will be displayed above, showing your messages and the chatbot's responses.

4.  **Logout:**
    *   To end your session, click the "Logout" button on the chat screen. This will clear your session and return you to the login screen.
