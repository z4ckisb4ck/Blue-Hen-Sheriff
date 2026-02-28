"""Unit tests for scoring_engine module."""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from scoring_engine import ScoringEngine


class TestScoringEngine:
    """Test suite for ScoringEngine class."""

    def test_initialization(self):
        """Test that ScoringEngine can be initialized."""
        engine = ScoringEngine()
        assert engine is not None
        assert hasattr(engine, 'weights')

    def test_calculate_score_method_exists(self):
        """Test that calculate_score method exists."""
        engine = ScoringEngine()
        assert hasattr(engine, 'calculate_score')
        assert callable(engine.calculate_score)

    def test_calculate_score_with_empty_detections(self):
        """Test scoring with empty detection results."""
        engine = ScoringEngine()
        result = engine.calculate_score({})
        assert isinstance(result, dict)
        assert 'authenticity' in result
        assert result['authenticity'] == 0.0

    def test_calculate_score_with_single_detection(self):
        """Test scoring with a single detector result."""
        engine = ScoringEngine()
        detections = {
            "text": {
                "raw": [
                    {"label": "REAL", "score": 0.85},
                    {"label": "FAKE", "score": 0.15}
                ]
            }
        }
        result = engine.calculate_score(detections)
        assert isinstance(result, dict)
        assert 'authenticity' in result
        assert 0.0 <= result['authenticity'] <= 1.0
        assert result['authenticity'] == 0.85

    def test_calculate_score_with_multiple_detections(self):
        """Test scoring with multiple detector results."""
        engine = ScoringEngine()
        detections = {
            "text": {
                "raw": [{"label": "REAL", "score": 0.8}]
            },
            "audio": {
                "raw": [{"label": "REAL", "score": 0.6}]
            }
        }
        result = engine.calculate_score(detections)
        assert isinstance(result, dict)
        assert 'authenticity' in result
        # Average of 0.8 and 0.6 should be 0.7
        assert result['authenticity'] == 0.7

    def test_calculate_score_returns_details(self):
        """Test that calculate_score includes details in output."""
        engine = ScoringEngine()
        detections = {"text": {"raw": [{"label": "REAL", "score": 0.9}]}}
        result = engine.calculate_score(detections)
        assert 'details' in result
        assert result['details'] == detections
