import cv2
import numpy as np

from abc import abstractmethod, ABC
from ultralytics import YOLO



class YoLoAbstract(ABC):
    def __init__(self, model_path: str = "data/model_pt/yolo26n.pt"):
        self.model = YOLO(model_path)

    @abstractmethod
    def _yolo_predict(self, frame: cv2.Mat | np.ndarray) -> list:
        pass

    @abstractmethod
    def _find_result(self, result) -> int:
        pass

    def predict(self, frame: cv2.Mat | np.ndarray) -> tuple[int, int, int, int] | None:
        """Возвращает нужный размер"""
        try:
            res = self._yolo_predict(frame)
            size = self._find_result(res)
            return size

        except Exception as e:
            return None
