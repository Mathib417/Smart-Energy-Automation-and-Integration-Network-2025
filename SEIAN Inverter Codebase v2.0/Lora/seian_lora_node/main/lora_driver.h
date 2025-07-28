#ifndef LORA_DRIVER_H
#define LORA_DRIVER_H

#include <Arduino.h>

#define LORA_NSS_PIN  5   // Set your GPIO for NSS (CS)
#define LORA_SYNC_WORD 0x02
#define REG_SYNC_WORD  0x39

void lora_init();
void lora_write_reg(uint8_t addr, uint8_t value);
uint8_t lora_read_reg(uint8_t addr);

#endif // LORA_DRIVER_H
