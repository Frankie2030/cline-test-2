from unittest.mock import Mock, patch
from src.api.gemini import get_chat_response
import pytest

class TestGeminiIntegration:
    @patch('src.api.gemini.genai.GenerativeModel')
    def test_chat_response_generation(self, mock_model):
        """Test Gemini API response generation with mocking. This is to simulate the LLM output in a controlled, predictable way by skipping API calls."""
        # Setup mock
        mock_model.return_value.generate_content.return_value.text = "Mocked response"
        
        # Test
        response = get_chat_response("Test prompt")
        
        # Verify
        assert response == "Mocked response"
        mock_model.return_value.generate_content.assert_called_once_with("Test prompt")
        
    @patch('src.api.gemini.genai.GenerativeModel')
    def test_error_handling(self, mock_model):
        """Test error handling in Gemini API calls"""
        # Setup mock to simulate an exception during generate_content
        mock_model.return_value.generate_content.side_effect = Exception("API Error")
        
        # Test
        response = get_chat_response("Test prompt")
        
        # Verify that the function returns an error string
        assert "Error: API Error" in response
        mock_model.return_value.generate_content.assert_called_once_with("Test prompt")

    @patch('src.api.gemini.genai.GenerativeModel')
    def test_empty_prompt(self, mock_model):
        """Test handling of empty prompt"""
        mock_model.return_value.generate_content.return_value.text = "Empty prompt response"
        response = get_chat_response("")
        assert "Empty prompt response" in response

    @patch('src.api.gemini.genai.GenerativeModel')
    def test_long_prompt(self, mock_model):
        """Test handling of very long prompt"""
        long_prompt = "a" * 10000
        mock_model.return_value.generate_content.return_value.text = "Long prompt response"
        response = get_chat_response(long_prompt)
        assert "Long prompt response" in response

    @patch('src.api.gemini.genai.GenerativeModel')
    def test_special_characters(self, mock_model):
        """Test handling of prompts with special characters"""
        special_prompt = "!@#$%^&*()_+{}|:\"<>?~`"
        mock_model.return_value.generate_content.return_value.text = "Special chars response"
        response = get_chat_response(special_prompt)
        assert "Special chars response" in response

    @patch('src.api.gemini.genai.GenerativeModel')
    @patch('src.api.gemini.os.getenv')
    def test_missing_api_key(self, mock_getenv, mock_model):
        """Test behavior when API key is missing"""
        mock_getenv.return_value = None
        with pytest.raises(ValueError, match="GEMINI_API_KEY environment variable not set"):
            get_chat_response("Test prompt")
