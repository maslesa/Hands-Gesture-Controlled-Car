# 🚗 Hand Gesture Controlled Car with ESP32 & WebSockets

This project allows you to control a car using hand gestures via MediaPipe on a Python Flask WebSocket server, which sends movement commands to an ESP32 microcontroller.

## 📌 Features

 - 🖐 Hand Gesture Recognition using OpenCV & MediaPipe

 - 🌐 WebSocket Communication between Python server and ESP32

 - 🚗 Real-time Car Movement using an L298N motor driver

 - 📡 WiFi Connectivity to link ESP32 with the server

## Hand Gesture Commands (right hand)
| Gesture  | Action |
| ------------- | ------------- |
| All fingers up  | Stop  |
| Index & middle up  | Forward  |
| Thumb pointing left  | Left  |
| Pinky pointing right  | Right  |
| Index & middle down  | Bacward  |

 - It is same for the left hand, only difference is that if thumb is up, car will go right, and if pinky is up, car will go left.
