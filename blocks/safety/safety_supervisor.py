"""
BLOCK: Safety supervisor — thresholds, estop, faults.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List

from excavation_control.config import thresholds as th
from excavation_control.blocks.sensors.sensor_fusion import RobotSnapshot
from excavation_control.blocks.detection.stall_detection import StallType


class FaultCode(str, Enum):
    NONE = "NONE"
    OVERCURRENT_BOOM = "OVERCURRENT_BOOM"
    OVERCURRENT_CLAM = "OVERCURRENT_CLAM"
    OVERCURRENT_WHEEL = "OVERCURRENT_WHEEL"
    UNDERVOLTAGE = "UNDERVOLTAGE"
    STALL = "STALL"
    SLIP = "SLIP"
    IMU_TIP = "IMU_TIP"
    COMM_LOSS = "COMM_LOSS"
    TIMEOUT = "TIMEOUT"
    EMERGENCY_STOP = "EMERGENCY_STOP"


@dataclass
class SafetyStatus:
    ok: bool = True
    faults: List[FaultCode] = field(default_factory=list)
    estop: bool = False


class SafetySupervisorBlock:
    def evaluate(
        self,
        snap: RobotSnapshot,
        comm_ok: bool,
        stall: StallType,
        slip_level: str,
        estop_button: bool,
    ) -> SafetyStatus:
        faults: List[FaultCode] = []
        if estop_button:
            faults.append(FaultCode.EMERGENCY_STOP)
        if not comm_ok:
            faults.append(FaultCode.COMM_LOSS)
        if snap.current.i_boom_a > th.I_LA_EMERG_A:
            faults.append(FaultCode.OVERCURRENT_BOOM)
        if snap.current.i_clam_a > th.I_LA_EMERG_A:
            faults.append(FaultCode.OVERCURRENT_CLAM)
        if snap.current.i_wheel_mean_a > th.I_WHEEL_CRIT_A:
            faults.append(FaultCode.OVERCURRENT_WHEEL)
        if snap.battery.voltage_v < th.V_BAT_EMERG_V:
            faults.append(FaultCode.UNDERVOLTAGE)
        if stall != StallType.NONE:
            faults.append(FaultCode.STALL)
        if slip_level in ("CRIT", "EMERG"):
            faults.append(FaultCode.SLIP)
        if abs(snap.imu.pitch_deg) > th.PITCH_CRIT_DEG or abs(snap.imu.roll_deg) > th.ROLL_CRIT_DEG:
            faults.append(FaultCode.IMU_TIP)

        st = SafetyStatus(ok=len(faults) == 0, faults=faults, estop=estop_button)
        return st
