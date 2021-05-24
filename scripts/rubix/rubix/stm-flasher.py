import sys
import os
import RPi.GPIO as GPIO
from time import sleep

if len(sys.argv) != 2:
    print("Invalid filename.")
    print("Usage: <command> BIN_FILE")
    exit(-1)

GPIO.setmode(GPIO.BCM)

GPIO.setup(4, GPIO.OUT)  # BOOT0
GPIO.setup(12, GPIO.OUT)  # Reset

# Enable BOOT0 for bootloader and reset mcu
GPIO.output(4, GPIO.HIGH)
sleep(0.1)
GPIO.output(12, GPIO.LOW)
sleep(1)
GPIO.output(12, GPIO.HIGH)
sleep(1)

FILE = sys.argv[1]


command = "dfu-util -a 0 -i 0 -s 0x08000000 -D {}".format(FILE)
print("TRY AND RUN COMMAND")
print(command)
os.system(command)

# Disable BOOT0 for bootloader and reset mcu
GPIO.output(4, GPIO.LOW)
sleep(0.1)
GPIO.output(12, GPIO.LOW)
sleep(0.1)
GPIO.output(12, GPIO.HIGH)
sleep(0.1)

GPIO.cleanup()
