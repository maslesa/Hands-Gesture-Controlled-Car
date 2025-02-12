#include <WiFi.h>
#include <WebSocketsClient.h>

// WiFi Credentials
const char* ssid = ""; // your WiFi ssid
const char* password = ""; // your WiFi password

// Flask WebSocket Server
const char* serverAddress = "192.168.0.20";  // Flask's server address
const int serverPort = 5000;

WebSocketsClient webSocket;

#define IN1 18
#define IN2 19
#define IN3 21
#define IN4 22
#define WIFI_LED 23

void setup() {
    Serial.begin(115200);
    pinMode(WIFI_LED, OUTPUT);
    
    // Setup Wi-Fi Connection
    WiFi.begin(ssid, password);
    Serial.print("Connecting to WiFi...");
    
    while (WiFi.status() != WL_CONNECTED) {
        digitalWrite(WIFI_LED, LOW);
        delay(500);
        Serial.print(".");
        digitalWrite(WIFI_LED, HIGH);
        delay(500);
    }
    
    Serial.println("\nConnected to WiFi!");
    digitalWrite(WIFI_LED, HIGH);

    webSocket.begin(serverAddress, serverPort, "/");
    webSocket.onEvent(webSocketEvent);
}

void loop() {
    webSocket.loop();
}

void moveCar(String command) {
    Serial.println("Command Received: " + command);

    if (command == "forward") {
        digitalWrite(IN1, HIGH);
        digitalWrite(IN2, LOW);
        digitalWrite(IN3, HIGH);
        digitalWrite(IN4, LOW);
    } 
    else if (command == "backward") {
        digitalWrite(IN1, LOW);
        digitalWrite(IN2, HIGH);
        digitalWrite(IN3, LOW);
        digitalWrite(IN4, HIGH);
    } 
    else if (command == "left") {
        digitalWrite(IN1, LOW);
        digitalWrite(IN2, HIGH);
        digitalWrite(IN3, HIGH);
        digitalWrite(IN4, LOW);
    } 
    else if (command == "right") {
        digitalWrite(IN1, HIGH);
        digitalWrite(IN2, LOW);
        digitalWrite(IN3, LOW);
        digitalWrite(IN4, HIGH);
    } 
    else {
        digitalWrite(IN1, LOW);
        digitalWrite(IN2, LOW);
        digitalWrite(IN3, LOW);
        digitalWrite(IN4, LOW);
    }
}

void webSocketEvent(WStype_t type, uint8_t *payload, size_t length) {
    switch (type) {
        case WStype_DISCONNECTED:
            Serial.println("WebSocket Disconnected!");
            digitalWrite(WIFI_LED, LOW);  
            break;

        case WStype_CONNECTED:
            Serial.println("WebSocket Connected!");
            digitalWrite(WIFI_LED, HIGH);
            webSocket.sendTXT("ESP32 Connected!");
            break;

        case WStype_TEXT:
            moveCar((char*)payload);
            break;
    }
}
