To run the server

```
gunicorn -b 0.0.0.0:8000 'api:create_app()'
```