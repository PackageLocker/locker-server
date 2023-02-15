# Locker-Server
This is the back-end application for the package locker system, which is hosted on Gunicorn, a Python WSGI HTTP server, on the Raspberry Pi.

## Raspberry Pi Setup
Follow this [blog](https://pimylifeup.com/raspberry-pi-rfid-rc522/) to set up the RC522 RFID reader.

## To run the server
1. Clone the repo and install required packages `pip install -r requirements.txt`

2. (One time on each Pi) Create a database `python create_db.py`

3. Start server (OS specific)

    a. For OSX/Linux
    ```
    gunicorn -w 3 -b 127.0.0.1:8000 'api:create_app()'
    ```
    b. For Windows
    ```
    waitress-serve --host 127.0.0.1 --port=8000 api:create_app()
    ```

4. Run locker_service

```
python locker_service.py
```
