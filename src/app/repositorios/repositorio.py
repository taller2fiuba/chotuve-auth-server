from abc import ABC

from app import db
from app.excepciones import NoExisteEntidadBuscadaException, NoHayResultadoUnicoException

class Repositorio(ABC):

    @property
    def clase(self):
        raise NotImplementedError

    def resultado_unico_obligatorio(self, clase, **kwargs):
        resultado = self.resultado_unico(clase, **kwargs)
        if not resultado:
            raise NoExisteEntidadBuscadaException()
        return resultado

    def resultado_unico(self, clase, **kwargs):
        resultado = clase.query.filter_by(**kwargs)
        if len(resultado.all()) > 1:
            raise NoHayResultadoUnicoException()
        return resultado.first()

    def buscar_unico(self, obligatorio, **kwargs):
        if obligatorio:
            return self.resultado_unico_obligatorio(self.clase, **kwargs)
        return self.resultado_unico(self.clase, **kwargs)

    def guardar(self, entidad):
        db.session.add(entidad)
        db.session.commit()
