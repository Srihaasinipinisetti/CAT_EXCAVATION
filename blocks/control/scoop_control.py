"""
BLOCK: Clamshell scoop / close after penetration.
"""

from dataclasses import dataclass

from excavation_control.blocks.actuators.clamshell_actuator import ClamshellActuatorBlock
from excavation_control.config import thresholds as th


@dataclass
class ScoopCommand:
    target_clam_mm: float
    vel_mm_s: float
    complete: bool


class ScoopControlBlock:
    def __init__(self):
        self.clam = ClamshellActuatorBlock()

    def update(self, clam_stroke_mm: float, i_clam_a: float, depth_mm: float) -> ScoopCommand:
        if depth_mm < 5.0:
            return ScoopCommand(self.clam.OPEN_MM, 0.0, False)

        target = self.clam.CLOSED_MM
        vel = 5.0
        if i_clam_a > th.I_LA_WARN_A:
            vel = 2.0
        if i_clam_a > th.I_LA_CRIT_A:
            vel = 0.0

        complete = clam_stroke_mm <= (self.clam.CLOSED_MM + 3.0) or i_clam_a > 1.0 and vel == 0.0
        return ScoopCommand(target, vel, complete)
