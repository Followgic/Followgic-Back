% release: cd followgic && python manage.py migrate
% web: daphne followgic.asgi:channel_layer --port $PORT --bind 0.0.0.0 -v2
% worker: python manage.py runworker -v2

release: cd followgic && python manage.py migrate
web: cd decifollowgicde && gunicorn followgic.wsgi --log-file -