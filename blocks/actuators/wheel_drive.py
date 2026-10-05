"""
BLOCK: Skid-steer wheel drive (4x BTS7960 + OG555).
Commands: left/right -255..255 (matches phase-1 protocol).
"""

from excavation_control.config import hardware as hw


class WheelDriveBlock:
    def __init__(self, max_cmd: int = 255):
        self.max_cmd = max_cmd

    def clamp(self, v: int) -> int:
        return max(-self.max_cmd, min(self.max_cmd, int(v)))

    def skid_steer(self, serial, forward: int, turn: int) -> None:
        left = self.clamp(forward + turn)
        right = self.clamp(forward - turn)
        serial.send_motors(left, right)

    def stop(self, serial) -> None:
        serial.send_motors(0, 0)

    def creep_forward(self, serial, speed: int = 40) -> None:
        """Low-speed creep during penetration only."""
        self.skid_steer(serial, self.clamp(speed), 0)

    def reverse_recovery(self, serial, speed: int = 60, duration_s: float = 0.5):
        """Use in recovery — caller handles timing."""
        self.skid_steer(serial, -self.clamp(speed), 0)
