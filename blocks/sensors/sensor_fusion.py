"""
BLOCK: Fuse Arduino telemetry + Pi sensors into one RobotSnapshot.
"""

from dataclasses import dataclass, field
import time
from typing import Optional

from excavation_control.blocks.sensors.current_sensor import CurrentReadings, CurrentSensorBlock
from excavation_control.blocks.sensors.encoder_sensor import EncoderBlock, EncoderSnapshot
from excavation_control.blocks.sensors.battery_monitor import BatteryMonitorBlock, BatteryState
from excavation_control.blocks.sensors.imu_sensor import ImuBlock, ImuState
from excavation_control.config import thresholds as th


@dataclass
class ActuatorFeedback:
    boom_length_mm: float = 255.0
    clam_stroke_mm: float = 40.0
    boom_cmd_vel_mm_s: float = 0.0
    clam_cmd_vel_mm_s: float = 0.0


@dataclass
class RobotSnapshot:
    current: CurrentReadings = field(default_factory=CurrentReadings)
    encoders: EncoderSnapshot = field(default_factory=EncoderSnapshot)
    battery: BatteryState = field(default_factory=BatteryState)
    imu: ImuState = field(default_factory=ImuState)
    actuators: ActuatorFeedback = field(default_factory=ActuatorFeedback)
    telem_age_s: float = 0.0
    timestamp: float = field(default_factory=time.time)


class SensorFusionBlock:
    def __init__(self):
        self.current = CurrentSensorBlock()
        self.encoders = EncoderBlock()
        self.battery = BatteryMonitorBlock()
        self.imu = ImuBlock()
        self._last_telem_time = time.time()

    def ingest_arduino_packet(self, parsed: dict) -> RobotSnapshot:
        self._last_telem_time = time.time()
        snap = RobotSnapshot()
        snap.current = self.current.update_from_telemetry(parsed)
        snap.encoders = self.encoders.update(parsed)
        snap.battery = self.battery.update(parsed)
        snap.imu = self.imu.update(parsed)
        snap.actuators = ActuatorFeedback(
            boom_length_mm=float(parsed.get("boom_mm", 255)),
            clam_stroke_mm=float(parsed.get("clam_mm", 40)),
            boom_cmd_vel_mm_s=float(parsed.get("boom_cmd_v", 0)),
            clam_cmd_vel_mm_s=float(parsed.get("clam_cmd_v", 0)),
        )
        snap.telem_age_s = 0.0
        snap.timestamp = time.time()
        return snap

    def simulate(self, phase: str = "idle") -> RobotSnapshot:
        self._last_telem_time = time.time()
        snap = RobotSnapshot()
        snap.current = self.current.simulate_sample(phase)
        snap.battery = self.battery.update({"v_bat": 11.8, "i_bat": snap.current.i_bat_a})
        snap.actuators.boom_length_mm = 260.0
        snap.actuators.clam_stroke_mm = 45.0
        return snap

    def comm_ok(self) -> bool:
        return (time.time() - self._last_telem_time) < th.COMM_TIMEOUT_S

    def encoders_fresh(self, snap: RobotSnapshot) -> bool:
        return snap.telem_age_s * 1000 < th.ENCODER_STALE_MS
