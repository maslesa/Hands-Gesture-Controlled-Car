import asyncio
import websockets
import cv2
import mediapipe as mp
import time


mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)

connected_clients = set()

async def send_command(command):
    """Send command to all connected WebSocket clients (ESP32)."""
    if connected_clients:
        tasks = [ws.send(command) for ws in connected_clients]
        await asyncio.gather(*tasks)

async def detect_hand_gesture():
    """Detect hand gestures and send commands via WebSocket."""
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FPS, 10)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    while True:
        success, image = cap.read()
        if not success:
            continue

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)
        command = "stop"

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
                index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                index_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
                middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
                middle_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP]

                if thumb_tip.x > wrist.x:
                    if index_tip.y < index_mcp.y and middle_tip.y < middle_mcp.y:
                        command = "forward"
                    elif index_tip.y > index_mcp.y and middle_tip.y > middle_mcp.y:
                        command = "backward"
                    elif thumb_tip.x > wrist.x:
                        command = "left"
                    elif thumb_tip.x < wrist.x:
                        command = "right"

        print(f"🖐 Detected Command: {command}")
        await send_command(command)
        await asyncio.sleep(0.1)

async def websocket_server(websocket):
    """Handle WebSocket connections (ESP32)."""
    print(f"🔗 New WebSocket Client Connected: {websocket.remote_address}")
    connected_clients.add(websocket)

    try:
        async for message in websocket:
            print(f"📩 Received from ESP32: {message}")
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        connected_clients.remove(websocket)
        print("❌ WebSocket Client Disconnected")

async def start_websocket():
    """Start WebSocket server."""
    async with websockets.serve(websocket_server, "0.0.0.0", 5000):
        await asyncio.Future()  # Keeps the server running

async def main():
    await asyncio.gather(detect_hand_gesture(), start_websocket())

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except:
        pass
