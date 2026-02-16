from ultralytics import YOLO
import cv2
import numpy as np

from ModelServiceAI.src.domain.services.detector import YOLOContract


class YOLOManager(YOLOContract):
    def __init__(self, model_path: str = "data/model_pt/yolo26n.pt"):
        super().__init__(model_path)

    def _yolo_predict(self, frame: cv2.Mat | np.ndarray) -> list:
        result = self.model.predict(frame, classes=[0], verbose=False)
        return result

    def _find_result(self, result) -> int:
        return len(result[0].boxes)


