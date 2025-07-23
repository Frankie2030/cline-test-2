# Testing Guide

## Test Structure

```
tests/
├── unit/               # Unit tests for individual components
│   ├── test_password.py
│   ├── test_jwt.py
│   ├── test_database.py
│   └── test_gemini.py
└── integration/        # End-to-end flow tests
    ├── test_auth_flow.py
    └── test_chat_flow.py
```

## Running Tests

1. Install test dependencies:
```bash
pip install -r requirements.txt
```

2. Run all tests:
```bash
pytest
```

3. Run specific test category:
```bash
pytest tests/unit/       # Run only unit tests
pytest tests/integration # Run only integration tests
```

4. Generate coverage report:
```bash
pytest --cov=src --cov-report=html
```

## Test Types

### Unit Tests
- Test individual components in isolation
- Mock external dependencies
- Fast execution
- Located in `tests/unit/`

### Integration Tests
- Test complete system flows
- Verify component interactions
- May use test database
- Located in `tests/integration/`

## Writing New Tests

Follow these patterns:
- Test files should start with `test_`
- Test classes should start with `Test`
- Test methods should start with `test_`
- Use descriptive docstrings
- Keep tests focused on one scenario
