[![Build Status](https://travis-ci.com/taller2fiuba/chotuve-auth-server.svg?branch=master)](https://travis-ci.com/taller2fiuba/chotuve-auth-server)
[![Coverage Status](https://coveralls.io/repos/github/taller2fiuba/chotuve-auth-server/badge.svg?branch=master)](https://coveralls.io/github/taller2fiuba/chotuve-auth-server?branch=master)

# Chotuve Auth Server

## Configuración
Toda la configuración del servidor de autenticación de Chotuve se realiza a través de variables de entorno. Aquellas variables definidas como "requeridas" deben tener un valor definido para poder iniciar el servidor y generarán un error en caso contrario.

### Básica
Las siguientes configuraciones son necesarias para la funcionalidad básica del servidor de autenticación de Chotuve.
- `DATABASE_URL`: Requerido. URL de la base de datos, en formato `esquema://usuario:clave@host:puerto/nombre_db`. Los esquemas soportados por las imágenes de Docker son `sqlite` y `postgres`. Sólo se garantiza el correcto funcionamiento con bases de datos PostgreSQL. Ejemplo: `postgres://chotuve:s3cr3t0@localhost:5432/chotuve_app`.
- `JWT_SECRET_KEY`: Clave secreta para encriptar los tokens JWT. Valor por defecto: `JWT_SECRET_KEY`.
- `PORT`: Sólo productivo. Requerido. Puerto en el cual se aceptarán conexiones.

### Seguridad

- `CHOTUVE_AUTH_ADMIN_EMAIL`: E-mail de administrador. Valor por defecto: `admin`.
- `CHOTUVE_AUTH_ADMIN_CLAVE`: Clave de administrador. Valor por defecto: `admin`.
- `IGNORAR_APP_SERVER_TOKEN`: Permite desactivar la autenticación de solicitudes provenientes del
servidor de aplicación. Si la variable no está configurada o está configurada con un valor falso,
todas las solicitudes provenientes de los servidores de aplicación serán validadas para asegurar que
provienen de un servidor habilitado (comportamiento por defecto). Si, por el contrario, 
la variable está configurada con un valor verdadero, se desactivará esta comprobación y se permitirán
solicitudes desde cualquier origen. Ejemplo: `1`. Valor por defecto: desactivada.

### Misceláneas
- `FLASK_ENV`: Opcional. Entorno de Flask a utilizar. Valor por defecto: `development`. Debe configurarse manualmente a `production` en un entorno productivo.

## Despliegue productivo

Para el despliegue productivo de la aplicación se provee un archivo `Dockerfile`. El mismo permitirá construir una imagen productiva de Docker del servidor de autenticación de Chotuve.

### Dependencias

Para el entorno productivo la única dependencia requerida es Docker. 

En caso de querer realizar una instalación sin Docker, se requieren las siguientes bibliotecas:
- Python 3.8.3
- Flask 1.1.2
- Jinja2 2.11.2
- Werkzeug 1.0.1
- requests 2.23.0
- flask-cors 3.0.8
- flask-restful 0.3.8
- flask-sqlalchemy 2.4.1
- flask-migrate 2.5.3
- psycopg2 2.8.5
- bcrypt 3.1.7
- Flask-Bcrypt 0.7.1
- PyJWT 1.7.1

### Ejemplo de despliegue productivo

En el siguiente ejemplo se lanzará una versión productiva de Chotuve Auth Server con la siguiente configuración:
- Base de datos SQLite en el archivo `/tmp/app.db`
- Aceptará conexiones en el puerto 5000.

```bash
~/chotuve-auth-server$ docker build -t chotuve-auth-server:latest .
...
Successfully tagged chotuve-auth-server:latest
~/chotuve-auth-server$ docker run \
    -e FLASK_ENV=production \
    -e DATABASE_URL="sqlite:////tmp/app.db" \
    -e PORT=5000 \
    --network="host" \
    -d \
    chotuve-auth-server:latest
b51f513fc78cc222b32226d617b689a3960e4eb5b8f6d021dd6714163c14fb8b
~/chotuve-auth-server$
```

> **IMPORTANTE**: No olvidar configurar la variable de ambiente `FLASK_ENV` en `production` para hacer el despliegue productivo.

Ahora el servidor de autenticación estará corriendo y aceptando conexiones en `http://localhost:5000`.

## Desarrollo

Todo el proyecto está dockerizado de modo de poder desarrollar sin tener que instalar ninguna dependencia adicional más que Docker y Docker Compose.

Para esto se provee un conjunto de scripts para levantar el servidor de desarrollo y simplificar algunas tareas comunes:
- `bin/dev-compose`: Wrapper para `docker-compose`. El servidor de desarrollo utiliza un archivo `docker-compose.yml` que está ubicado en `bin/chotuve_app/docker-compose.yml`. Para evitar tener que indicar explícitamente la ruta a `docker-compose` en cada invocación se provee este script. Ejecutar `bin/dev-compose` es equivalente a ejecutar `docker-compose -f bin/chotuve_app/docker-compose.yml`.
- `bin/exec-dev`: Permite ejecutar un comando dentro del contenedor de desarrollo. Útil para cuando es necesario abrir un intérprete de Python o ejecutar un script de Flask dentro del contenedor. Requiere que el contenedor de desarrollo esté iniciado.
- `bin/run-unit-tests`: Corre el *linter* y las pruebas unitarias del proyecto dentro del contenedor de desarrollo. Requiere que el contenedor de desarrollo esté iniciado.

### Iniciar el servidor de desarrollo
El servidor de desarrollo tendrá acceso al código fuente del proyecto mediante un montaje de tipo *bind*, lo cual implica que cualquier cambio que se realice sobre el código impactará directamente sobre el servidor.

```bash
~/chotuve-auth-server$ bin/dev-compose up
```

El servidor de desarrollo aceptará conexiones en `http://localhost:26080`.

Para iniciar el servidor en segundo plano o pasarle opciones extras a `docker-compose`, se pueden agregar al final de la línea de comandos, por ejemplo:

```bash
~/chotuve-auth-server$ bin/dev-compose up -d
```

### Para detener el servidor de desarrollo

Si estaba corriendo interactivamente (en una terminal) `Ctrl-C`, si estaba corriendo
en segundo plano:

```bash
~/chotuve-auth-server$ bin/dev-compose down
```

> Para detener el servidor y además borrar su base de datos, se puede ejecutar `dev-compose down -v`.

### Para correr las pruebas unitarias

```bash
~/chotuve-auth-server$ bin/run-unit-tests
```

Puede ser necesario, eventualmente, correr alguna prueba específica o correr las pruebas sin correr el *linter*. Para esto se puede abrir un `bash` dentro del contenedor y ejecutar los comandos manualmente. Por ejemplo:

```bash
~/chotuve-auth-server$ bin/exec-dev bash
root@chotuve:/var/www/app# cd src
root@chotuve:/var/www/app/src# nose2 tests.test_chat
....
----------------------------------------------------------------------
Ran 4 tests in 0.294s

OK
root@chotuve:/var/www/app/src#
```

### Para correr un comando de Flask

Para correr un comando de Flask, se debe ingresar al contenedor y ejecutar el comando dentro del mismo. Cualquier archivo creado se verá reflejado fuera del contenedor.

Por ejemplo, para correr `flask db migrate`:

```bash
~/chotuve-auth-server$ bin/exec-dev bash
root@chotuve:/var/www/app# cd src
root@chotuve:/var/www/app/src# flask db migrate
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
root@chotuve:/var/www/app/src#
```

> **NOTA**: Hay una consideración a tener en cuenta cuando algún comando crea archivos dentro del contenedor. Debido a cómo está hecha la imagen `python:3.8.3`, el usuario con el que se corren los comandos es `root`, con lo cual los archivos creados tendrán usuario y grupo `root`. La solución es simplemente cambiarles el usuario y grupo luego de crearlos.

### Para abrir un intérprete de Python dentro del contenedor de desarrollo

```bash
~/chotuve-auth-server$ bin/exec-dev bash
root@chotuve:/var/www/app# cd src
root@chotuve:/var/www/app/src# python
Python 3.8.3 (default, Jun  9 2020, 17:39:39) 
[GCC 8.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

## Base de datos

Se utiliza el ORM SQLAlchemy y Alembic para las migraciones. Para el proyecto se utilizan los *wrappers* `flask-sqlalchemy` y `flask-migrate` que lo que hacen es exportar las funcionalidades de los paquetes a través del CLI de Flask.

El servidor de autenticación fue diseñado considerando que el motor de la base de datos es PostgreSQL 12. En principio podría funcionar con otros motores pero no hay ninguna garantía de que funcione correctamente en esos casos.

### Migraciones
Cada vez que se realiza un cambio estructural en la base de datos se debe generar la correspondiente migración. Para esto, una vez modificado el modelo en código, se debe ejecutar el siguiente comando:

```bash
~/chotuve-auth-server$ bin/exec-dev bash
root@chotuve:/var/www/app# cd src
root@chotuve:/var/www/app/src# flask db migrate
...
Generating migration [...]
root@chotuve:/var/www/app/src#
```

Este comando va a generar un nuevo archivo `.py` en `src/migrations/versions` que deberá ser versionado y contendrá los cambios incrementales realizados sobre la estructura de la base.

> **NOTA**: Se debe tener especial cuidado al cambiar de branch o mergear branches con el orden en que se generaron las migraciones y el estado actual de la base de datos. Ver el apartado "Conflictos con migraciones".

Una vez que las migraciones fueron creadas correctamente, deben ser aplicadas a la base de datos de la siguiente forma:

```bash
~/chotuve-auth-server$ bin/exec-dev bash
root@chotuve:/var/www/app# cd src
root@chotuve:/var/www/app/src# flask db upgrade
...
root@chotuve:/var/www/app/src#
```

#### Conflictos con migraciones
Podría suceder que haya cambios simultáneos en dos ramas a la estructura de la base de datos. Lamentablemente, resolver estos conflictos no es una tarea tan simple como hacer `git merge`.

Alembic maneja las migraciones como si fueran una especie de lista enlazada. Cada migración (o revisión) "sabe" cuál es la versión siguiente y la versión anterior de la base de modo de poder actualizar o desactualizar la base de una versión a la otra.

En el caso en que haya conflictos de migraciones lo que termina sucediendo es que la lista diverge. Por ejemplo:
```
           v3 <[branch 1]
          /
 v1 -> v2 
          \
           v4 <[branch 2]
```

En el caso en que se genere un conflicto de este estilo, la forma de proceder es la siguiente:
- Desactualizar la base de datos hasta una versión que sea común entre los dos branches. En el caso de la figura sería desactualizar a la revisión `v2` (`flask db downgrade`).
- Borrar las migraciones posteriores a la revisión `v2` de la carpeta `src/migrations/versions`.
- Con la base en esa revisión, realizar el *merge* de los archivos `.py` de los modelos (y del resto del código si fuera necesario).
- Generar las nuevas migraciones (`flask db migrate`).
- Actualizar la base a la última versión (`flask db upgrade`).
- Versionar los cambios en migraciones.

> Otra opción es eliminar la base de datos y volver a crearla. En ese caso debe primero hay que 
borrar las migraciones divergentes, luego borrar la base, volver a crearla y luego generar las 
nuevas migraciones.

## Pruebas de aceptación

Este proyecto cuenta con pruebas de aceptación utilizando `behave`. Para correr las pruebas ver su documentación en [el repositorio de pruebas](https://github.com/taller2fiuba/chotuve-integration-tests).

Para simplificar las pruebas de aceptación se provee un archivo `docker-compose.yml` en la raíz del repositorio que permite levantar una imagen semi-productiva del proyecto y una base de datos PostgreSQL para el mismo.

Este archivo se puede utilizar también para levantar una versión productiva del servidor y la base de datos en una misma máquina, haciéndole algunos cambios a las variables de entorno.

Para que este archivo `docker-compose.yml` pueda funcionar correctamente se asume la existencia de una red de Docker denominada `chotuve` que permite conectar todos los servidores entre sí. 

En caso de que esta red no exista se puede crear con el siguiente comando:

```bash
$ docker network create -d bridge chotuve
```

No es necesario crear la red de Docker para correr las pruebas de aceptación, el script que corre las pruebas se encargará de crearla si no existiera.

## Integración continua

Se utiliza Travis CI como servidor de integración continua y despliegue automático a Heroku, bajo la siguiente configuración:
- En todas las ramas se corren las pruebas unitarias en cada commit.
- En los PR se corren las pruebas unitarias y además las pruebas de aceptación. Es necesario que el PR tenga una aprobación y que pase las pruebas **unitarias** para poder mergearlo a `master`.
- En `master` se corren las pruebas unitarias y de aceptación, y en caso de que todas las pruebas pasen se hace un deploy automático a Heroku.
