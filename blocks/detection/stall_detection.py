"""
BLOCK: Actuator and wheel stall detection.
"""

from dataclasses import dataclass
from enum import Enum
import time

from excavation_control.config import thresholds as th
from excavation_control.blocks.sensors.sensor_fusion import RobotSnapshot


class StallType(str, Enum):
    NONE = "NONE"
    BOOM = "BOOM_STALL"
    CLAM = "CLAM_STALL"
    WHEEL = "WHEEL_STALL"


@dataclass
class StallStatus:
    stall: StallType = StallType.NONE
    since: float = 0.0


class StallDetectionBlock:
    def __init__(self):
        self._boom_t0: float | None = None
        self._clam_t0: float | None = None
        self._wheel_t0: float | None = None
        self._prev_boom_mm = 0.0
        self._prev_clam_mm = 0.0

    def update(
        self,
        snap: RobotSnapshot,
        boom_cmd_v: float,
        clam_cmd_v: float,
        wheel_cmd: int,
        enc_delta_left: int,
    ) -> StallStatus:
        now = time.time()
        st = StallStatus()

        # Boom LA
        if abs(boom_cmd_v) > th.V_CMD_MIN_LA_MM_S:
            if (
                abs(snap.actuators.boom_length_mm - self._prev_boom_mm) < th.STALL_LA_DELTA_S_MM
                and snap.current.i_boom_a > th.I_LA_WARN_A
            ):
                self._boom_t0 = self._boom_t0 or now
                if now - self._boom_t0 > th.STALL_LA_TIME_BOOM_S:
                    return StallStatus(StallType.BOOM, self._boom_t0)
            else:
                self._boom_t0 = None
        else:
            self._boom_t0 = None

        # Clamshell LA
        if abs(clam_cmd_v) > th.V_CMD_MIN_LA_MM_S:
            if (
                abs(snap.actuators.clam_stroke_mm - self._prev_clam_mm) < th.STALL_LA_DELTA_S_MM
                and snap.current.i_clam_a > th.I_LA_WARN_A
            ):
                self._clam_t0 = self._clam_t0 or now
                if now - self._clam_t0 > th.STALL_LA_TIME_CLAM_S:
                    return StallStatus(StallType.CLAM, self._clam_t0)
            else:
                self._clam_t0 = None
        else:
            self._clam_t0 = None

        # Wheels
        if abs(wheel_cmd) > 25:
            if (
                enc_delta_left < th.STALL_WHEEL_MIN_COUNTS
                and snap.current.i_wheel_mean_a > th.STALL_WHEEL_I_MIN_A
            ):
                self._wheel_t0 = self._wheel_t0 or now
                if now - self._wheel_t0 > th.STALL_WHEEL_TIME_S:
                    return StallStatus(StallType.WHEEL, self._wheel_t0)
            else:
                self._wheel_t0 = None
        else:
            self._wheel_t0 = None

        self._prev_boom_mm = snap.actuators.boom_length_mm
        self._prev_clam_mm = snap.actuators.clam_stroke_mm
        return st
