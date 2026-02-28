"""Unit tests for video_detector module."""

import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest


class TestVideoDetector:
    """Test suite for VideoDetector class."""

    @patch("video_detector.pipeline")
    def test_initialization(self, mock_pipeline):
        """Test that VideoDetector can be initialized."""
        from video_detector import VideoDetector
        detector = VideoDetector()
        assert detector is not None
        assert hasattr(detector, '_pipe')
        mock_pipeline.assert_called_once()

    @patch("video_detector.pipeline")
    def test_initialization_with_custom_model(self, mock_pipeline):
        """Test initialization with a custom model name."""
        from video_detector import VideoDetector
        model_name = "my-custom-video-model"
        detector = VideoDetector(model_name=model_name)
        mock_pipeline.assert_called_once_with("video-classification", model=model_name)

    @patch("video_detector.pipeline")
    def test_analyze_returns_dict(self, mock_pipeline):
        """Test that analyze method returns a dictionary with 'raw' key."""
        from video_detector import VideoDetector
        mock_pipe_instance = MagicMock()
        mock_pipe_instance.return_value = [{"label": "REAL", "score": 0.95}]
        mock_pipeline.return_value = mock_pipe_instance

        detector = VideoDetector()
        result = detector.analyze("test_video.mp4")

        assert isinstance(result, dict)
        assert "raw" in result
        mock_pipe_instance.assert_called_once_with("test_video.mp4")

    @patch("video_detector.pipeline")
    def test_analyze_method_signature(self, mock_pipeline):
        """Test that analyze method accepts a video_path parameter."""
        from video_detector import VideoDetector
        import inspect
        detector = VideoDetector()
        sig = inspect.signature(detector.analyze)
        assert 'video_path' in sig.parameters
        sig = inspect.signature(detector.analyze)
        assert 'video_path' in sig.parameters
