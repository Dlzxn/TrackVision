from ultralytics import YOLO
from abc import abstractmethod, ABC


class YOLOContract(ABC):
    def __init__(self, model_path: str = "data/model_pt/yolo26n.pt"):
        self.model = YOLO(model_path)

    @abstractmethod
    def _yolo_predict(self, frame: cv2.Mat | np.array) -> list:
        pass

    @abstractmethod
    def _find_result(self, result) -> int:
        pass

    def predict(self, frame: cv2.Mat | np.array) -> int | None:
        try:
            res = self._yolo_predict(frame)
            num_people = self._find_result(res)
            return num_people

        except Exception as e:
            return None

