"""
BLOCK: Boom linear actuator command + soft limits.
"""

from excavation_control.config import hardware as hw


class BoomActuatorBlock:
    def __init__(self):
        self.soft_min = hw.BOOM_LA_SOFT_MIN_MM
        self.soft_max = hw.BOOM_LA_SOFT_MAX_MM

    @staticmethod
    def stroke_mm(length_mm: float) -> float:
        return length_mm - hw.BOOM_LA_LENGTH_CLOSED_MM

    @staticmethod
    def length_from_stroke(stroke_mm: float) -> float:
        return hw.BOOM_LA_LENGTH_CLOSED_MM + stroke_mm

    def clamp_length(self, length_mm: float) -> float:
        return max(self.soft_min, min(self.soft_max, length_mm))

    def command_move(self, serial, length_mm: float, vel_mm_s: float) -> None:
        length_mm = self.clamp_length(length_mm)
        serial.send_boom(length_mm, vel_mm_s)

    def command_stop(self, serial, current_length_mm: float) -> None:
        serial.send_boom(current_length_mm, 0.0)
