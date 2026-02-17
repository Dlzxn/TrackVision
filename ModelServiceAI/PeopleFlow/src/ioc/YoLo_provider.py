from dishka import Provider, Scope, provide
from PeopleFlow.src.domain.services.detector import YOLOContract
from PeopleFlow.src.infrastructure.YoLoImpl import YOLOManager

class AIProvider(Provider):
    @provide(scope=Scope.APP)
    def get_detector(self) -> YOLOContract:
        return YOLOManager()