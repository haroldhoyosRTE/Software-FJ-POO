"""Abstracción y encapsulación de entidades y clientes."""
from abc import ABC, abstractmethod
from excepciones import DatoInvalidoError

class Entidad(ABC):
    """Entidad abstracta con identidad y descripción obligatorias."""
    def __init__(self, identificador):
        if not isinstance(identificador, str) or not identificador.strip():
            raise DatoInvalidoError('La identificación es obligatoria.')
        self._identificador = identificador.strip()

    @property
    def identificador(self):
        return self._identificador

    @abstractmethod
    def describir(self):
        """Describe la entidad."""

class Cliente(Entidad):
    """Cliente cuyos datos personales se validan mediante propiedades."""
    def __init__(self, identificador, nombre, correo, telefono):
        super().__init__(identificador)
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise DatoInvalidoError('El nombre debe tener al menos tres caracteres.')
        self.__nombre = valor.strip()

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        if (not isinstance(valor, str) or valor.count('@') != 1
                or '.' not in valor.rsplit('@', 1)[-1] or ' ' in valor):
            raise DatoInvalidoError('Correo electrónico no válido.')
        self.__correo = valor.strip()

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        if not isinstance(valor, str) or not valor.isdigit() or not 7 <= len(valor) <= 15:
            raise DatoInvalidoError('El teléfono debe tener entre 7 y 15 dígitos.')
        self.__telefono = valor

    def describir(self):
        return f'Cliente {self.nombre} (documento {self.identificador})'
