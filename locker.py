import RPi.GPIO as GPIO
from time import sleep

# change this according to GPIO pinout (format - locker#: pin#)
LOCKER_GPIO = {
    1: 26,  # 31,
    2: 38,  # 29,
    3: 37,  # 35,
    4: 31,  # 37,
    5: 40,  # 26,
    6: 37,  # 38,
    7: 29  # 40
}


def unlock(locker_id):
    GPIO.setmode(GPIO.BOARD)
    print("unlocking locker #" + str(locker_id))
    GPIO.setup(LOCKER_GPIO[locker_id], GPIO.OUT)
    GPIO.output(LOCKER_GPIO[locker_id], GPIO.HIGH)
    sleep(2)
    GPIO.output(LOCKER_GPIO[locker_id], GPIO.LOW)
    GPIO.cleanup()
