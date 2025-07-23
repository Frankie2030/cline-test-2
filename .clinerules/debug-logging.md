# Debug Logging Rules for Chatbot System

## 1. General Principles

- **Log Levels**: Use standard log levels (e.g., `DEBUG`, `INFO`, `WARN`, `ERROR`).
  - `DEBUG`: Detailed information for development and troubleshooting (e.g., function calls, variable states, message processing).
  - `INFO`: High-level events that mark the progress of the application (e.g., user login, chatbot query received, response sent).
  - `WARN`: Potentially harmful situations that do not prevent the application from running (e.g., failed login attempt, invalid chatbot query).
  - `ERROR`: Errors that cause a part of the application to fail (e.g., database connection failure, unhandled exceptions, Gemini API errors).

- **No Sensitive Information**: NEVER log sensitive user information like passwords, session tokens, or personal identifiable information (PII). Log user IDs or usernames instead of emails where possible.

- **Structured Logging**: Use a structured logging format like JSON. This makes logs easier to parse, search, and analyze. Each log entry should include a timestamp, log level, message, and relevant context.

## 2. Login and Authentication

- **Log Login Attempts**: Log all login attempts with the username and IP address.
  - **Success**: `INFO` level. Message: `User '{username}' logged in successfully from IP {ip_address}.`
  - **Failure**: `WARN` level. Message: `Failed login attempt for user '{username}' from IP {ip_address}. Reason: {reason}.` (Reasons: "Invalid credentials", "User not found", "Account locked").

- **Log Registration**: Log new user registrations.
  - `INFO` level. Message: `New user registered: '{username}'.`

- **Log Logout**: Log user logout events.
  - `INFO` level. Message: `User '{username}' logged out.`

## 3. Chatbot Functionality

- **Log Query Submission**: Log when a user submits a query to the chatbot.
  - `INFO` level. Message: `User '{username}' submitted query: '{query}'. SessionID: {session_id}.`

- **Log Gemini API Interaction**: Log requests and responses from the Gemini API.
  - `DEBUG` level. Message: `Gemini API request for session {session_id}. Prompt: '{prompt}'.`
  - `INFO` level. Message: `Gemini API response received for session {session_id}. Response length: {length}.`

- **Log Conversation History Updates**: Log when conversation history is updated.
  - `DEBUG` level. Message: `Conversation history updated for session {session_id}. New entry: User: '{user_message}', Bot: '{bot_response}'.`

## 4. Error and Exception Logging

- **Log Unhandled Exceptions**: Catch and log all unhandled exceptions with a full stack trace.
  - `ERROR` level. Message: `Unhandled exception occurred.` Include the exception details and stack trace in the log context.

- **Log API Errors**: Log errors related to external API calls if any.
  - `ERROR` level. Message: `API call to {api_name} failed. Status: {status_code}, Response: {response_body}.`

## Example Log Entry (JSON)

```json
{
  "timestamp": "2025-07-17T11:30:00Z",
  "level": "WARN",
  "message": "Failed login attempt for user 'player_one' from IP 192.168.1.10. Reason: Invalid credentials.",
  "context": {
    "username": "player_one",
    "ip_address": "192.168.1.10",
    "reason": "Invalid credentials"
  }
}
