import pytest
from src.utils.password import hash_password, verify_password

class TestPasswordUtils:
    def test_hash_password_returns_string(self):
        """Test that hash_password returns a string"""
        hashed = hash_password("testpassword")
        assert isinstance(hashed, str)

    def test_verify_password_correct(self):
        """Test password verification with correct password"""
        password = "correct_password"
        hashed = hash_password(password)
        assert verify_password(password, hashed) is True

    def test_verify_password_incorrect(self):
        """Test password verification with incorrect password"""
        hashed = hash_password("original_password")
        assert verify_password("wrong_password", hashed) is False

    def test_verify_password_corrupted_hash(self):
        """Test verification with corrupted hash string"""
        with pytest.raises(ValueError):
            verify_password("test", "invalid_hash_format")

    @pytest.mark.parametrize("password", [
        "",  # empty password
        "a" * 1000,  # very long password
        "p@ssw0rd!$%^&*()",  # special characters
        "密碼",  # unicode characters
    ])
    def test_password_edge_cases(self, password):
        """Test various edge cases for password handling"""
        hashed = hash_password(password)
        assert verify_password(password, hashed) is True
