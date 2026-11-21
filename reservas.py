"""Modelo Reserva y gestor con listas de memoria (sin base de datos)."""
from enum import Enum
from modelos import Cliente
from servicios import Servicio, numero_positivo
from excepciones import (ClienteDuplicadoError, DatoInvalidoError,
    OperacionNoPermitidaError, ReservaInvalidaError, ServicioNoDisponibleError)
from registro import logger

class EstadoReserva(Enum):
    PENDIENTE = 'pendiente'
    CONFIRMADA = 'confirmada'
    CANCELADA = 'cancelada'
    PROCESADA = 'procesada'

class Reserva:
    """Reserva con máquina de estados y costo calculado al crearla."""
    def __init__(self, identificador, cliente, servicio, duracion, **opciones):
        if not isinstance(identificador, str) or not identificador.strip():
            raise ReservaInvalidaError('Se necesita un ID de reserva.')
        if not isinstance(cliente, Cliente) or not isinstance(servicio, Servicio):
            raise ReservaInvalidaError('Cliente o servicio incorrecto.')
        self.identificador = identificador.strip()
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = numero_positivo(duracion, 'Duración')
        self.opciones = dict(opciones)
        self.costo = servicio.calcular_costo(self.duracion, **self.opciones)
        self.estado = EstadoReserva.PENDIENTE

    def confirmar(self):
        if self.estado is not EstadoReserva.PENDIENTE:
            raise OperacionNoPermitidaError('Solo se confirman reservas pendientes.')
        if not self.servicio.disponible:
            raise ServicioNoDisponibleError('El servicio dejó de estar disponible.')
        self.estado = EstadoReserva.CONFIRMADA
        logger.info('Reserva %s confirmada', self.identificador)

    def cancelar(self):
        if self.estado not in (EstadoReserva.PENDIENTE, EstadoReserva.CONFIRMADA):
            raise OperacionNoPermitidaError('No es posible cancelar esta reserva.')
        self.estado = EstadoReserva.CANCELADA
        logger.info('Reserva %s cancelada', self.identificador)

    def procesar(self):
        if self.estado is not EstadoReserva.CONFIRMADA:
            raise OperacionNoPermitidaError('Solo se procesan reservas confirmadas.')
        self.estado = EstadoReserva.PROCESADA
        logger.info('Reserva %s procesada', self.identificador)

    def describir(self):
        return (f'{self.identificador}: {self.cliente.nombre} | '
                f'{self.servicio.describir()} | {self.estado.value} | ${self.costo}')

class GestorSoftwareFJ:
    """Centraliza registros usando listas internas encapsuladas."""
    def __init__(self):
        self.__clientes = []
        self.__servicios = []
        self.__reservas = []

    def registrar_cliente(self, cliente):
        if not isinstance(cliente, Cliente):
            raise DatoInvalidoError('Se esperaba un objeto Cliente.')
        if any(c.identificador == cliente.identificador for c in self.__clientes):
            raise ClienteDuplicadoError('Ya existe un cliente con ese documento.')
        self.__clientes.append(cliente)
        logger.info('Cliente %s registrado', cliente.identificador)
        return cliente

    def registrar_servicio(self, servicio):
        if not isinstance(servicio, Servicio):
            raise DatoInvalidoError('Se esperaba un objeto Servicio.')
        if any(s.identificador == servicio.identificador for s in self.__servicios):
            raise DatoInvalidoError('Código de servicio repetido.')
        self.__servicios.append(servicio)
        logger.info('Servicio %s creado', servicio.identificador)
        return servicio

    def crear_reserva(self, identificador, cliente, servicio, duracion, **opciones):
        if cliente not in self.__clientes:
            raise ReservaInvalidaError('El cliente no está registrado.')
        if servicio not in self.__servicios:
            raise ReservaInvalidaError('El servicio no está registrado.')
        if any(r.identificador == identificador for r in self.__reservas):
            raise ReservaInvalidaError('Código de reserva duplicado.')
        reserva = Reserva(identificador, cliente, servicio, duracion, **opciones)
        self.__reservas.append(reserva)
        logger.info('Reserva %s creada con costo %s', reserva.identificador, reserva.costo)
        return reserva

    @property
    def clientes(self):
        return tuple(self.__clientes)

    @property
    def servicios(self):
        return tuple(self.__servicios)

    @property
    def reservas(self):
        return tuple(self.__reservas)
