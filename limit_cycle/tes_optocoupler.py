mport RPi.GPIO as GPIO
import time

PIN = 14

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        state = GPIO.input(PIN)

        if state:
            print("HIGH")
        else:
            print("LOW")

        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()
