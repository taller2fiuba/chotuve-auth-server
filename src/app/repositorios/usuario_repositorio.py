from app.models.usuario import Usuario
from .repositorio import Repositorio

class UsuarioRepositorio(Repositorio):
    @property
    def clase(self):
        return Usuario
