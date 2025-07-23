import pytest
from fastapi.testclient import TestClient
from src.backend.main import app
from src.database.models import User
from src.utils.password import hash_password
import uuid

client = TestClient(app)

@pytest.fixture
def test_user(test_db):
    """Create a test user for auth flow tests"""
    hashed_password = hash_password("testpass")
    user = User(
        username="testuser",
        email="test@example.com", 
        hashed_password=hashed_password
    )
    test_db.add(user)
    test_db.commit()
    return user

class TestAuthFlow:
    def test_register_login_protected_route(self, test_db, test_user):
        """Test complete auth flow: register -> login -> protected route"""
        # Register (though user already exists in this test)
        unique_id = str(uuid.uuid4())[:8]
        register_data = {
            "username": f"testuser_{unique_id}",
            "email": f"test_{unique_id}@example.com",
            "password": f"testPass_{unique_id}"
        }
        response = client.post("/register", json=register_data)
        assert response.status_code == 200
        assert response.json() == {"message": "User created successfully"}

        # Login with newly registered user
        login_data = {
            "username": register_data["username"],
            "password": register_data["password"]
        }
        response = client.post("/login", data=login_data)
        assert response.status_code == 200
        token = response.json()["access_token"]

        # Access protected route
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/protected", headers=headers)
        assert response.status_code == 200

    def test_duplicate_name_registration(self, test_db, test_user):
        """Test registration with duplicate username"""
        # Duplicate username
        response = client.post("/register", json={
            "username": "testuser",  # duplicate
            "email": "new@example.com",
            "password": "testpass"
        })
        assert response.status_code == 400
        assert "Username already registered" in response.json()["detail"]

    def test_duplicate_email_registration(self, test_db, test_user):
        # Duplicate email
        response = client.post("/register", json={
            "username": "newuser",
            "email": "test@example.com",  # duplicate
            "password": "testpass"
        })
        assert response.status_code == 400
        assert "Email already registered" in response.json()["detail"]

    def test_invalid_login(self, test_db, test_user):
        """Test login with invalid credentials"""
        # Wrong password
        response = client.post("/login", data={
            "username": "testuser",
            "password": "wrongpass"
        })
        assert response.status_code == 401
        assert "Incorrect username or password" in response.json()["detail"]

        # Non-existent user
        response = client.post("/login", data={
            "username": "nonexistent",
            "password": "testpass"
        })
        assert response.status_code == 401
        assert "Incorrect username or password" in response.json()["detail"]

    def test_protected_route_without_token(self):
        """Test accessing protected route without token"""
        response = client.get("/protected")
        assert response.status_code == 401
        assert "Not authenticated" in response.json()["detail"]

    def test_protected_route_with_invalid_token(self):
        """Test accessing protected route with invalid token"""
        headers = {"Authorization": "Bearer invalid.token.here"}
        response = client.get("/protected", headers=headers)
        assert response.status_code == 401
        assert "Not authenticated" in response.json()["detail"]

    @pytest.mark.parametrize("invalid_data", [
        {"username": "", "email": "test@example.com", "password": "testpass"},  # empty username
        {"username": "testuser", "email": "", "password": "testpass"},  # empty email
        {"username": "testuser", "email": "test@example.com", "password": ""},  # empty password
        {"username": "a"*256, "email": "test@example.com", "password": "testpass"},  # too long username
        {"username": "testuser", "email": "a"*256, "password": "testpass"},  # too long email
    ])
    def test_invalid_registration_data(self, invalid_data):
        """Test registration with various invalid data"""
        response = client.post("/register", json=invalid_data)
        assert response.status_code == 422  # Unprocessable Entity
