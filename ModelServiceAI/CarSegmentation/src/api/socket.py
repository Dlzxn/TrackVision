from fastapi import WebSocket, WebSocketDisconnect, APIRouter
from dishka.integrations.fastapi import FromDishka, inject

import cv2, random
import numpy as np

from src.domain.YoLoContract import YoLoAbstract
from src.domain.OCRcontract import OCRAbstract
from src.utils.resize import resize_frame


socket: APIRouter = APIRouter(
    prefix = "/apiV2"
)


@socket.websocket("/ocr")
@inject
async def track_people(
        websocket: WebSocket,
        yolo_manager: FromDishka[YoLoAbstract],
        ocr_manager: FromDishka[OCRAbstract],
):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_bytes()
            nparr = np.frombuffer(data, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            response_json = {
                "status": False,
                "number": None
            }

            if frame is not None:
                size = yolo_manager.predict(frame)
                if size is not None:
                    print("Size is not None: ", size)
                    number_frame = resize_frame(frame, size)
                    number = ocr_manager.read(number_frame)

                    print("Number:", number)
                    if number is not None and number != "":
                        response_json["number"] = number
                        response_json["status"] = True
                        cv2.imwrite(f"data/example/{number}.jpg", number_frame)

            await websocket.send_json(response_json)


    except WebSocketDisconnect as e:
        print("WebSocket has been disconnected")

