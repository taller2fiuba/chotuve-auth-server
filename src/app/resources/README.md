# Documento de API temporal, a migrar a OPEN API SPEC

## ping
Ruta: GET /ping

Respuesta: 200

## usuario
### Get
Ruta: GET /usuario/<usuario_id>

Repuestas:

- En caso de exito: CODE 200 BODY {email: email}
- Si no existe usuario con ese id: CODE 404

### Post
Ruta: POST /usuario BODY email, password

Repuestas:

- En caso de exito: CODE 201 BODY {auth_token: auth_token}
- Mail ya registrado: CODE 400 BODY {errores: email: error_string}

## sesion
### Get
Ruta: GET /usuario/sesion HEADER Authorization: Bearer <token>

Repuestas:

- En caso de exito: CODE 200 BODY {usuario_id: usuario_id}
- Si no se envio token o es invalido o caducado: CODE 401

### Post
Ruta: POST /usuario/sesion BODY email, password

Repuestas:

- En caso de exito: CODE 200 BODY auth_token
- Mail o contraseña incorrectos: CODE 400 BODY {mensaje: error_string}
