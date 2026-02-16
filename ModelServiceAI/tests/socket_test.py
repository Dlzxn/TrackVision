import asyncio
import cv2
import websockets
import json


async def test_socket_with_video():
    uri = "ws://127.0.0.1:8000/apiV1/track"
    video_path = "Data/test_socket.mp4"
    cap = cv2.VideoCapture(video_path)

    async with websockets.connect(uri) as websocket:
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break

            _, buffer = cv2.imencode('.jpg', frame)
            await websocket.send(buffer.tobytes())

            try:
                response = await websocket.recv()
                data = json.loads(response)
                print(f"Server response: {data}")

                assert data["status"] is True
                assert "num" in data
            except Exception as e:
                print(f"Error: {e}")
                break

    cap.release()


if __name__ == "__main__":
    asyncio.run(test_socket_with_video())