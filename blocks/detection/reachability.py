"""
BLOCK: DIG_ZONE_REACHABILITY_CHECK (sample FK table / geometry).
"""

from dataclasses import dataclass

from excavation_control.config import hardware as hw
from excavation_control.config import thresholds as th


@dataclass
class DigTarget:
    x_mm: float = 600.0  # forward from robot base — SAMPLE
    z_mm: float = 0.0  # sand surface relative to base


@dataclass
class ReachabilityResult:
    reachable: bool
    min_distance_mm: float
    suggested_boom_mm: float
    reason: str = ""


class ReachabilityBlock:
    """
    Sample model: tip forward reach scales with boom LA length linearly between
    250.8 mm and 616 mm chord hints from sketch. Replace with CAD lookup table.
    """

    REACH_MIN_MM = 250.8
    REACH_MAX_MM = 616.0

    def tip_forward_mm(self, boom_length_mm: float) -> float:
        u = (boom_length_mm - hw.BOOM_LA_LENGTH_CLOSED_MM) / hw.BOOM_LA_STROKE_MM
        u = max(0.0, min(1.0, u))
        return self.REACH_MIN_MM + u * (self.REACH_MAX_MM - self.REACH_MIN_MM)

    def check(self, target: DigTarget, rover_x_mm: float = 0.0) -> ReachabilityResult:
        best_d = 1e9
        best_L = hw.BOOM_LA_SOFT_MIN_MM
        for L in range(int(hw.BOOM_LA_SOFT_MIN_MM), int(hw.BOOM_LA_SOFT_MAX_MM) + 1, 5):
            tip = rover_x_mm + self.tip_forward_mm(float(L))
            d = abs(tip - target.x_mm)
            if d < best_d:
                best_d = d
                best_L = float(L)

        ok = best_d <= th.REACH_TOL_MM
        return ReachabilityResult(
            reachable=ok,
            min_distance_mm=best_d,
            suggested_boom_mm=best_L,
            reason="" if ok else "DIG_UNREACHABLE",
        )
