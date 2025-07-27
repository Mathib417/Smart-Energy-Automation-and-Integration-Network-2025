#ifndef SPI_DRIVER_H
#define SPI_DRIVER_H

#include <Arduino.h>
#include <SPI.h>

uint8_t spi_transfer(uint8_t data);
void spi_init();

#endif // SPI_DRIVER_H
