
#include <SPI.h>
#include <LoRa.h>

// Pin mapping from RA-02 to ESP32 (NodeMCU)
#define SS    4    // D2 → GPIO4
#define RST   5    // D1 → GPIO5
#define DIO0  16   // D0 → GPIO16

void setup() {
  Serial.begin(9600);
  while (!Serial);  // Wait for Serial Monitor (if needed)

  LoRa.setPins(SS, RST, DIO0);

  if (!LoRa.begin(433E6)) {
    Serial.println("LoRa init failed. Check wiring.");
    while (true); // Halt
  }

  Serial.println("LoRa init succeeded.");
}

void loop() {
  String message = "Voltage: 230.0, Frequency: 50.0";
  Serial.println("Sending: " + message);

  LoRa.beginPacket();
  LoRa.print(message);
  LoRa.endPacket();

  delay(5000);  // Wait 5 seconds before next send
}
