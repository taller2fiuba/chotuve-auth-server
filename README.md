[![Build Status](https://travis-ci.com/taller2fiuba/chotuve-auth-server.svg?branch=master)](https://travis-ci.com/taller2fiuba/chotuve-auth-server)
[![Coverage Status](https://coveralls.io/repos/github/taller2fiuba/chotuve-auth-server/badge.svg?branch=poner_linter_y_coveralls)](https://coveralls.io/github/taller2fiuba/chotuve-auth-server?branch=master)

# Chotuve Auth Server

## Dependencias:

- Docker + Docker compose

## Para correr el server de dev

```bash
$ bin/dev-compose up
```

Cualquier cambio en el sistema de archivos provocará que Flask recargue automáticamente el proyecto. Cualquier cambio en el sistema de archivos dentro del container se verá reflejado fuera del container.

Para iniciar el servidor en segundo plano o pasarle opciones extras a `docker-compose up`, se pueden agregar al final de la línea de comandos, por ejemplo:

```bash
$ bin/dev-compose up -d
```

## Para detener el server de dev

Si estaba corriendo interactivamente (en una terminal) `Ctrl-C`, si estaba corriendo
en segundo plano:

```bash
$ bin/dev-compose down
```

## Para correr los tests unitarios (requiere tener el server dev corriendo)

```bash
$ bin/run-unit-tests
```

## Para correr un comando de Flask o Python dentro del container.

```bash
$ bin/exec-dev bash
container /var/www/app # cd src
container /var/www/app/src # flask [args]
```

## Despliegue

### Sólo el servidor de Flask
Hay un `Dockerfile` en la raíz del sitio que se utiliza para hacer el despliegue productivo del servidor de Flask.

```bash
$ docker build -t chotuve-auth-server .
$ docker run -d -p 5000:80 -e PORT=80 -e DATABASE_URL="sqlite:////tmp/db.db" chotuve-auth-server
```

Se debe reemplazar `PORT` por el puerto en el que se desea que el servidor Gunicorn acepte conexiones y `DATABASE_URL` por la URL de la base de datos a utilizar. Se pueden utilizar bases de tipo *sqlite* o *PostgreSQL*. En principio se podría utilizar una base de datos de otro tipo soportado por SQLAlchemy y Arambic, pero es necesario agregar al archivo `requirements.txt` el conector adecuado.

Con eso el contenedor está corriendo y el sitio es accesible desde localhost:5000.

### Para desplegar el servidor de Flask y una base de datos PostgreSQL
Se provee un archivo `docker-compose.yml` para despliegue a través de Docker Compose. Este archivo levantará el servicio de Flask utilizando el Dockerfile mencionado anteriormente y un contenedor con una base de datos PostgreSQL. Se creará también un volumen para la persistencia de los datos de la base.

```bash
$ docker-compose build
$ docker-compose up -d
```

# Notas

Tener en consideración que el usuario "virtual" con el que corre el container es `root`, con lo cual si se crearan archivos desde adentro del container (por ejemplo corriendo `flask [algo que cree archivos]` van a quedar creados con usuario y grupo `root`, y hay que cambiarlos manualmente.

# Otras utilidades

## `bin/dev-compose`

Es un atajo a `docker-compose` para el servidor de dev. Se utiliza igual que `docker-compose`, solo que el archivo `.yml` que va a utilizar está fijo.

## `bin/exec-dev`

Es un atajo para ejecutar un comando dentro del servidor de dev que está corriendo. Tener en consideración que el comando ejecutado *siempre* se corre en la raíz del **repositorio**. Para correr un comando desde una carpeta distinta se debe correr un `bash` y luego navegar.

Casos comunes:
- `bin/exec-dev bash`: Para ejecutar un bash dentro del container
- `bin/exec-dev python`: Para abrir un intérprete de python dentro del container

## Bases de datos
Se utiliza el ORM SQLAlchemy y Alembic para las migraciones. Para el proyecto se utilizan los *wrappers* `flask-sqlalchemy` y `flask-migrate` que lo que hacen es exportar las funcionalidades de los paquetes a través del CLI de Flask.

### Migraciones
- Para inicializar la carpeta de migraciones: `flask db init`
- Para verificar el estado de la base de datos: `flask db migrate`. Este comando va a indicar si es necesario actualizarla.
- Para aplicar las actualizaciones a la base: `flask db upgrade`.
