# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class UsuarioId(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, usuario_id: str=None):  # noqa: E501
        """UsuarioId - a model defined in Swagger

        :param usuario_id: The usuario_id of this UsuarioId.  # noqa: E501
        :type usuario_id: str
        """
        self.swagger_types = {
            'usuario_id': str
        }

        self.attribute_map = {
            'usuario_id': 'usuario_id'
        }

        self._usuario_id = usuario_id

    @classmethod
    def from_dict(cls, dikt) -> 'UsuarioId':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Usuario_id of this UsuarioId.  # noqa: E501
        :rtype: UsuarioId
        """
        return util.deserialize_model(dikt, cls)

    @property
    def usuario_id(self) -> str:
        """Gets the usuario_id of this UsuarioId.


        :return: The usuario_id of this UsuarioId.
        :rtype: str
        """
        return self._usuario_id

    @usuario_id.setter
    def usuario_id(self, usuario_id: str):
        """Sets the usuario_id of this UsuarioId.


        :param usuario_id: The usuario_id of this UsuarioId.
        :type usuario_id: str
        """
        if usuario_id is None:
            raise ValueError("Invalid value for `usuario_id`, must not be `None`")  # noqa: E501

        self._usuario_id = usuario_id