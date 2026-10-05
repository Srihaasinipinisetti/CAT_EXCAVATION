"""
BLOCK: Battery voltage / pack current (PZEM or shunt on Pi/Arduino).
"""

from dataclasses import dataclass, field
import time
from typing import Dict, Optional

from excavation_control.config import thresholds as th


@dataclass
class BatteryState:
    voltage_v: float = 12.0
    current_a: float = 0.0
    power_w: float = 0.0
    timestamp: float = field(default_factory=time.time)

    level: str = "NORMAL"  # NORMAL, WARN, CRIT, EMERG


class BatteryMonitorBlock:
    def __init__(self):
        self._last: Optional[BatteryState] = None

    def update(self, raw: Dict[str, float]) -> BatteryState:
        v = float(raw.get("v_bat", 12.0))
        i = float(raw.get("i_bat", 0.0))
        st = BatteryState(voltage_v=v, current_a=i, power_w=v * i)
        st.level = self._classify_voltage(v)
        self._last = st
        return st

    def _classify_voltage(self, v: float) -> str:
        if v < th.V_BAT_EMERG_V:
            return "EMERG"
        if v < th.V_BAT_CRIT_V:
            return "CRIT"
        if v < th.V_BAT_WARN_V:
            return "WARN"
        return "NORMAL"

    def current_level(self, i_ma: float) -> str:
        if i_ma > th.I_BAT_CRIT_FRAC * th.I_BAT_CONT_A:
            return "CRIT"
        if i_ma > th.I_BAT_WARN_FRAC * th.I_BAT_CONT_A:
            return "HIGH"
        return "NORMAL"

    @property
    def last(self) -> Optional[BatteryState]:
        return self._last
