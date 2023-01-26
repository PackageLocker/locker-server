# Locker-Server
This is the back-end application for the package locker system, which is hosted on Gunicorn, a Python WSGI HTTP server, on the Raspberry Pi.

### To run the server
1. Clone the repo and install required packages `pip install -r requirements.txt`

2. (One time on each Pi) Create a database `python create_db.py`

3. Start server

```
gunicorn -b 0.0.0.0:8000 'api:create_app()'
```