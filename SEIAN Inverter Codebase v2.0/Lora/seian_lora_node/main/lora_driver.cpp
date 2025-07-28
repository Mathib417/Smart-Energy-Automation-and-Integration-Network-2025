#include "lora_driver.h"
#include "spi_driver.h"

#define get_millis() millis()

void lora_write_reg(uint8_t addr, uint8_t value) {
    digitalWrite(LORA_NSS_PIN, LOW);
    spi_transfer(addr | 0x80);  // MSB = 1 for write
    spi_transfer(value);
    digitalWrite(LORA_NSS_PIN, HIGH);
}

uint8_t lora_read_reg(uint8_t addr) {
    digitalWrite(LORA_NSS_PIN, LOW);
    spi_transfer(addr & 0x7F);  // MSB = 0 for read
    uint8_t val = spi_transfer(0x00);
    digitalWrite(LORA_NSS_PIN, HIGH);
    return val;
}

void lora_init(void) {
    pinMode(LORA_NSS_PIN, OUTPUT);
    digitalWrite(LORA_NSS_PIN, HIGH);
    spi_init();

    lora_write_reg(0x01, 0x80);  // RegOpMode: LoRa + standby

    lora_write_reg(REG_SYNC_WORD, LORA_SYNC_WORD);  // Sync word

    // Optionally verify
    uint8_t verify = lora_read_reg(REG_SYNC_WORD);
    if (verify == LORA_SYNC_WORD) {
        Serial.println("LoRa sync word set OK");
    }

    lora_write_reg(0x01, 0x85);  // RegOpMode: LoRa + continuous RX
}
