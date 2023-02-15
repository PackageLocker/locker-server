from mfrc522 import SimpleMFRC522
import sqlite3
import locker


def main():
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
                    locker.unlock(locker_id)
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
            print("something went wrong in locker_service...")
            print(e)
            break


if __name__ == "__main__":
    main()
