# from mfrc522 import SimpleMFRC522
import sqlite3
import locker
import gspread
from datetime import datetime

def main():
    # reader = SimpleMFRC522()
    connection = sqlite3.connect('instance/database.db')
    cursor = connection.cursor()
    while True:
        try:
            # scan id
            id, text = reader.read()
            print("id: " + str(id))

            # look for id in the db
            res = cursor.execute(
                "select * from packages where student_id = '" + str(id) + "'")
            packages = res.fetchall()

            if (packages):
                for package in packages:
                    locker_id = package[0]
                    print("locker_id found: #" + str(locker_id))
                    locker.unlock(locker_id)
                    cursor.execute(
                        "update packages " +
                        "set package_id = '', name = '', student_id = '', email = '', available=True " +
                        "where locker_id = '" + str(locker_id) + "'"
                    )
                    connection.commit()
                    print(
                        "[" + str(id) + "] record deleted from locker#" + str(locker_id))

                    # send log message to google sheet
                    wks = gspread.service_account().open("Knight Pickup Global Database").sheet1
                    wks.insert_row(values=None, index=2)
                    wks.update('A2', [[datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), package[0], "RECEIVED", package[3],
                                       package[1], package[2], package[4]]])

            else:
                print("No package found!")
        except Exception as e:
            print("something went wrong in locker_service...")
            print(e)
            break


if __name__ == "__main__":
    main()
