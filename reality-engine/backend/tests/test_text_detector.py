"""Unit tests for text_detector module."""

import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest


class TestTextDetector:
    """Test suite for TextDetector class."""

    @patch("text_detector.pipeline")
    def test_initialization(self, mock_pipeline):
        """Test that TextDetector can be initialized."""
        from text_detector import TextDetector
        detector = TextDetector()
        assert detector is not None
        assert hasattr(detector, '_pipe')
        mock_pipeline.assert_called_once()

    @patch("text_detector.pipeline")
    def test_initialization_with_custom_model(self, mock_pipeline):
        """Test initialization with a custom model name."""
        from text_detector import TextDetector
        model_name = "my-custom-text-model"
        detector = TextDetector(model_name=model_name)
        mock_pipeline.assert_called_once_with("text-classification", model=model_name)

    @patch("text_detector.pipeline")
    def test_analyze_returns_dict(self, mock_pipeline):
        """Test that analyze method returns a dictionary with 'raw' key."""
        from text_detector import TextDetector
        mock_pipe_instance = MagicMock()
        mock_pipe_instance.return_value = [
            {"label": "REAL", "score": 0.91},
            {"label": "FAKE", "score": 0.09}
        ]
        mock_pipeline.return_value = mock_pipe_instance

        detector = TextDetector()
        result = detector.analyze("This is a test sentence.")

        assert isinstance(result, dict)
        assert "raw" in result
        mock_pipe_instance.assert_called_once_with("This is a test sentence.")

    @patch("text_detector.pipeline")
    def test_analyze_method_signature(self, mock_pipeline):
        """Test that analyze method has correct signature."""
        from text_detector import TextDetector
        import inspect
        detector = TextDetector()
        sig = inspect.signature(detector.analyze)
        assert 'text' in sig.parameters
