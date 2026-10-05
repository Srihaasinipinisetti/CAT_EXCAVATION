"""
BLOCK: IMU (pitch/roll/yaw rate) — compass disabled for competition rules.
"""

from dataclasses import dataclass, field
import time
from typing import Dict, Optional


@dataclass
class ImuState:
    pitch_deg: float = 0.0
    roll_deg: float = 0.0
    yaw_rate_dps: float = 0.0
    ax: float = 0.0
    ay: float = 0.0
    az: float = 9.81
    timestamp: float = field(default_factory=time.time)


class ImuBlock:
    def __init__(self):
        self._last: Optional[ImuState] = None

    def update(self, raw: Dict[str, float]) -> ImuState:
        st = ImuState(
            pitch_deg=float(raw.get("pitch", 0)),
            roll_deg=float(raw.get("roll", 0)),
            yaw_rate_dps=float(raw.get("yaw_rate", 0)),
            ax=float(raw.get("ax", 0)),
            ay=float(raw.get("ay", 0)),
            az=float(raw.get("az", 9.81)),
        )
        self._last = st
        return st

    @property
    def last(self) -> Optional[ImuState]:
        return self._last
