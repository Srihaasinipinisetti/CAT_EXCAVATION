"""
BLOCK: Clamshell (cross-member) linear actuator.
"""

from excavation_control.config import hardware as hw


class ClamshellActuatorBlock:
    OPEN_MM = hw.CLAM_LA_SOFT_MAX_MM
    CLOSED_MM = hw.CLAM_LA_SOFT_MIN_MM

    def __init__(self):
        self.soft_min = hw.CLAM_LA_SOFT_MIN_MM
        self.soft_max = hw.CLAM_LA_SOFT_MAX_MM

    def clamp(self, stroke_mm: float) -> float:
        return max(self.soft_min, min(self.soft_max, stroke_mm))

    @staticmethod
    def height_estimate(stroke_mm: float) -> float:
        """Proxy assembly height from stroke (sample linear map)."""
        t = (hw.CLAM_LA_SOFT_MAX_MM - stroke_mm) / (
            hw.CLAM_LA_SOFT_MAX_MM - hw.CLAM_LA_SOFT_MIN_MM
        )
        return hw.CLAM_HEIGHT_OPEN_MM + t * (hw.CLAM_HEIGHT_CLOSED_MM - hw.CLAM_HEIGHT_OPEN_MM)

    def command_open(self, serial, vel_mm_s: float = 8.0) -> None:
        serial.send_clam(self.OPEN_MM, vel_mm_s)

    def command_close(self, serial, vel_mm_s: float = 5.0) -> None:
        serial.send_clam(self.CLOSED_MM, vel_mm_s)

    def command_position(self, serial, stroke_mm: float, vel_mm_s: float) -> None:
        serial.send_clam(self.clamp(stroke_mm), vel_mm_s)
