% prepara el repositorio para su despliegue. 
release: cd followgic && python manage.py migrate
% especifica el comando para lanzar Decide
% web: cd followgic && gunicorn followgic.wsgi --log-file -
web: cd followgic && daphne followgic.asgi:channel_layer --port $PORT --bind 0.0.0.0 -v2