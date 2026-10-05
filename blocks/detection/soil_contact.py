"""
BLOCK: Soil contact detection (current + velocity drop).
"""

from dataclasses import dataclass
from enum import Enum
import time

from excavation_control.config import thresholds as th
from excavation_control.blocks.sensors.sensor_fusion import RobotSnapshot


class ContactType(str, Enum):
    NONE = "NONE"
    SOIL = "SOIL"
    OBSTACLE = "OBSTACLE"
    MECH_LIMIT = "MECH_LIMIT"


@dataclass
class ContactResult:
    contact: ContactType
    confidence: float


class SoilContactBlock:
    def __init__(self):
        self._i_boom_idle = 0.4
        self._t0: float | None = None

    def update(
        self,
        snap: RobotSnapshot,
        boom_cmd_v_mm_s: float,
        at_soft_limit: bool,
    ) -> ContactResult:
        if at_soft_limit and snap.current.i_boom_a > th.I_LA_WARN_A:
            return ContactResult(ContactType.MECH_LIMIT, 0.9)

        v_act = abs(snap.actuators.boom_cmd_vel_mm_s)
        v_ratio = v_act / max(abs(boom_cmd_v_mm_s), 1e-3)
        di = snap.current.i_boom_a - self._i_boom_idle

        if boom_cmd_v_mm_s < -1.0 and v_ratio < th.V_BOOM_CONTACT_FRAC and di > th.I_BOOM_CONTACT_DELTA_A:
            now = time.time()
            self._t0 = self._t0 or now
            if now - self._t0 > th.CONTACT_CONFIRM_TIME_S:
                if di > th.I_PEN_HIGH_A * 1.2:
                    return ContactResult(ContactType.OBSTACLE, 0.75)
                return ContactResult(ContactType.SOIL, 0.85)
        else:
            self._t0 = None

        return ContactResult(ContactType.NONE, 0.0)
