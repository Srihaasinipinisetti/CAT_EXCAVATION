"""
BLOCK: Bucket load estimation (current-based lift test).
"""

from enum import Enum
from dataclasses import dataclass

from excavation_control.config import thresholds as th
from excavation_control.blocks.sensors.sensor_fusion import RobotSnapshot


class LoadClass(str, Enum):
    PRESENT = "LOAD_PRESENT"
    PARTIAL = "LOAD_PARTIAL"
    EMPTY = "LOAD_EMPTY"
    UNCERTAIN = "LOAD_UNCERTAIN"


@dataclass
class LoadEstimate:
    load_class: LoadClass
    delta_i_a: float
    confidence: float


class LoadSensingBlock:
    """
    Method 1: compare boom current during standardized lift vs empty baseline.
    Calibrate empty_baseline_a on robot (sample value below).
    """

    def __init__(self):
        self.empty_baseline_a = 0.55  # SAMPLE — calibrate with 20 empty lifts
        self._lift_i_samples: list = []

    def reset_lift_samples(self):
        self._lift_i_samples = []

    def sample_during_lift(self, snap: RobotSnapshot):
        self._lift_i_samples.append(snap.current.i_boom_a)

    def classify_after_lift(self) -> LoadEstimate:
        if len(self._lift_i_samples) < 3:
            return LoadEstimate(LoadClass.UNCERTAIN, 0.0, 0.0)
        i_mean = sum(self._lift_i_samples) / len(self._lift_i_samples)
        delta_i = i_mean - self.empty_baseline_a

        if delta_i >= th.DI_LIFT_FULL_MIN_A:
            lc = LoadClass.PRESENT
            conf = 0.85
        elif delta_i >= th.DI_LIFT_PARTIAL_MIN_A:
            lc = LoadClass.PARTIAL
            conf = 0.7
        else:
            lc = LoadClass.EMPTY
            conf = 0.75

        return LoadEstimate(lc, delta_i, conf)

    def detect_load_loss(self, i_before: float, i_after: float) -> bool:
        return (i_before - i_after) > 0.25  # SAMPLE hysteresis
