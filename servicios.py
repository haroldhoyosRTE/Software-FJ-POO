"""Servicios derivados: sala, equipos y asesoría especializada."""
from abc import ABC, abstractmethod
from decimal import Decimal, InvalidOperation
from modelos import Entidad
from excepciones import DatoInvalidoError, ServicioNoDisponibleError


def numero_positivo(valor, campo, cero=False):
    """Convierte números a Decimal, encadenando fallos de conversión."""
    try:
        if isinstance(valor, bool):
            raise ValueError('No se aceptan valores booleanos')
        resultado = Decimal(str(valor))
    except (InvalidOperation, ValueError, TypeError) as error:
        raise DatoInvalidoError(f'{campo} debe ser un número.') from error
    if not resultado.is_finite() or resultado < 0 or (resultado == 0 and not cero):
        raise DatoInvalidoError(f'{campo} debe ser positivo y finito.')
    return resultado

class Servicio(Entidad, ABC):
    """Contrato de los servicios con cálculo polimórfico de costos."""
    def __init__(self, identificador, nombre, tarifa_hora, disponible=True):
        super().__init__(identificador)
        if not isinstance(nombre, str) or not nombre.strip():
            raise DatoInvalidoError('Nombre de servicio obligatorio.')
        if not isinstance(disponible, bool):
            raise DatoInvalidoError('La disponibilidad debe ser verdadera o falsa.')
        self._nombre = nombre.strip()
        self._tarifa_hora = numero_positivo(tarifa_hora, 'La tarifa')
        self._disponible = disponible

    def cambiar_disponibilidad(self, valor):
        if not isinstance(valor, bool):
            raise DatoInvalidoError('La disponibilidad debe ser booleana.')
        self._disponible = valor

    @property
    def disponible(self):
        return self._disponible

    def validar_parametros(self, duracion, **opciones):
        if not self.disponible:
            raise ServicioNoDisponibleError(f'El servicio {self._nombre} está inactivo.')
        horas = numero_positivo(duracion, 'La duración')
        if horas > 24:
            raise DatoInvalidoError('La duración no debe superar 24 horas.')
        return horas

    def aplicar_ajustes(self, subtotal, impuesto=0, descuento=0):
        impuesto = numero_positivo(impuesto, 'Impuesto', cero=True)
        descuento = numero_positivo(descuento, 'Descuento', cero=True)
        if impuesto > 100 or descuento > 100:
            raise DatoInvalidoError('Impuesto o descuento mayor al 100 %.')
        return (subtotal * (1 - descuento / 100) * (1 + impuesto / 100)).quantize(Decimal('0.01'))

    @abstractmethod
    def calcular_costo(self, duracion, impuesto=0, descuento=0, **opciones):
        """Soporta distintas llamadas con parámetros opcionales."""

class ReservaSala(Servicio):
    """Sala facturada por horas; asistentes no pueden superar capacidad."""
    def __init__(self, identificador, nombre, tarifa_hora, capacidad, disponible=True):
        super().__init__(identificador, nombre, tarifa_hora, disponible)
        if type(capacidad) is not int or capacidad < 1:
            raise DatoInvalidoError('La capacidad debe ser un entero positivo.')
        self._capacidad = capacidad

    def validar_parametros(self, duracion, **opciones):
        horas = super().validar_parametros(duracion)
        asistentes = opciones.get('asistentes', 1)
        if type(asistentes) is not int or not 1 <= asistentes <= self._capacidad:
            raise DatoInvalidoError('Número de asistentes fuera de la capacidad.')
        return horas

    def calcular_costo(self, duracion, impuesto=0, descuento=0, **opciones):
        horas = self.validar_parametros(duracion, **opciones)
        return self.aplicar_ajustes(horas * self._tarifa_hora, impuesto, descuento)

    def describir(self):
        return f'Sala {self._nombre} (capacidad: {self._capacidad})'

class AlquilerEquipo(Servicio):
    """Equipos con recargo de mantenimiento del cinco por ciento."""
    def __init__(self, identificador, nombre, tarifa_hora, unidades, disponible=True):
        super().__init__(identificador, nombre, tarifa_hora, disponible)
        if type(unidades) is not int or unidades < 1:
            raise DatoInvalidoError('Las unidades deben ser un entero positivo.')
        self._unidades = unidades

    def validar_parametros(self, duracion, **opciones):
        horas = super().validar_parametros(duracion)
        cantidad = opciones.get('cantidad', 1)
        if type(cantidad) is not int or cantidad < 1:
            raise DatoInvalidoError('La cantidad de equipos debe ser positiva.')
        if cantidad > self._unidades:
            raise ServicioNoDisponibleError('No hay suficientes equipos disponibles.')
        return horas

    def calcular_costo(self, duracion, impuesto=0, descuento=0, **opciones):
        horas = self.validar_parametros(duracion, **opciones)
        cantidad = opciones.get('cantidad', 1)
        subtotal = horas * self._tarifa_hora * cantidad * Decimal('1.05')
        return self.aplicar_ajustes(subtotal, impuesto, descuento)

    def describir(self):
        return f'Equipo {self._nombre} (unidades: {self._unidades})'

class AsesoriaEspecializada(Servicio):
    """Asesoría con costo fijo de preparación adicional."""
    def __init__(self, identificador, nombre, tarifa_hora, especialidad, disponible=True):
        super().__init__(identificador, nombre, tarifa_hora, disponible)
        if not isinstance(especialidad, str) or not especialidad.strip():
            raise DatoInvalidoError('La especialidad es obligatoria.')
        self._especialidad = especialidad.strip()

    def calcular_costo(self, duracion, impuesto=0, descuento=0, **opciones):
        horas = self.validar_parametros(duracion, **opciones)
        subtotal = horas * self._tarifa_hora + Decimal('20000')
        return self.aplicar_ajustes(subtotal, impuesto, descuento)

    def describir(self):
        return f'Asesoría {self._nombre} ({self._especialidad})'
