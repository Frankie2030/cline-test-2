from fastapi.testclient import TestClient
from src.backend.main import app
from unittest.mock import patch
import pytest

client = TestClient(app)

class TestChatFlow:
    @patch('src.backend.main.get_chat_response')
    def test_chat_interaction(self, mock_generate):
        """Test complete chat flow from frontend to backend"""
        # Setup mock
        mock_generate.return_value = "Mocked AI response"
        
        # Login (using test user from auth flow)
        login_data = {"username": "testuser", "password": "testpass"}
        login_response = client.post("/login", data=login_data)
        token = login_response.json()["access_token"]
        
        # Send chat message
        headers = {"Authorization": f"Bearer {token}"}
        chat_data = {"text": "Hello AI"}
        response = client.post("/chat", json=chat_data, headers=headers)
        
        # Verify response
        assert response.status_code == 200
        assert response.json() == {"response": "Mocked AI response"}
        mock_generate.assert_called_once_with("Hello AI")

    @patch('src.backend.main.get_chat_response')
    def test_empty_message(self, mock_generate):
        """Test sending empty message"""
        mock_generate.return_value = "Empty message response"
        
        login_data = {"username": "testuser", "password": "testpass"}
        login_response = client.post("/login", data=login_data)
        token = login_response.json()["access_token"]
        
        headers = {"Authorization": f"Bearer {token}"}
        response = client.post("/chat", json={"text": ""}, headers=headers)
        assert response.status_code == 200
        assert "Empty message response" in response.json()["response"]

    @patch('src.backend.main.get_chat_response')
    def test_long_message(self, mock_generate):
        """Test sending very long message"""
        long_message = "a" * 10000
        mock_generate.return_value = "Long message response"
        
        login_data = {"username": "testuser", "password": "testpass"}
        login_response = client.post("/login", data=login_data)
        token = login_response.json()["access_token"]
        
        headers = {"Authorization": f"Bearer {token}"}
        response = client.post("/chat", json={"text": long_message}, headers=headers)
        assert response.status_code == 200
        assert "Long message response" in response.json()["response"]

    @patch('src.backend.main.get_chat_response')
    def test_special_characters(self, mock_generate):
        """Test message with special characters"""
        special_message = "!@#$%^&*()_+{}|:\"<>?~`"
        mock_generate.return_value = "Special chars response"
        
        login_data = {"username": "testuser", "password": "testpass"}
        login_response = client.post("/login", data=login_data)
        token = login_response.json()["access_token"]
        
        headers = {"Authorization": f"Bearer {token}"}
        response = client.post("/chat", json={"text": special_message}, headers=headers)
        assert response.status_code == 200
        assert "Special chars response" in response.json()["response"]

    def test_chat_without_token(self):
        """Test accessing chat endpoint without token"""
        response = client.post("/chat", json={"text": "Hello"})
        assert response.status_code == 401
        assert "Not authenticated" in response.json()["detail"]

    def test_chat_with_invalid_token(self):
        """Test accessing chat endpoint with invalid token"""
        headers = {"Authorization": "Bearer invalid.token.here"}
        response = client.post("/chat", json={"text": "Hello"}, headers=headers)
        assert response.status_code == 401
        assert "Not authenticated" in response.json()["detail"]

    @patch('src.backend.main.get_chat_response')
    def test_multiple_messages(self, mock_generate):
        """Test sending multiple messages in sequence"""
        mock_generate.side_effect = ["Response 1", "Response 2", "Response 3"]
        
        login_data = {"username": "testuser", "password": "testpass"}
        login_response = client.post("/login", data=login_data)
        token = login_response.json()["access_token"]
        
        headers = {"Authorization": f"Bearer {token}"}
        
        # First message
        response1 = client.post("/chat", json={"text": "Message 1"}, headers=headers)
        assert response1.status_code == 200
        assert response1.json() == {"response": "Response 1"}
        
        # Second message
        response2 = client.post("/chat", json={"text": "Message 2"}, headers=headers)
        assert response2.status_code == 200
        assert response2.json() == {"response": "Response 2"}
        
        # Third message
        response3 = client.post("/chat", json={"text": "Message 3"}, headers=headers)
        assert response3.status_code == 200
        assert response3.json() == {"response": "Response 3"}
        
        assert mock_generate.call_count == 3
