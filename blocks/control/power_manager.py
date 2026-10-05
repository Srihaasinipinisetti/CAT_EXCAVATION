"""
BLOCK: Power consumption protection + actuator arbitration.
"""

from dataclasses import dataclass
from enum import Enum
import time

from excavation_control.config import thresholds as th


class PowerState(str, Enum):
    NORMAL = "NORMAL"
    HIGH = "HIGH"
    EXCESSIVE = "EXCESSIVE"
    CRITICAL = "CRITICAL"


@dataclass
class PowerDecision:
    state: PowerState
    allow_penetration: bool
    allow_clam_close: bool
    allow_wheel_torque: bool
    wheel_scale: float


class PowerManagerBlock:
    def __init__(self):
        self._i_ma = 0.0
        self._high_since: float | None = None
        self._crit_since: float | None = None

    def _ema(self, prev: float, x: float, dt: float) -> float:
        alpha = dt / (th.CURRENT_EMA_TAU_S + dt)
        return prev + alpha * (x - prev)

    def update(self, i_bat_a: float, v_bat_v: float, dt: float) -> PowerDecision:
        self._i_ma = self._ema(self._i_ma, i_bat_a, dt)
        now = time.time()

        dec = PowerDecision(PowerState.NORMAL, True, True, True, 1.0)

        if self._i_ma > th.I_BAT_CRIT_FRAC * th.I_BAT_CONT_A:
            self._crit_since = self._crit_since or now
        else:
            self._crit_since = None

        if self._i_ma > th.I_BAT_WARN_FRAC * th.I_BAT_CONT_A:
            self._high_since = self._high_since or now
        else:
            self._high_since = None

        if self._crit_since and now - self._crit_since > th.I_CRIT_HOLD_S:
            dec.state = PowerState.CRITICAL
            dec.allow_penetration = False
            dec.allow_clam_close = False
            dec.wheel_scale = 0.3
        elif self._high_since and now - self._high_since > th.I_HIGH_HOLD_S:
            dec.state = PowerState.HIGH
            dec.allow_penetration = False
            dec.allow_clam_close = True
            dec.wheel_scale = 0.5
        elif v_bat_v < th.V_BAT_CRIT_V:
            dec.state = PowerState.EXCESSIVE
            dec.allow_penetration = False
            dec.wheel_scale = 0.4

        return dec
