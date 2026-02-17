from abc import ABC, abstractmethod
import numpy as np

class OCRAbstract(ABC):
    @abstractmethod
    def _get_number(self, frame: np.ndarray) -> list:
        """Метод для получения сырых данных от движка OCR"""
        pass

    @abstractmethod
    def _get_result(self, result: list) -> str:
        """Метод для парсинга сырых данных в чистую строку"""
        pass

    def read(self, frame: np.ndarray) -> str:
        # Template Method: определяем скелет алгоритма
        if frame is None or frame.size == 0:
            return ""
        res = self._get_number(frame)
        return self._get_result(res)