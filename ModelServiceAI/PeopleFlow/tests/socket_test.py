import asyncio
import cv2
import websockets
import json


async def run_socket_with_video():
    uri = "ws://127.0.0.1:8000/apiV1/track"
    video_path = "data/test_socket.mp4"
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Не удалось открыть видео")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    frames_to_process = int(fps * 10)
    current_frame = 0

    print(f"Начинаю обработку 10 секунд видео ({frames_to_process} кадров)...")

    async with websockets.connect(uri) as websocket:
        while cap.isOpened() and current_frame < frames_to_process:
            success, frame = cap.read()
            if not success:
                break

            _, buffer = cv2.imencode('.jpg', frame)
            await websocket.send(buffer.tobytes())

            try:
                response = await websocket.recv()
                print(f"Frame {current_frame} response: {json.loads(response)}")
            except Exception as e:
                print(f"Error: {e}")
                break

            current_frame += 1

    cap.release()
    print("10 секунд обработано, работа завершена.")

if __name__ == "__main__":
    asyncio.run(run_socket_with_video())