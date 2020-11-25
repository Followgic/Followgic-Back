# Followgic

_Aplicación de magos para magos, ¿Qué podría salir mal?._

## Comenzando 🚀

_Estas instrucciones te permitirán obtener una copia del backend proyecto en funcionamiento en tu máquina local para propósitos de desarrollo y pruebas._

### Pre-requisitos 📋

_Herramientas que necesitas para instalar el software._

```
Python -v 3.9
```

```
PostgreSQL -v 13.1 
```

### Instalación 🔧

_Explicación paso a paso de como instalar las dependencias para tener el entorno de desarrollo ejecutandose_

_Una vez instalados los pre-requisitos, bastan con instalar las dependencias del entorno de desarrollo._

```
pip install -r requirements.txt
```

## Despliegue 📦

_En esta sección explicaremos como realizar el despliegue de la aplicación de forma local._

### Despliegue local 📝

_Para poder desplegar el backend basta con ejecutar los siguientes comandos:_

_Hay que ejecutar la base de datos PostgreSQL
```
Arrancar manualmente la base de datos con pgAdmin4. 
```

_Hay que migrar la base de datos_
```
python manage.py migrate 
```

_Hay que arrancar el servidor_
```
python manage.py runserver 
```

## Autores ✒️

* **Jesús Elias Rodriguez** - *Front-end developer* - (https://github.com/jeselirod)
* **Sergio Pérez Martín** - *Back-end developer* - (https://github.com/sergioperez1998)
