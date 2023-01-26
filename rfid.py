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
        locker_id = res.fetchone()
        if (locker_id):
            print("locker_id found: " + locker_id)
            # unlock locker
            print("unlocking locker #" + locker_id)
            GPIO.output(locker_gpio[locker_id], GPIO.HIGH)
            sleep(1)
            GPIO.output(locker_gpio[locker_id], GPIO.LOW)
            # delete record in db
            cursor.execute(
                "delete from packages where student_id = '" + str(id) + "'")
            connection.commit()
        else:
            print("locker_id not found!")
    except Exception as e:
        print("something went wrong...")
        print(e)
        break

GPIO.cleanup()