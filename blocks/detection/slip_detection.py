"""
BLOCK: Wheel slip (encoder vs IMU-integrated forward velocity).
"""

from dataclasses import dataclass

from excavation_control.config import thresholds as th


@dataclass
class SlipStatus:
    ratio: float = 0.0
    level: str = "NORMAL"


class SlipDetectionBlock:
    def evaluate(self, v_enc_m_s: float, v_imu_m_s: float) -> SlipStatus:
        denom = max(abs(v_enc_m_s), th.SLIP_V_EPS_M_S)
        ratio = abs(v_enc_m_s - v_imu_m_s) / denom
        if ratio >= th.SLIP_EMERG:
            level = "EMERG"
        elif ratio >= th.SLIP_CRIT:
            level = "CRIT"
        elif ratio >= th.SLIP_WARN:
            level = "WARN"
        else:
            level = "NORMAL"
        return SlipStatus(ratio=ratio, level=level)
