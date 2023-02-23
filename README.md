# Locker-Server
This is the back-end application for the package locker system, which is hosted on Gunicorn, a Python WSGI HTTP server, on the Raspberry Pi.

## Raspberry Pi Setup
Follow this [blog](https://pimylifeup.com/raspberry-pi-rfid-rc522/) to set up the RC522 RFID reader.

## To run the server
1. Clone the repo and install required packages `pip install -r requirements.txt`

2. (One time on each Pi) Create a database `python create_db.py`, set up environment variables `LOCKER_SECRET_KEY` and `EMAIL_KEY`

3. Start server (OS specific)

    a. For OS X/Linux
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

## Run Server on Startup
1. Create a server service with the following command and content
	```
	sudo nano /lib/systemd/system/locker-server.service
	```

	```
	[Unit]
	Description=Locker Server Service
	After=multi-user.target

	[Service]
	User=pi
	Environment="LOCKER_SECRET_KEY=<key>"
	Environment="EMAIL_KEY=<key>"
	WorkingDirectory=/home/pi/locker-server
	ExecStart=/home/pi/.local/bin/gunicorn -w 3 -b 127.0.0.1:8000 'api:create_app()'
	Restart=always

	[Install]
	WantedBy=multi-user.target
	```

2. Reload all services
	```
	sudo systemctl daemon-reload
	```

3. Enable service on startup
	```
	sudo systemctl enable locker-server.service
	```

4. Repeat the steps for a scanner service
	```
	sudo nano /lib/systemd/system/locker-scanner.service
	```

	```
	[Unit]
	Description=Locker Scanner Service
	After=multi-user.target
    Restart=always

	[Service]
	User=pi
	WorkingDirectory=/home/pi/locker-server
	ExecStart=/usr/bin/python locker_service.py
	Restart=always

	[Install]
	WantedBy=multi-user.target
	```

	```
	sudo systemctl daemon-reload
	sudo systemctl enable locker-scanner.service
	```

### Useful Debug Commands
- Start/Stop a service
	```
	sudo systemctl start locker-server.service
	sudo systemctl stop locker-server.service
	```
- Check service status
	```
	systemctl -l status locker-server.service
	journalctl -u locker-server -n 20
	```