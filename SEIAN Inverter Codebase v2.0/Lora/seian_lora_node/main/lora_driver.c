#include "lora_driver.h"
#include "spi_driver.h"

#define get_millis() millis()

void lora_write_reg(uint8_t addr, uint8_t value) {
    digitalWrite(LORA_NSS_PIN, LOW);
    spi_transfer(addr | 0x80);  // MSB = 1 → Write mode
    spi_transfer(value);
    digitalWrite(LORA_NSS_PIN, HIGH);
}

uint8_t lora_read_reg(uint8_t addr) {
    digitalWrite(LORA_NSS_PIN, LOW);
    spi_transfer(addr & 0x7F);  // MSB = 0 → Read mode
    uint8_t val = spi_transfer(0x00);
    digitalWrite(LORA_NSS_PIN, HIGH);
    return val;
}

void lora_init(void) {
    pinMode(LORA_NSS_PIN, OUTPUT);
    digitalWrite(LORA_NSS_PIN, HIGH);
    spi_init();

    // Set LoRa mode
    lora_write_reg(0x01, 0x80);  // LoRa mode, standby

    // Set Sync Word
    lora_write_reg(REG_SYNC_WORD, LORA_SYNC_WORD);

    // Verify sync word
    uint8_t verify = lora_read_reg(REG_SYNC_WORD);
    if (verify == LORA_SYNC_WORD) {
        // Success
    }

    // Enter continuous RX
    lora_write_reg(0x01, 0x85);  // LoRa + RX continuous mode
}
