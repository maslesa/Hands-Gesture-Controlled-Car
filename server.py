from flask import Flask, render_template
from flask_socketio import SocketIO
import cv2
import mediapipe as mp
import time
import base64
import threading


# initialize hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')


def detect_hand_gesture():
    cap = cv2.VideoCapture(0)

    while True:
        success, image = cap.read()
        if not success:
            continue

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)

        command = 'stop'

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:

                # fingers lanmarks
                thumb_cmc = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_CMC]
                thumb_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP]
                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
                index_finger_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]
                index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                middle_finger_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
                middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
                ring_finger_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP]
                ring_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
                pinky_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP]
                pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
                
                # right hand
                if thumb_cmc.x > wrist.x:
                    if index_finger_tip.y < index_finger_mcp.y and middle_finger_tip.y < middle_finger_mcp.y and thumb_tip.y < thumb_mcp.y and ring_finger_tip.y < ring_finger_mcp.y and pinky_tip.y < pinky_mcp.y:
                        command = 'stop'
                    elif index_finger_tip.y < index_finger_mcp.y and middle_finger_tip.y < middle_finger_mcp.y and ring_finger_tip.y > ring_finger_mcp.y and pinky_tip.y > pinky_mcp.y:
                        command = 'forward'
                    elif thumb_cmc.x < thumb_tip.x and index_finger_tip.y > index_finger_mcp.y and middle_finger_tip.y > middle_finger_mcp.y and ring_finger_tip.y > ring_finger_mcp.y and pinky_tip.y > pinky_mcp.y:
                        command = 'left'
                    elif thumb_cmc.x > thumb_tip.x and index_finger_tip.y > index_finger_mcp.y and middle_finger_tip.y > middle_finger_mcp.y and ring_finger_tip.y > ring_finger_mcp.y and pinky_tip.y < pinky_mcp.y:
                        command = 'right'
                    elif thumb_cmc.x > thumb_tip.x and index_finger_tip.y > index_finger_mcp.y and middle_finger_tip.y > middle_finger_mcp.y:
                        command = 'backwards'
                    

                # left hand
                if thumb_cmc.x < wrist.x:
                    if index_finger_tip.y < index_finger_mcp.y and middle_finger_tip.y < middle_finger_mcp.y and thumb_tip.y < thumb_mcp.y and ring_finger_tip.y < ring_finger_mcp.y and pinky_tip.y < pinky_mcp.y:
                        command = 'stop'
                    elif index_finger_tip.y < index_finger_mcp.y and middle_finger_tip.y < middle_finger_mcp.y and ring_finger_tip.y > ring_finger_mcp.y and pinky_tip.y > pinky_mcp.y:
                        command = 'forward'
                    elif thumb_cmc.x > thumb_tip.x and index_finger_tip.y > index_finger_mcp.y and middle_finger_tip.y > middle_finger_mcp.y and ring_finger_tip.y > ring_finger_mcp.y and pinky_tip.y > pinky_mcp.y:
                        command = 'right'
                    elif thumb_cmc.x < thumb_tip.x and index_finger_tip.y > index_finger_mcp.y and middle_finger_tip.y > middle_finger_mcp.y and ring_finger_tip.y > ring_finger_mcp.y and pinky_tip.y < pinky_mcp.y:
                        command = 'left'
                    elif thumb_cmc.x < thumb_tip.x and index_finger_tip.y > index_finger_mcp.y and middle_finger_tip.y > middle_finger_mcp.y:
                        command = 'backwards'


                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        socketio.emit('gesture', {'command': command})

        _, buffer = cv2.imencode('.jpg', image)
        image_str = base64.b64encode(buffer).decode('utf-8')
        socketio.emit('image', {'image': image_str})

        # [for testing this file only]
        # cv2.imshow('Hand Recognition', image)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

        print(command)
        time.sleep(0.1)


@app.route('/')
def host_webpage():
    return render_template('index.html')


if __name__ == '__main__':
    threading.Thread(target=detect_hand_gesture, daemon=True).start()
    socketio.run(app, host='0.0.0.0', port=5000)