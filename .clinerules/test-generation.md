# Test Generation Rules for Chatbot System

## 1. General Principles

- **Coverage**: Aim for high test coverage for critical parts of the application, especially authentication and game logic. Use coverage reports to identify untested code.

- **Test Pyramid**: Follow the test pyramid principle: have a large base of unit tests, a smaller number of integration tests, and a few end-to-end tests.

- **Isolation**: Tests should be independent and not rely on the state of other tests. Each test should set up its own required state and clean up after itself.

- **Naming Convention**: Use a clear and descriptive naming convention for tests. For example, `test_login_with_valid_credentials_succeeds`.

## 2. Unit Tests

- **Scope**: Unit tests should focus on a single unit of work (e.g., a function or a class method) in isolation. Mock dependencies like databases or external APIs.

- **Authentication**:
  - Test password hashing and verification.
  - Test validation logic for usernames, emails, and passwords (e.g., length, format).
  - Test token generation and validation logic.

- **Chatbot Functionality**:
  - Test the logic for submitting queries to the Gemini API.
  - Test parsing and processing of Gemini API responses.
  - Test conversation history management (adding, retrieving, clearing).
  - Test edge cases for chatbot responses (e.g., empty responses, error responses).

## 3. Integration Tests

- **Scope**: Integration tests should verify the interaction between multiple components. For example, testing the login flow from the API endpoint to the database.

- **Login and Registration**:
  - Test the entire registration flow: API request -> user creation in the database.
  - Test the login flow: API request with credentials -> user retrieval -> token generation.
  - Test endpoints with authentication middleware to ensure they are protected.

- **Chatbot API**:
  - Test submitting a query to the chatbot API and receiving a response.
  - Test the integration with the Gemini API through the backend.
  - Test retrieving conversation history for a session.

## 4. End-to-End (E2E) Tests

- **Scope**: E2E tests should simulate real user scenarios from the user interface to the backend. Use a testing framework like Cypress or Selenium.

- **User Journeys**:
  - **Registration**: A user can navigate to the registration page, fill out the form, submit it, and be logged in.
  - **Login/Logout**: A user can log in with valid credentials, be redirected to the game page, and then log out.
  - **Chatbot Interaction**: A logged-in user can submit a query, receive a response, and see the conversation history updated.

## Example Test Case (Unit Test for Chatbot Functionality)

```python
# (Example in Python using pytest)

def test_process_gemini_response_valid():
    # GIVEN a valid Gemini API response
    response_data = {"candidates": [{"content": {"parts": [{"text": "Hello, how can I help?"}]}}]}
    
    # WHEN the response processing function is called
    processed_text = process_gemini_response(response_data)
    
    # THEN the processed text should match the expected output
    assert processed_text == "Hello, how can I help?"
```
