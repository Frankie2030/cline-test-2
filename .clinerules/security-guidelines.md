# Security Guidelines

## Authentication
- Use bcrypt for password hashing with appropriate salt rounds
- Implement JWT token expiration and refresh mechanisms
- Validate all user inputs on both client and server sides

## Data Protection
- Never store plaintext passwords
- Encrypt sensitive data at rest
- Implement proper session management

## API Security
- Use HTTPS for all communications
- Implement rate limiting to prevent brute force attacks
- Validate and sanitize all API inputs
- Use parameterized queries to prevent SQL injection

## Best Practices
- Regularly update dependencies
- Implement proper error handling without exposing sensitive info
- Follow principle of least privilege for all permissions
