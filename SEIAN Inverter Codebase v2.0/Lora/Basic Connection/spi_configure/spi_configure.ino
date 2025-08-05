#include <SPI.h>
#include <LoRa.h>

#define SS    4
#define RST   5
#define DIO0  16

void setup() {
  Serial.begin(9600);
  LoRa.setPins(SS, RST, DIO0);
  delay(100);  // Important delay

  if (!LoRa.begin(433E6)) {
    Serial.println("LoRa init failed. Check wiring.");
    while (1);
  }

  Serial.println("LoRa init succeeded.");
}

void loop() {
  // do nothing
}
