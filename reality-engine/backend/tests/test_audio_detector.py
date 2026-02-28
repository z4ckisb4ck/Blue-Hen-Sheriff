"""Unit tests for audio_detector module."""

import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest


class TestAudioDetector:
    """Test suite for AudioDetector class."""

    @patch("audio_detector.pipeline")
    def test_initialization(self, mock_pipeline):
        """Test that AudioDetector can be initialized."""
        from audio_detector import AudioDetector
        detector = AudioDetector()
        assert detector is not None
        assert hasattr(detector, '_pipe')
        mock_pipeline.assert_called_once()

    @patch("audio_detector.pipeline")
    def test_initialization_with_custom_model(self, mock_pipeline):
        """Test initialization with a custom model name."""
        from audio_detector import AudioDetector
        model_name = "my-custom-audio-model"
        detector = AudioDetector(model_name=model_name)
        mock_pipeline.assert_called_once_with("audio-classification", model=model_name)

    @patch("audio_detector.pipeline")
    def test_analyze_returns_dict(self, mock_pipeline):
        """Test that analyze method returns a dictionary with 'raw' key."""
        from audio_detector import AudioDetector
        mock_pipe_instance = MagicMock()
        mock_pipe_instance.return_value = [{"label": "REAL", "score": 0.9}]
        mock_pipeline.return_value = mock_pipe_instance

        detector = AudioDetector()
        result = detector.analyze("test_audio.wav")

        assert isinstance(result, dict)
        assert "raw" in result
        mock_pipe_instance.assert_called_once_with("test_audio.wav")

    @patch("audio_detector.pipeline")
    def test_analyze_method_signature(self, mock_pipeline):
        """Test that analyze method accepts an audio_path parameter."""
        from audio_detector import AudioDetector
        import inspect
        detector = AudioDetector()
        sig = inspect.signature(detector.analyze)
        assert 'audio_path' in sig.parameters
