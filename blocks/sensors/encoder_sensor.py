"""
BLOCK: Wheel encoders (OE-37 on OG555 motor shaft → wheel shaft CPR).
"""

from dataclasses import dataclass, field
import math
import time
from typing import Dict, Optional, Tuple

from excavation_control.config import hardware as hw


@dataclass
class EncoderSnapshot:
    counts_fl: int = 0
    counts_fr: int = 0
    counts_rl: int = 0
    counts_rr: int = 0
    timestamp: float = field(default_factory=time.time)

    def counts(self) -> Tuple[int, int, int, int]:
        return self.counts_fl, self.counts_fr, self.counts_rl, self.counts_rr


class EncoderBlock:
    """Wheel odometry from quadrature counts."""

    def __init__(self):
        self.cpr = hw.ENCODER_CPR_WHEEL_SHAFT
        self.wheel_circ_m = math.pi * (hw.WHEEL_DIAMETER_MM / 1000.0)
        self.m_per_count = self.wheel_circ_m / self.cpr
        self._prev: Optional[EncoderSnapshot] = None

    def update(self, raw: Dict[str, int]) -> EncoderSnapshot:
        snap = EncoderSnapshot(
            counts_fl=int(raw.get("enc_fl", 0)),
            counts_fr=int(raw.get("enc_fr", 0)),
            counts_rl=int(raw.get("enc_rl", 0)),
            counts_rr=int(raw.get("enc_rr", 0)),
        )
        self._prev = snap
        return snap

    def linear_speed_m_s(
        self, snap: EncoderSnapshot, side: str = "left", dt: Optional[float] = None
    ) -> float:
        if self._prev is None or dt is None or dt <= 0:
            return 0.0
        if side == "left":
            dc = (snap.counts_rl - self._prev.counts_rl + snap.counts_fl - self._prev.counts_fl) / 2
        else:
            dc = (snap.counts_rr - self._prev.counts_rr + snap.counts_fr - self._prev.counts_fr) / 2
        return (dc * self.m_per_count) / dt

    def body_velocity_estimate(
        self, snap: EncoderSnapshot, dt: float
    ) -> Tuple[float, float]:
        """Returns (v_forward_m_s, yaw_rate_rad_s) skid-steer sample model."""
        if self._prev is None or dt <= 0:
            return 0.0, 0.0
        v_l = self.linear_speed_m_s(snap, "left", dt)
        v_r = self.linear_speed_m_s(snap, "right", dt)
        v = 0.5 * (v_l + v_r)
        track = hw.TRACK_WIDTH_MM / 1000.0
        omega = (v_r - v_l) / track if track > 0 else 0.0
        return v, omega

    def delta_counts_left(self, snap: EncoderSnapshot) -> int:
        if self._prev is None:
            return 0
        return abs(
            (snap.counts_fl - self._prev.counts_fl) + (snap.counts_rl - self._prev.counts_rl)
        ) // 2
