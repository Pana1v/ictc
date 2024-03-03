#include <WiFi.h>
#include <ESPAsyncWebServer.h>
#include <AsyncWebSocket.h>

const char* ssid = "Panav";
const char* password = "87654321";
float leftSpeed;
float rightSpeed;
AsyncWebServer server(80);
AsyncWebSocket ws("/ws");

void handleWebSocketEvent(AsyncWebSocket *server, AsyncWebSocketClient *client, AwsEventType type, void *arg, uint8_t *data, size_t len) {
  switch (type) {
    case WS_EVT_CONNECT:
      Serial.println("WebSocket client connected");
      break;
    case WS_EVT_DISCONNECT:
      Serial.println("WebSocket client disconnected");
      break;
    case WS_EVT_DATA:
      handleWebSocketData(data, len);
      break;
    case WS_EVT_PONG:
    case WS_EVT_ERROR:
      break;
  }
}

void handleWebSocketData(uint8_t *data, size_t len) {
  // Convert uint8_t array to string
  String jsonString = String(reinterpret_cast<char*>(data));

  // Find the position of "left_speed" in the string
  int leftPos = jsonString.indexOf("\"left_speed\":") + 13;

  // Extract the left speed substring
  String leftSpeedStr = jsonString.substring(leftPos, jsonString.indexOf(',', leftPos));

  // Find the position of "right_speed" in the string
  int rightPos = jsonString.indexOf("\"right_speed\":") + 14;

  // Extract the right speed substring
  String rightSpeedStr = jsonString.substring(rightPos, jsonString.indexOf('}', rightPos));

  // Convert the speed substrings to floats
  leftSpeed = leftSpeedStr.toFloat()/2;
  rightSpeed = rightSpeedStr.toFloat()/2;

  // Print the extracted speeds

  // Perform any additional actions with the speeds if needed
}


void setup() {
  Serial.begin(115200);

  // Connect to WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
  Serial.println(WiFi.localIP());

  // WebSocket events
  ws.onEvent(handleWebSocketEvent);

  // Add WebSocket to server
  server.addHandler(&ws);

  // Start server
  server.begin();
}
const int left =26;
const int right =27;
void loop() {

  
  Serial.printf("Received speeds: Left - %.2f, Right - %.2f\n", leftSpeed, rightSpeed);

  analogWrite(26,leftSpeed);
  // delūay(10);
  analogWrite(27,rightSpeed);
  delay(10);
  // Additional actions, if any
}
