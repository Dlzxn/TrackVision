import cv2
import numpy as np

from src.domain.YoLoContract import YoLoAbstract



class YoLoManager(YoLoAbstract):
    def __init__(self, path: str):
        super().__init__(path)

    def _yolo_predict(self, frame: cv2.Mat | np.ndarray) -> list:
        return self.model.predict(frame, verbose=False)


    def _find_result(self, result) -> tuple[int, int, int, int] | None:
        if len(result[0].boxes) > 0:
            best_box = max(result[0].boxes, key=lambda b: (b.xyxy[0][2] - b.xyxy[0][0]) * (b.xyxy[0][3] - b.xyxy[0][1]))
            return map(int, best_box.xyxy[0])
        else:
            return None