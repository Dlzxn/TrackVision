from dishka import Provider, Scope, provide

from src.domain.YoLoContract import YoLoAbstract
from src.domain.OCRcontract import OCRAbstract
from src.infrastructure.YoLoManager import YoLoManager
from src.infrastructure.OCRManager import OCRManager



class AIProvider(Provider):
    @provide(scope=Scope.APP)
    def get_detector(self) -> YoLoAbstract:
        return YoLoManager("data/model_pt/yolo26n.pt")

    @provide(scope=Scope.APP)
    def get_ocr(self) -> OCRAbstract:
        return OCRManager()