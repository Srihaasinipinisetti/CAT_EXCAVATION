"""
BLOCK: Raspberry Pi camera — visual telemetry / optional berm alignment (hands-free only).
"""

from dataclasses import dataclass, field
from typing import Any, Optional
import time

from excavation_control.config import hardware as hw


@dataclass
class CameraFrame:
    timestamp: float = field(default_factory=time.time)
    width: int = hw.CAMERA_WIDTH
    height: int = hw.CAMERA_HEIGHT
    frame: Any = None  # numpy array when OpenCV enabled
    valid: bool = False


class CameraBlock:
    def __init__(self):
        self._cap = None

    def connect(self) -> bool:
        if hw.SIMULATION_MODE:
            return True
        try:
            import cv2

            self._cap = cv2.VideoCapture(hw.CAMERA_INDEX)
            self._cap.set(3, hw.CAMERA_WIDTH)
            self._cap.set(4, hw.CAMERA_HEIGHT)
            return self._cap.isOpened()
        except ImportError:
            return False

    def read(self) -> CameraFrame:
        if hw.SIMULATION_MODE:
            return CameraFrame(valid=True)
        if self._cap is None:
            return CameraFrame(valid=False)
        import cv2

        ok, frame = self._cap.read()
        return CameraFrame(frame=frame, valid=ok)

    def release(self):
        if self._cap is not None:
            import cv2

            self._cap.release()
            self._cap = None
