"""
BLOCK: Adaptive penetration (boom down into sand).
"""

from dataclasses import dataclass
from enum import Enum

from excavation_control.config import hardware as hw
from excavation_control.config import thresholds as th


class ResistanceClass(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass
class PenetrationCommand:
    boom_vel_mm_s: float
    resistance: ResistanceClass
    depth_mm: float
    stop: bool = False
    retract_mm: float = 0.0


class PenetrationControlBlock:
    def __init__(self):
        self.depth_mm = 0.0
        self._contact_boom_mm = 0.0
        self._contact_set = False

    def latch_contact(self, boom_length_mm: float):
        self._contact_boom_mm = boom_length_mm
        self._contact_set = True
        self.depth_mm = 0.0

    def update(self, boom_length_mm: float, i_boom_a: float) -> PenetrationCommand:
        if self._contact_set:
            stroke_from_contact = self._contact_boom_mm - boom_length_mm
            self.depth_mm = max(0.0, stroke_from_contact / hw.K_DEPTH_MM_STROKE_PER_MM_DEPTH)

        res = self._classify_resistance(i_boom_a)
        if res == ResistanceClass.CRITICAL:
            return PenetrationCommand(
                0.0, res, self.depth_mm, stop=True, retract_mm=th.PEN_RETRACT_MM
            )

        v_nom = 6.0  # mm/s SAMPLE boom extend rate (into ground = shorten LA or lengthen depending on mount)
        if res == ResistanceClass.LOW:
            v = v_nom
        elif res == ResistanceClass.MEDIUM:
            v = v_nom * 0.5
        else:
            v = v_nom * 0.2

        stop = self.depth_mm >= hw.PENETRATION_DEPTH_TARGET_MM
        return PenetrationCommand(-v, res, self.depth_mm, stop=stop)

    def _classify_resistance(self, i_a: float) -> ResistanceClass:
        if i_a >= th.I_PEN_HIGH_A:
            return ResistanceClass.CRITICAL
        if i_a >= th.I_PEN_MED_A:
            return ResistanceClass.HIGH
        if i_a >= th.I_PEN_LOW_A:
            return ResistanceClass.MEDIUM
        return ResistanceClass.LOW

    def reset(self):
        self.depth_mm = 0.0
        self._contact_set = False
