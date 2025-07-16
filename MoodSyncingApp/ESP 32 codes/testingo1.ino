#include <WiFi.h>
#include <WebServer.h>

const char* ssid = "Sasmitha 123";
const char* password = "firefox12345";

WebServer server(80);

// LED Configuration
const int ledPin = 2;  // Built-in LED (adjust if needed)
float ledIntensity = 0.5; // Default intensity

void setup() {
  Serial.begin(115200);
  pinMode(ledPin, OUTPUT);
  
  // Connect to WiFi
  WiFi.begin(ssid, password);
  Serial.println("Connecting to WiFi...");
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  // Setup server routes
  server.on("/", handleRoot);
  server.on("/test", handleTest);
  server.on("/command", handleCommand);
  
  server.begin();
  Serial.println("HTTP server started");
}

void loop() {
  server.handleClient();
  
  // Apply LED intensity with PWM (0-255)
  int pwmValue = (int)(ledIntensity * 255);
  analogWrite(ledPin, pwmValue);
}

void handleRoot() {
  String html = "<html><body>";
  html += "<h1>ESP32 Mood LED Controller</h1>";
  html += "<p>Current LED Intensity: " + String(ledIntensity) + "</p>";
  html += "<p>Send commands to /command?led=x.x where x.x is between 0.0 and 1.0</p>";
  html += "</body></html>";
  
  server.send(200, "text/html", html);
}

void handleTest() {
  server.send(200, "text/plain", "OK");
}

void handleCommand() {
  if (server.hasArg("led")) {
    float newIntensity = server.arg("led").toFloat();
    
    // Validate the input
    if (newIntensity >= 0.0 && newIntensity <= 1.0) {
      ledIntensity = newIntensity;
      server.send(200, "text/plain", "Intensity set to " + String(ledIntensity));
      Serial.println("LED intensity changed to: " + String(ledIntensity));
    } else {
      server.send(400, "text/plain", "Invalid intensity value");
    }
  } else {
    server.send(400, "text/plain", "Missing 'led' parameter");
  }
}