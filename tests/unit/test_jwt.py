from src.utils.jwt import create_access_token, verify_token
from src.database.models import User
import pytest
from jose import jwt
from datetime import timedelta

class TestJWTUtils:
    def test_token_creation_and_verification(self):
        """Test JWT token creation and verification"""
        test_user = User(id=1, username="testuser", email="test@example.com")
        token = create_access_token(data={"sub": test_user.username, "email": test_user.email})
        
        # Verify valid token
        payload = verify_token(token)
        assert payload is not None
        assert payload["sub"] == "testuser"
        assert payload["email"] == "test@example.com"
        
    def test_expired_token(self, monkeypatch):
        """Test that expired tokens are rejected"""
        # Patch expiration to be negative
        monkeypatch.setattr("src.utils.jwt.ACCESS_TOKEN_EXPIRE_MINUTES", -1)
        
        test_user = User(id=1, username="testuser", email="test@example.com")
        token = create_access_token(data={"sub": test_user.username, "email": test_user.email})
        
        # Verify expired token
        payload = verify_token(token)
        assert payload is None

    def test_invalid_signature(self):
        """Test token with invalid signature"""
        test_user = User(id=1, username="testuser", email="test@example.com")
        token = create_access_token(data={"sub": test_user.username})
        
        # Tamper with the token
        parts = token.split('.')
        parts[2] = 'tampered_signature'
        tampered_token = '.'.join(parts)
        
        payload = verify_token(tampered_token)
        assert payload is None

    def test_malformed_token(self):
        """Test malformed/incomplete tokens"""
        assert verify_token("invalid.token.format") is None
        assert verify_token("missing.parts") is None
        assert verify_token("") is None

    def test_missing_claims(self):
        """Test tokens with missing required claims"""
        # Create token without 'sub' claim
        token = jwt.encode({"exp": 9999999999}, "wrong-secret", algorithm="HS256")
        assert verify_token(token) is None

    @pytest.mark.parametrize("expires_delta", [
        None,
        timedelta(minutes=5),
        timedelta(hours=1),
        timedelta(days=7)
    ])
    def test_token_with_various_expirations(self, expires_delta):
        """Test token creation with different expiration times"""
        token = create_access_token(
            data={"sub": "testuser"},
            expires_delta=expires_delta
        )
        assert verify_token(token) is not None
