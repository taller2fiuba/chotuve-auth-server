# Documento de API temporal, a migrar a OPEN API SPEC

## ping: ver el estado del server
Ruta: GET /ping

Respuesta: 200

## usuario
### Get: obtener email de usuario_id
Ruta: GET /usuario/<usuario_id>

Repuestas:

- En caso de exito: CODE 200 BODY {email: email}
- Si no existe usuario con ese id: CODE 404

### Post: registrar un nuevo usuario
Ruta: POST /usuario BODY email, password

Repuestas:

- En caso de exito: CODE 201 BODY {auth_token: auth_token}
- Mail ya registrado: CODE 400 BODY {errores: email: error_string}

## sesion
### Get: validar el token de sesion
Ruta: GET /usuario/sesion HEADER Authorization: Bearer <token>

Repuestas:

- En caso de exito: CODE 200 BODY {usuario_id: usuario_id}
- Si no se envio token o es invalido o caducado: CODE 401

### Post: iniciar sesion
Ruta: POST /usuario/sesion BODY email, password

Repuestas:

- En caso de exito: CODE 200 BODY auth_token
- Mail o contraseña incorrectos: CODE 400 BODY {mensaje: error_string}
