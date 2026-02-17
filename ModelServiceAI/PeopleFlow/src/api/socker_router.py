from fastapi import WebSocket, WebSocketDisconnect, APIRouter
from dishka.integrations.fastapi import FromDishka, inject

import cv2
import numpy as np

from PeopleFlow.src.domain.services.detector import YOLOContract
from PeopleFlow.src.utils.json_out import json_output_model


socket: APIRouter = APIRouter(
    prefix = "/apiV1"
)


@socket.websocket("/track")
@inject
async def track_people(
        websocket: WebSocket,
        manager: FromDishka[YOLOContract]
):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_bytes()
            nparr = np.frombuffer(data, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            if frame is not None:
                num_ppl = manager.predict(frame)
                out = json_output_model(num_ppl)
                await websocket.send_json(out)

    except WebSocketDisconnect as e:
        print("WebSocket has been disconnected")




