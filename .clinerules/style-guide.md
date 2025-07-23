# Style Guide

## Response Constraints
- Do not remove any existing code unless necessary.
- Do not remove my comments or commented-out code unless necessary.
- Do not change the formatting of my imports.
- Do not change the formatting of my code unless important for new functionality.

## Coding Guidelines

### Naming Conventions
- Variable names use camelCase in Python
- Class names use PascalCase
- Constants use UPPER_SNAKE_CASE
- Function names use snake_case
- Module names use snake_case

### Code Style
- Use 2 spaces for indentation
- Maximum 100 characters per line
- Add comments for functions longer than 20 lines
- Follow Python 3.10+ type hinting conventions (see below)

### Function Structure
- Single Responsibility Principle (one function is equivalent to one task)
- Maximum 40 lines per function
- Avoid nesting more than 2 levels of `if` or `for`
- Use descriptive docstrings for public functions

## Python Type Hinting (3.10+)
- Use built-in generics instead of typing imports:
  - Replace `List[T]` with `list[T]`
  - Replace `Dict[K, V]` with `dict[K, V]`
- Use union operator instead of Optional:
  - Replace `Optional[X]` with `X | None`
- Examples:
  ```python
  # Before
  from typing import List, Dict, Optional
  def process(items: List[int]) -> Dict[str, int]: ...
  def get_user(name: Optional[str]) -> None: ...
  
  # After (Python 3.10+)
  def process(items: list[int]) -> dict[str, int]: ...
  def get_user(name: str | None) -> None: ...
  ```

## FastAPI Specific Guidelines
- Use dependency injection for reusable components
- Group related endpoints in separate routers
- Use Pydantic models for request/response validation
- Document endpoints using OpenAPI standards

## Streamlit Specific Guidelines
- Use session_state for maintaining state
- Organize UI components in logical sections
- Use caching (@st.cache_data) for expensive operations
- Keep callback functions small and focused

## Error Handling
- Use specific exception classes
- Provide meaningful error messages
- Log errors with appropriate severity levels
- Return user-friendly error responses in APIs
