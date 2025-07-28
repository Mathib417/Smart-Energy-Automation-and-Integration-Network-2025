import spidev
import RPi.GPIO as GPIO
import time

# Pin definitions
NSS = 8       # CE0 ? GPIO8
RESET = 25    # GPIO25
DIO0 = 4      # GPIO4 (for RX done)

# LoRa parameters
SYNC_WORD = 0x02
PAYLOAD_LENGTH = 32  # Fixed length (or set dynamically)

# SPI setup
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 5000000

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(NSS, GPIO.OUT)
GPIO.setup(RESET, GPIO.OUT)
GPIO.setup(DIO0, GPIO.IN)

def reset_lora():
    GPIO.output(RESET, GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(RESET, GPIO.HIGH)
    time.sleep(0.1)

def write_reg(addr, value):
    GPIO.output(NSS, GPIO.LOW)
    spi.xfer2([addr | 0x80, value])
    GPIO.output(NSS, GPIO.HIGH)

def read_reg(addr):
    GPIO.output(NSS, GPIO.LOW)
    val = spi.xfer2([addr & 0x7F, 0x00])[1]
    GPIO.output(NSS, GPIO.HIGH)
    return val

def setup_lora():
    reset_lora()
    write_reg(0x01, 0x80)  # LoRa mode, sleep

    # Frequency: 433 MHz
    write_reg(0x06, 0x6C)
    write_reg(0x07, 0x80)
    write_reg(0x08, 0x00)

    write_reg(0x0C, 0x23)   # LNA gain
    write_reg(0x1D, 0x72)   # ModemConfig1
    write_reg(0x1E, 0x74)   # ModemConfig2
    write_reg(0x20, 0x00)
    write_reg(0x21, 0x08)
    write_reg(0x22, PAYLOAD_LENGTH)

    # Optional: Set sync word (must match transmitter!)
    write_reg(0x39, SYNC_WORD)

    write_reg(0x01, 0x85)  # LoRa RX Continuous

    # Version check
    version = read_reg(0x42)
    print(f"LoRa chip version: 0x{version:02X}")
    if version != 0x12:
        print("? LoRa chip not responding! Check wiring or power.")
        exit(1)

def receive_packet():
    irq_flags = read_reg(0x12)
    if irq_flags & 0x40:  # RxDone
        packet_len = read_reg(0x13)
        fifo_addr = read_reg(0x10)
        write_reg(0x0D, fifo_addr)

        payload = []
        for _ in range(packet_len):
            payload.append(read_reg(0x00))

        write_reg(0x12, 0xFF)  # Clear IRQs
        return bytes(payload).decode("utf-8", errors="ignore")
    return None

# === MAIN ===
setup_lora()
print("? LoRa Receiver Ready (433 MHz, sync word 0x%02X)" % SYNC_WORD)

try:
    while True:
        dio_status = GPIO.input(DIO0)
        if dio_status:
            print("[DIO0 HIGH] Checking for packet...")
            message = receive_packet()
            if message:
                print("?? Received:", message)
        time.sleep(0.01)  # 10ms loop for better responsiveness

except KeyboardInterrupt:
    GPIO.cleanup()
    spi.close()
    print("\n?? LoRa RX stopped and cleaned up.")
