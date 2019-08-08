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
gunicorn --bind 127.0.0.1:5000 --workers 3 --error-logfile=- --access-logfile=- --capture-output --log-level debug wsgi:application
```