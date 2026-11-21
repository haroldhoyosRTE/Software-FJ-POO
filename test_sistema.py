"""Pruebas automatizadas usando solamente la biblioteca estándar."""
import unittest
from decimal import Decimal
from excepciones import (ClienteDuplicadoError, DatoInvalidoError,
    OperacionNoPermitidaError, ReservaInvalidaError, ServicioNoDisponibleError)
from modelos import Cliente
from reservas import EstadoReserva, GestorSoftwareFJ
from servicios import AlquilerEquipo, AsesoriaEspecializada, ReservaSala

class PruebasSoftwareFJ(unittest.TestCase):
    def setUp(self):
        self.gestor = GestorSoftwareFJ()
        self.cliente = self.gestor.registrar_cliente(
            Cliente('CC1', 'Ana Pérez', 'ana@correo.co', '3001234567'))
        self.sala = self.gestor.registrar_servicio(
            ReservaSala('SAL1', 'Sala ejecutiva', 50000, 5))

    def test_cliente_rechaza_correo(self):
        with self.assertRaises(DatoInvalidoError):
            Cliente('CC2', 'Luis Pérez', 'incorrecto', '3001234567')

    def test_cliente_duplicado(self):
        with self.assertRaises(ClienteDuplicadoError):
            self.gestor.registrar_cliente(Cliente('CC1', 'Otra Persona', 'otro@correo.co', '3001234567'))

    def test_costo_con_impuesto_y_descuento(self):
        self.assertEqual(self.sala.calcular_costo(2, impuesto=19, descuento=10), Decimal('107100.00'))

    def test_exceso_capacidad(self):
        with self.assertRaises(DatoInvalidoError):
            self.gestor.crear_reserva('R1', self.cliente, self.sala, 2, asistentes=8)

    def test_tarifa_invalida_encadenada(self):
        with self.assertRaises(DatoInvalidoError) as contexto:
            AlquilerEquipo('E1', 'Portátil', 'abc', 2)
        self.assertIsNotNone(contexto.exception.__cause__)

    def test_servicio_inactivo(self):
        self.sala.cambiar_disponibilidad(False)
        with self.assertRaises(ServicioNoDisponibleError):
            self.gestor.crear_reserva('R1', self.cliente, self.sala, 2)

    def test_estados_correctos(self):
        reserva = self.gestor.crear_reserva('R1', self.cliente, self.sala, 2)
        reserva.confirmar()
        reserva.procesar()
        self.assertEqual(reserva.estado, EstadoReserva.PROCESADA)
        with self.assertRaises(OperacionNoPermitidaError):
            reserva.cancelar()

    def test_reserva_duplicada(self):
        self.gestor.crear_reserva('R1', self.cliente, self.sala, 2)
        with self.assertRaises(ReservaInvalidaError):
            self.gestor.crear_reserva('R1', self.cliente, self.sala, 2)

    def test_equipo_costos_y_cantidad(self):
        equipo = self.gestor.registrar_servicio(AlquilerEquipo('E1', 'Portátil', 10000, 2))
        reserva = self.gestor.crear_reserva('R1', self.cliente, equipo, 2, cantidad=2)
        self.assertEqual(reserva.costo, Decimal('42000.00'))
        with self.assertRaises(ServicioNoDisponibleError):
            self.gestor.crear_reserva('R2', self.cliente, equipo, 1, cantidad=3)

    def test_asesoria_costo(self):
        asesoria = AsesoriaEspecializada('A1', 'Consultoría', 50000, 'Sistemas')
        self.assertEqual(asesoria.calcular_costo(2), Decimal('120000.00'))

if __name__ == '__main__':
    unittest.main()
