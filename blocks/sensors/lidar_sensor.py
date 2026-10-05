"""
BLOCK: LiDAR on Raspberry Pi (navigation / dig zone — not wall following for scoring).
"""

from dataclasses import dataclass, field
from typing import List, Optional, Tuple
import time

from excavation_control.config import hardware as hw


@dataclass
class LidarScan:
    ranges_m: List[float] = field(default_factory=list)
    angle_min_rad: float = -3.14159
    angle_increment_rad: float = 0.01
    timestamp: float = field(default_factory=time.time)
    valid: bool = False


class LidarBlock:
    """Wrap RPLidar / YDLidar serial driver — stub for simulation."""

    def __init__(self, port: str = hw.LIDAR_PORT, baud: int = hw.LIDAR_BAUD):
        self.port = port
        self.baud = baud
        self._connected = False

    def connect(self) -> bool:
        if hw.SIMULATION_MODE:
            self._connected = True
            return True
        # TODO: import your lidar library and open self.port
        self._connected = False
        return False

    def read_scan(self) -> LidarScan:
        if hw.SIMULATION_MODE:
            # Fake open path ahead
            n = 360
            ranges = [2.0] * n
            ranges[0] = 0.8
            return LidarScan(ranges_m=ranges, valid=True)
        return LidarScan(valid=False)

    def nearest_obstacle_ahead_m(self, scan: LidarScan, fov_deg: float = 30.0) -> Optional[float]:
        if not scan.valid or not scan.ranges_m:
            return None
        n = len(scan.ranges_m)
        center = n // 2
        span = int((fov_deg / 360.0) * n)
        window = scan.ranges_m[center - span : center + span]
        good = [r for r in window if 0.15 < r < 8.0]
        return min(good) if good else None

    def estimate_dig_face_distance_m(self, scan: LidarScan) -> Optional[float]:
        """Sample: distance to sand pile / excavation face in front."""
        return self.nearest_obstacle_ahead_m(scan, fov_deg=20.0)
