# Backend-Specific Guidelines for Chatbot System

- Structure FastAPI apps with separate routers for different resources (e.g., /auth, /chat).
- Use PyJWT for secure JWT-based authentication; validate tokens in middleware.
- Use bcrypt for secure password hashing; follow best practices for salt rounds.
- Use FastAPI's WebSocket support for real-time communication; define clear message protocols with Pydantic models.
- Use SQLAlchemy with SQLite for database interactions; prefer parameterized queries for security.
- Organize database schemas and migrations in dedicated files (e.g., db/migrations/).
- Integrate Gemini API with proper error handling and rate limiting.
- Implement session management using secure cookies or JWT tokens.
