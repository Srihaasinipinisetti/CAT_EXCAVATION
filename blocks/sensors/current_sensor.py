"""
BLOCK: Current sensing (wheel motors, boom LA, clamshell LA, pack).
Arduino reads shunts / INA219; Pi receives via telemetry.
"""

from dataclasses import dataclass, field
from typing import Dict, Optional
import time


@dataclass
class CurrentReadings:
    i_boom_a: float = 0.0
    i_clam_a: float = 0.0
    i_bat_a: float = 0.0
    i_wheel_fl_a: float = 0.0
    i_wheel_fr_a: float = 0.0
    i_wheel_rl_a: float = 0.0
    i_wheel_rr_a: float = 0.0
    timestamp: float = field(default_factory=time.time)

    @property
    def i_wheel_sum_a(self) -> float:
        return self.i_wheel_fl_a + self.i_wheel_fr_a + self.i_wheel_rl_a + self.i_wheel_rr_a

    @property
    def i_wheel_mean_a(self) -> float:
        return self.i_wheel_sum_a / 4.0

    def as_dict(self) -> Dict[str, float]:
        return {
            "i_boom_a": self.i_boom_a,
            "i_clam_a": self.i_clam_a,
            "i_bat_a": self.i_bat_a,
            "i_wheel_fl_a": self.i_wheel_fl_a,
            "i_wheel_fr_a": self.i_wheel_fr_a,
            "i_wheel_rl_a": self.i_wheel_rl_a,
            "i_wheel_rr_a": self.i_wheel_rr_a,
        }


class CurrentSensorBlock:
    """Parse and validate current telemetry."""

    def __init__(self, max_sane_a: float = 50.0):
        self.max_sane_a = max_sane_a
        self._last: Optional[CurrentReadings] = None
        self._fault = False

    def update_from_telemetry(self, raw: Dict[str, float]) -> CurrentReadings:
        reading = CurrentReadings(
            i_boom_a=float(raw.get("i_boom_a", 0)),
            i_clam_a=float(raw.get("i_clam_a", 0)),
            i_bat_a=float(raw.get("i_bat_a", 0)),
            i_wheel_fl_a=float(raw.get("i_wheel_fl_a", 0)),
            i_wheel_fr_a=float(raw.get("i_wheel_fr_a", 0)),
            i_wheel_rl_a=float(raw.get("i_wheel_rl_a", 0)),
            i_wheel_rr_a=float(raw.get("i_wheel_rr_a", 0)),
        )
        if not self._validate(reading):
            self._fault = True
        else:
            self._fault = False
        self._last = reading
        return reading

    def _validate(self, r: CurrentReadings) -> bool:
        for name, val in r.as_dict().items():
            if val < -0.5 or val > self.max_sane_a:
                return False
        return True

    @property
    def last(self) -> Optional[CurrentReadings]:
        return self._last

    @property
    def fault(self) -> bool:
        return self._fault

    def simulate_sample(self, phase: str = "idle") -> CurrentReadings:
        """Sample currents for SIMULATION_MODE."""
        base = CurrentReadings()
        if phase == "penetration":
            base.i_boom_a = 1.05
            base.i_wheel_fl_a = 0.8
            base.i_wheel_fr_a = 0.8
        elif phase == "scoop":
            base.i_clam_a = 1.15
        elif phase == "lift":
            base.i_boom_a = 1.25
        elif phase == "drive":
            base.i_wheel_fl_a = 2.0
            base.i_wheel_fr_a = 2.0
            base.i_wheel_rl_a = 2.0
            base.i_wheel_rr_a = 2.0
        base.i_bat_a = base.i_boom_a + base.i_clam_a + base.i_wheel_sum_a * 0.25
        self._last = base
        return base
