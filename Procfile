web: gunicorn --bind 0.0.0.0:$PORT --worker-class=gevent --worker-connections=1000 --workers=2 people.wsgi
celery: celery -A people worker -l info