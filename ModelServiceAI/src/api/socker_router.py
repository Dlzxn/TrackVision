from fastapi import WebSocket, WebSocketDisconnect, APIRouter
import cv2
import numpy as np

from ModelServiceAI.src.Infrastructure.YoLoImpl import YOLOManager
from ModelServiceAI.src.utils.json_out import json_output_model


socket: APIRouter = APIRouter(
    prefix = "apiV1"
)


@socket.websocket("/track")
async def track_people(websocket: WebSocket):
    await websocket.accept()
    manager = YOLOManager()
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




