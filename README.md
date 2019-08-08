# Seed

## Install
```
pip install -r requirements.txt
```

## Run
with Flask server
```bash
flask run
```

with Gunicorn
```bash
gunicorn --workers 3 --bind 127.0.0.1:5000 wsgi:application
```