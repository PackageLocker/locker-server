import RPi.GPIO as GPIO
from time import sleep

# change this according to GPIO pinout (format - locker#: pin#)
LOCKER_GPIO = {
    1: 36,
    2: 38,
    3: 40
}


def unlock(locker_id):
    GPIO.setmode(GPIO.BOARD)
    print("unlocking locker #" + str(locker_id))
    GPIO.setup(LOCKER_GPIO[locker_id], GPIO.OUT)
    GPIO.output(LOCKER_GPIO[locker_id], GPIO.HIGH)
    sleep(2)
    GPIO.output(LOCKER_GPIO[locker_id], GPIO.LOW)
    GPIO.cleanup()
