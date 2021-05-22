% prepara el repositorio para su despliegue. 
release: cd followgic && python manage.py migrate
% especifica el comando para lanzar Decide
web: cd followgic && gunicorn followgic.wsgi --log-file -