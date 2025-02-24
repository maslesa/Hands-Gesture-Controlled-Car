#include <WiFi.h>
#include <WebSocketsClient.h>

const char* ssid = ""; // Replace with your WiFi ssid
const char* password = ""; // Replace with your WiFi password
const char* serverAddress = ""; // Replace with your PC's IP
const int serverPort = 5000;

#define IN1 18
#define IN2 19
#define IN3 21
#define IN4 22

WebSocketsClient webSocket;

void moveCar(String command) {
    Serial.println("🚗 Command Received: " + command);

    if (command == "forward") {
        Serial.println("⬆ Moving Forward");
        digitalWrite(IN1, HIGH);
        digitalWrite(IN2, LOW);
        digitalWrite(IN3, HIGH);
        digitalWrite(IN4, LOW);
    } 
    else if (command == "backward") {
        Serial.println("⬇ Moving Backward");
        digitalWrite(IN1, LOW);
        digitalWrite(IN2, HIGH);
        digitalWrite(IN3, LOW);
        digitalWrite(IN4, HIGH);
    } 
    else if (command == "left") {
        Serial.println("⬅ Turning Left");
        digitalWrite(IN1, LOW);
        digitalWrite(IN2, HIGH);
        digitalWrite(IN3, HIGH);
        digitalWrite(IN4, LOW);
    } 
    else if (command == "right") {
        Serial.println("➡ Turning Right");
        digitalWrite(IN1, HIGH);
        digitalWrite(IN2, LOW);
        digitalWrite(IN3, LOW);
        digitalWrite(IN4, HIGH);
    } 
    else {
        Serial.println("🛑 Stopping");
        digitalWrite(IN1, LOW);
        digitalWrite(IN2, LOW);
        digitalWrite(IN3, LOW);
        digitalWrite(IN4, LOW);
    }
}

void onWebSocketEvent(WStype_t type, uint8_t* payload, size_t length) {
    switch (type) {
        case WStype_CONNECTED:
            Serial.println("✅ Connected to WebSocket server!");
            break;
        case WStype_DISCONNECTED:
            Serial.println("❌ Disconnected from WebSocket server.");
            break;
        case WStype_TEXT:
            Serial.print("📩 Received command: ");
            Serial.println((char*)payload);
            moveCar(String((char*)payload));
            break;
    }
}

void setup() {
    Serial.begin(115200);

    pinMode(IN1, OUTPUT);
    pinMode(IN2, OUTPUT);
    pinMode(IN3, OUTPUT);
    pinMode(IN4, OUTPUT);

    WiFi.begin(ssid, password);

    Serial.print("Connecting to WiFi");
    while (WiFi.status() != WL_CONNECTED) {
        Serial.print(".");
        delay(1000);
    }
    Serial.println("\n✅ Connected to WiFi!");

    // Connect to WebSocket server
    webSocket.begin(serverAddress, serverPort, "");
    webSocket.onEvent(onWebSocketEvent);
    webSocket.setReconnectInterval(5000); // Auto-reconnect
}

void loop() {
    webSocket.loop();
    delay(10);  // Prevents disconnections
}
