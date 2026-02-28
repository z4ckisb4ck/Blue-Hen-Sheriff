"""Scoring engine module.

Combines detection results into a unified authenticity score.
"""

from typing import Any, Dict, List


class ScoringEngine:
    """Aggregates detection results and produces final authenticity scores."""

    def __init__(self):
        """Initialize scoring engine."""
        # in a real project this might load configuration or calibration data
        self.weights: Dict[str, float] = {}

    def calculate_score(self, detections: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate final authenticity score from multiple detectors.

        ``detections`` is expected to be a mapping of modality names to the
        raw output produced by each detector's ``analyze`` method.  This
        simple implementation averages the top‑score from each detector and
        returns a single ``{'authenticity': float}`` value between 0 (definitely
        fake) and 1 (definitely real).
        """
        scores: List[float] = []
        for name, output in detections.items():
            # extract the highest confidence score if possible
            if isinstance(output, dict) and "raw" in output:
                preds = output["raw"]
            else:
                preds = output
            if isinstance(preds, list) and preds:
                best = max(p.get("score", 0.0) for p in preds if isinstance(p, dict))
                scores.append(best)
        if scores:
            avg = sum(scores) / len(scores)
        else:
            avg = 0.0
        return {"authenticity": avg, "details": detections}
