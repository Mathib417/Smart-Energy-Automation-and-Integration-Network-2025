#include "spi_driver.h"

void spi_init() {
    SPI.begin();  // Initialize SPI with default settings
}

uint8_t spi_transfer(uint8_t data) {
    return SPI.transfer(data);  // Full-duplex transfer (write + read)
}
