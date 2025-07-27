#include "spi_driver.h"

void spi_init() {
    SPI.begin();  // Initializes SPI with default pins
}

uint8_t spi_transfer(uint8_t data) {
    return SPI.transfer(data);  // Sends and receives 1 byte over SPI
}
