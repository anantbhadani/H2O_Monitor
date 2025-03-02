#include <WiFiManager.h>    // WiFi Auto-Connect
#include <OneWire.h>        // For DS18B20 Temperature Sensor
#include <DallasTemperature.h>
#include <WiFi.h>
#include <HTTPClient.h>

// WiFiManager instance
WiFiManager wm;

// WiFi and Server Details
const char* server_host = "192.168.0.105"; // Change to your server's IP
const int server_port = 5000;              // Port your server runs on
const String endpoint = "/api/data";       // API endpoint

// Pin Definitions
#define TDS_PIN 32          // GPIO32 for TDS Sensor
#define ONE_WIRE_BUS 4      // GPIO4 for DS18B20 Temperature Sensor
#define BUTTON_STOP 13      // GPIO13 for Stop Button

// TDS Calibration Factor
const float TDS_CALIBRATION = 0.5;

// OneWire instance & Temperature sensor object
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

// Global flag to stop execution
bool stopExecution = false;

void setup() {
    Serial.begin(115200);
    pinMode(BUTTON_STOP, INPUT_PULLUP); // Set button pin as input with pull-up

    Serial.println("\nStarting ESP32...");

    // Reset saved WiFi credentials if button is held at startup
    if (digitalRead(BUTTON_STOP) == LOW) {
        Serial.println("Resetting WiFi settings...");
        wm.resetSettings();  // Clears saved WiFi credentials
        ESP.restart();
    }

    // WiFi Auto-Connect (Creates an AP if no WiFi is saved)
    if (!wm.autoConnect("ESP32-Setup", "password123")) {
        Serial.println("Failed to connect. Restarting...");
        ESP.restart();
    }

    Serial.println("Connected to WiFi!");
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());

    // Initialize Temperature Sensor
    sensors.begin();
}

void loop() {
    // Stop execution if the button is pressed
    if (digitalRead(BUTTON_STOP) == LOW) {
        Serial.println("Stopping execution...");
        while (true);  // Halt the ESP32
    }

    // Read TDS Sensor Value
    int tdsRaw = analogRead(TDS_PIN);
    float tdsValue = (tdsRaw > 10) ? tdsRaw * TDS_CALIBRATION : 0.0; // If TDS is too low, set it to 0

    // Read Temperature Sensor
    sensors.requestTemperatures();
    float temperature = sensors.getTempCByIndex(0);
    if (temperature == -127.00) {
        temperature = 0.0; // Set temperature to 0 if sensor is not connected
    }

    // Print Data to Serial Monitor
    Serial.print("TDS Value: ");
    Serial.print(tdsValue);
    Serial.print(" ppm | Temperature: ");
    Serial.print(temperature);
    Serial.println(" °C");

    // Send Data to the Server
    sendDataToServer(tdsValue, temperature);

    delay(5000); // Wait 5 seconds before next reading
}

void sendDataToServer(float tds, float temp) {
    if (WiFi.status() == WL_CONNECTED) {
        HTTPClient http;
        String url = "http://" + String(server_host) + ":" + String(server_port) + endpoint;

        Serial.print("Checking server: ");
        Serial.println(url);

        // Check if server is reachable
        WiFiClient client;
        if (!client.connect(server_host, server_port)) {
            Serial.println("⚠️ Server is unreachable. Retrying in 5 seconds...");
            delay(5000);
            return;  // Skip sending data this time
        }
        client.stop();

        // If server is reachable, send data
        http.begin(url);
        http.addHeader("Content-Type", "application/json");

        // Construct JSON payload
        String payload = "{\"tds_value\": " + String(tds) + ", \"temperature\": " + String(temp) + "}";
        Serial.print("Sending Data: ");
        Serial.println(payload);

        int httpResponseCode = http.POST(payload);
        String response = http.getString();

        // Handle response
        if (httpResponseCode > 0) {
            Serial.print("✅ Server Response: ");
            Serial.println(response);
        } else {
            Serial.print("❌ Error Sending Data: ");
            Serial.println(httpResponseCode);
        }

        http.end();
    } else {
        Serial.println("⚠️ WiFi Disconnected. Attempting to reconnect...");
        WiFi.reconnect();
        delay(5000);
    }
}
