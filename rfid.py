import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import sqlite3
from time import sleep

# change this according to GPIO pinout (format - locker#: pin#)
locker_gpio = {
    1: 36,
    2: 38,
    3: 40
}

# set up GPIO
GPIO.setmode(GPIO.BOARD)
for gpio in locker_gpio.values():
    GPIO.setup(gpio, GPIO.OUT)

# set up card reader and db management
reader = SimpleMFRC522()
connection = sqlite3.connect('instance/database.db')
cursor = connection.cursor()

while True:
    try:
        # scan id
        id, text = reader.read()
        print("id: " + str(id))
        # look for id in the db
        res = cursor.execute(
            "select locker_id from packages where student_id = '" + str(id) + "'")
        locker_ids = res.fetchall()
        if (locker_ids):
            for locker_id in locker_ids:
                locker_id = locker_id[0]
                print("locker_id found: #" + str(locker_id))
                # unlock locker
                print("unlocking locker #" + str(locker_id))
                GPIO.output(locker_gpio[locker_id], GPIO.HIGH)
                sleep(1)
                GPIO.output(locker_gpio[locker_id], GPIO.LOW)
                # delete record in db
                cursor.execute(
                    "update packages " +
                    "set package_id = '', name = '', student_id = '', email = '', available=True " +
                    "where locker_id = '" + str(locker_id) + "'"
                )
                connection.commit()
                print(
                    "[" + str(id) + "] record deleted from locker#" + str(locker_id))
        else:
            print("locker_id not found!")
    except Exception as e:
        print("something went wrong...")
        print(e)
        break

GPIO.cleanup()
