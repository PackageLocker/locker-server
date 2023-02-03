import RPi.GPIO as GPIO
from time import sleep

# change this according to GPIO pinout (format - locker#: pin#)
LOCKER_GPIO = {
    1: 36,
    2: 38,
    3: 40
}


def gpioSetup():
    GPIO.setmode(GPIO.BOARD)
    for gpio in LOCKER_GPIO.values():
        GPIO.setup(gpio, GPIO.OUT)


def unlock(locker_id):
    print("unlocking locker #" + str(locker_id))
    GPIO.output(LOCKER_GPIO[locker_id], GPIO.HIGH)
    sleep(2)
    GPIO.output(LOCKER_GPIO[locker_id], GPIO.LOW)
