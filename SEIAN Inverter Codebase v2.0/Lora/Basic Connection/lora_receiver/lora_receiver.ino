#include <SPI.h>
#include <LoRa.h>

// LoRa pin mapping (RA-02 with NodeMCU)
#define SS    4   // GPIO4
#define RST   5   // GPIO5
#define DIO0  16  // GPIO16

void setup() {
  Serial.begin(9600);
  while (!Serial);

  LoRa.setPins(SS, RST, DIO0);

  if (!LoRa.begin(433E6)) {
    Serial.println("LoRa init failed. Check wiring.");
    while (1);
  }

  LoRa.setSyncWord(0x02);  // Must match Pi

  Serial.println("LoRa receiver ready.");
}

void loop() {
  int packetSize = LoRa.parsePacket();
  if (packetSize) {
    String received = "";
    while (LoRa.available()) {
      received += (char)LoRa.read();
    }
    Serial.print("Received: ");
    Serial.println(received);
  }
}
