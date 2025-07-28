#include "lora_driver.h"

void setup() {
  Serial.begin(9600);
  while (!Serial);  // Wait for serial port to connect (for native USB boards)

  Serial.println("Initializing LoRa...");
  lora_init();  // Initializes SPI, NSS pin, sync word, and sets RX mode
  Serial.println("LoRa initialized successfully.");
}

void loop() {
  // Simple test: Read RegVersion (0x42) and print it
  uint8_t version = lora_read_reg(0x42);
  Serial.print("LoRa Chip Version: 0x");
  Serial.println(version, HEX);

  delay(2000);  // Wait 2 seconds before next read
}
