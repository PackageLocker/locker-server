# Locker-Server
This is the back-end application for the package locker system, which is hosted on Gunicorn, a Python WSGI HTTP server, on the Raspberry Pi.

### To run the server
1. Clone the repo and install required packages `pip install -r requirements.txt`

2. Start server

```
gunicorn -w 3 -b 0.0.0.0:8000 'api:create_app()'
```