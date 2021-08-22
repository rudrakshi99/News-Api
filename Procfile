release: python3 manage.py makemigrations --no-input
release: python3 manage.py migrate --no-input

web: gunicorn NewsApi.wsgi --log-file -
worker: celery -A NewsApi worker --beat -S django --l info
