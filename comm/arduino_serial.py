"""
BLOCK: Raspberry Pi ↔ Arduino serial protocol.

Telemetry from Arduino (example line):
  T <v_bat> <i_bat> <i_boom> <i_clam> <i_fl> <i_fr> <i_rl> <i_rr> <boom_mm> <clam_mm> <enc_fl> ...

Commands to Arduino:
  M <left> <right>           wheel speeds -255..255
  B <boom_mm> <vel_mm_s>     boom linear actuator
  C <clam_mm> <vel_mm_s>     clamshell linear actuator
  X                          emergency stop
"""

import time
from typing import Optional, Dict, Any

from excavation_control.config import hardware as hw


class ArduinoSerial:
    def __init__(self):
        self._ser = None
        self.connected = False
        self._last_cmd_time = time.time()

    def connect(self) -> bool:
        if hw.SIMULATION_MODE:
            self.connected = True
            print("[ArduinoSerial] SIMULATION")
            return True
        try:
            import serial

            self._ser = serial.Serial(hw.SERIAL_PORT, hw.SERIAL_BAUD, timeout=0.05)
            self.connected = True
            return True
        except Exception as e:
            print(f"[ArduinoSerial] connect failed: {e}")
            return False

    def _write_line(self, line: str):
        self._last_cmd_time = time.time()
        if hw.SIMULATION_MODE:
            print(f"[SIM TX] {line}")
            return
        if self._ser:
            self._ser.write((line + "\n").encode())

    def send_motors(self, left: int, right: int):
        left = max(-255, min(255, int(left)))
        right = max(-255, min(255, int(right)))
        self._write_line(f"M {left} {right}")

    def send_boom(self, length_mm: float, vel_mm_s: float):
        self._write_line(f"B {length_mm:.1f} {vel_mm_s:.1f}")

    def send_clam(self, stroke_mm: float, vel_mm_s: float):
        self._write_line(f"C {stroke_mm:.1f} {vel_mm_s:.1f}")

    def emergency_stop(self):
        self._write_line("X")

    def read_telemetry(self) -> Optional[Dict[str, Any]]:
        if hw.SIMULATION_MODE:
            return self._sim_telemetry()
        if not self._ser or not self._ser.in_waiting:
            return None
        try:
            line = self._ser.readline().decode(errors="ignore").strip()
            return self._parse_t_line(line)
        except Exception:
            return None

    @staticmethod
    def _parse_t_line(line: str) -> Optional[Dict[str, Any]]:
        if not line.startswith("T "):
            return None
        p = line.split()
        if len(p) < 14:
            return None
        return {
            "v_bat": float(p[1]),
            "i_bat": float(p[2]),
            "i_boom_a": float(p[3]),
            "i_clam_a": float(p[4]),
            "i_wheel_fl_a": float(p[5]),
            "i_wheel_fr_a": float(p[6]),
            "i_wheel_rl_a": float(p[7]),
            "i_wheel_rr_a": float(p[8]),
            "boom_mm": float(p[9]),
            "clam_mm": float(p[10]),
            "enc_fl": int(p[11]),
            "enc_fr": int(p[12]),
            "enc_rl": int(p[13]),
            "enc_rr": int(p[14]) if len(p) > 14 else 0,
            "pitch": float(p[15]) if len(p) > 15 else 0.0,
            "roll": float(p[16]) if len(p) > 16 else 0.0,
        }

    def _sim_telemetry(self) -> Dict[str, Any]:
        return {
            "v_bat": 11.8,
            "i_bat": 2.0,
            "i_boom_a": 0.5,
            "i_clam_a": 0.4,
            "i_wheel_fl_a": 0.0,
            "i_wheel_fr_a": 0.0,
            "i_wheel_rl_a": 0.0,
            "i_wheel_rr_a": 0.0,
            "boom_mm": 270.0,
            "clam_mm": 45.0,
            "enc_fl": 0,
            "enc_fr": 0,
            "enc_rl": 0,
            "enc_rr": 0,
            "pitch": 1.0,
            "roll": 0.5,
        }

    def disconnect(self):
        if self._ser:
            self._ser.close()
        self.connected = False
