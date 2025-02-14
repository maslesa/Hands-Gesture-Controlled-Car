# Hands Gesture Controlled Car

## Overview
 - This project enables control of a car using hand gestures detected through a webcam. It utilizes:
 - Flask and Flask-SocketIO for real-time communication.
 - MediaPipe for hand gesture recognition.
 - OpenCV for video processing.
 - ESP32 to control the car's motors via WebSockets.

## Features
 - Real-time hand gesture recognition.
 - Web-based interface for visual feedback.
 - WebSocket communication between the Flask server and ESP32.
 - Commands for controlling car movement (forward, backward, left, right, stop).

## Components
1. Flask Server (Python)
 - Captures video from the webcam.
 - Uses MediaPipe to detect hand gestures.
 - Sends gesture-based commands to the ESP32 via WebSockets.

2. Web Interface (HTML, CSS, JavaScript)
 - Displays live video feed.
 - Shows detected gesture commands.
 - Communicates with the Flask backend via Socket.IO.

3. ESP32 Firmware (Arduino)
 - Connects to Flask WebSocket server.
 - Interprets received commands and controls the car's motors accordingly.

## Hand Gesture Commands (right hand)
| Gesture  | Action |
| ------------- | ------------- |
| All fingers up  | Stop  |
| Index & middle up  | Forward  |
| Thumb pointing left  | Left  |
| Pinky pointing right  | Right  |
| Index & middle down  | Bacward  |

 - It is same for the left hand, only difference is that if thumb is up, car will go right, and if pinky is up, car will go left.
