import asyncio
import cv2
import websockets
import json


async def send_frames(cap, websocket, frames_to_process):
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    current_second = 0
    total_seconds = 40

    print(f"FPS видео: {fps}. Буду отправлять по 1 кадру на каждую из {total_seconds} секунд.")

    while cap.isOpened() and current_second < total_seconds:
        frame_id = current_second * fps

        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_id)

        success, frame = cap.read()
        if not success:
            break

        frame = cv2.resize(frame, (1280, 720))
        _, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])

        try:
            await websocket.send(buffer.tobytes())
            print(f"Отправлен кадр для секунды: {current_second}")
        except Exception as e:
            print(f"Ошибка при отправке: {e}")
            break

        current_second += 1

        await asyncio.sleep(0.1)

    print("Отправка кадров (1 к/с) завершена.")


async def receive_responses(websocket):
    try:
        async for message in websocket:
            data = json.loads(message)
            print(f"Пришел ответ от сервера: {data}")
    except websockets.exceptions.ConnectionClosed:
        print("Соединение закрыто сервером.")


async def run_socket_with_video():
    uri = "ws://127.0.0.1:8000/apiV2/ocr"
    video_path = "data/video.mp4"
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    frames_to_process = int(fps * 40)

    async with websockets.connect(uri) as websocket:
        await asyncio.gather(
            send_frames(cap, websocket, frames_to_process),
            receive_responses(websocket)
        )

    cap.release()
    print("Работа полностью завершена.")


if __name__ == "__main__":
    asyncio.run(run_socket_with_video())