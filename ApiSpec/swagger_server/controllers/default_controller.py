import connexion
import six

from swagger_server.models.error_mail_registrado import ErrorMailRegistrado  # noqa: E501
from swagger_server.models.mail_usuario import MailUsuario  # noqa: E501
from swagger_server.models.mensaje_campo_invalido import MensajeCampoInvalido  # noqa: E501
from swagger_server.models.token import Token  # noqa: E501
from swagger_server.models.usuario import Usuario  # noqa: E501
from swagger_server.models.usuario_id import UsuarioId  # noqa: E501
from swagger_server import util


def base_de_datos_delete():  # noqa: E501
    """Elimina todas las tablas de la base de datos

    Elimina todas las tablas de la base de datos # noqa: E501


    :rtype: None
    """
    return 'do some magic!'


def pin_get():  # noqa: E501
    """Ping del App Server

    Permite ver el estado del servidor # noqa: E501


    :rtype: None
    """
    return 'do some magic!'


def usuario_get(usuario_id):  # noqa: E501
    """Devuelve el email del usuario correspondiente

    Dado el id de un usuario, se devuelve el email asociado al mismo # noqa: E501

    :param usuario_id: Id del usuario
    :type usuario_id: str

    :rtype: MailUsuario
    """
    return 'do some magic!'


def usuario_post(nuevo_usuario):  # noqa: E501
    """Crea un nuevo usuario

    Crea un usuario con los datos recibidos # noqa: E501

    :param nuevo_usuario: 
    :type nuevo_usuario: dict | bytes

    :rtype: Token
    """
    if connexion.request.is_json:
        nuevo_usuario = Usuario.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def usuario_sesion_get(Authorization=None):  # noqa: E501
    """Validar token de sesion

    .... # noqa: E501

    :param Authorization: Token pasado como header
    :type Authorization: str

    :rtype: MailUsuario
    """
    return 'do some magic!'


def usuario_sesion_post(usuario=None):  # noqa: E501
    """Inicio de sesion

    Dada la informacion de un usario se devuelve el token identificador del mismo # noqa: E501

    :param usuario: 
    :type usuario: dict | bytes

    :rtype: Token
    """
    if connexion.request.is_json:
        usuario = UsuarioId.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
