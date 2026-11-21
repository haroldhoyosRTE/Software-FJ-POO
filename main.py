"""Simulación reproducible de operaciones válidas e inválidas."""
from excepciones import ErrorSoftwareFJ
from modelos import Cliente
from registro import logger
from reservas import GestorSoftwareFJ
from servicios import AlquilerEquipo, AsesoriaEspecializada, ReservaSala


def ejecutar_operacion(numero, etiqueta, accion):
    """Ejecuta una acción sin detener la simulación si falla."""
    try:
        resultado = accion()
    except ErrorSoftwareFJ as error:
        logger.error('Operación %s (%s): %s', numero, etiqueta, error, exc_info=True)
        print(f'{numero:02d}. ERROR CONTROLADO | {etiqueta}: {error}')
        return None
    except Exception:
        logger.exception('Error inesperado en operación %s (%s)', numero, etiqueta)
        print(f'{numero:02d}. ERROR INESPERADO | {etiqueta}; revisar logs')
        return None
    else:
        print(f'{numero:02d}. OK | {etiqueta}')
        logger.info('Operación %s completada: %s', numero, etiqueta)
        return resultado
    finally:
        logger.info('Fin de operación %s', numero)


def demostrar():
    """Ejecuta dieciocho operaciones y presenta un resumen final."""
    gestor = GestorSoftwareFJ()
    cliente = ejecutar_operacion(1, 'Cliente válido', lambda: gestor.registrar_cliente(
        Cliente('101', 'Ana Pérez', 'ana@ejemplo.com', '3001234567')))
    ejecutar_operacion(2, 'Cliente sin correo válido', lambda: gestor.registrar_cliente(
        Cliente('102', 'Luis Díaz', 'correo-invalido', '3001234567')))
    ejecutar_operacion(3, 'Cliente duplicado', lambda: gestor.registrar_cliente(
        Cliente('101', 'Otra Persona', 'otra@ejemplo.com', '3009876543')))
    sala = ejecutar_operacion(4, 'Sala válida', lambda: gestor.registrar_servicio(
        ReservaSala('S1', 'Sala de juntas', 50000, 10)))
    ejecutar_operacion(5, 'Sala con capacidad inválida', lambda: gestor.registrar_servicio(
        ReservaSala('S2', 'Sala incorrecta', 30000, -1)))
    equipo = ejecutar_operacion(6, 'Equipo válido', lambda: gestor.registrar_servicio(
        AlquilerEquipo('E1', 'Portátil', 20000, 2)))
    ejecutar_operacion(7, 'Equipo con tarifa inválida', lambda: gestor.registrar_servicio(
        AlquilerEquipo('E2', 'Proyector', 'no-numérica', 3)))
    asesoria = ejecutar_operacion(8, 'Asesoría válida', lambda: gestor.registrar_servicio(
        AsesoriaEspecializada('A1', 'Consultoría', 80000, 'Seguridad informática')))
    reserva = ejecutar_operacion(9, 'Reserva de sala exitosa', lambda: gestor.crear_reserva(
        'R1', cliente, sala, 2, asistentes=5, impuesto=19, descuento=10))
    ejecutar_operacion(10, 'Reserva con duración negativa', lambda: gestor.crear_reserva(
        'R2', cliente, sala, -3))
    ejecutar_operacion(11, 'Reserva que excede capacidad', lambda: gestor.crear_reserva(
        'R3', cliente, sala, 1, asistentes=30))
    ejecutar_operacion(12, 'Reserva de equipo exitosa', lambda: gestor.crear_reserva(
        'R4', cliente, equipo, 3, cantidad=2))
    ejecutar_operacion(13, 'Equipo sin unidades suficientes', lambda: gestor.crear_reserva(
        'R5', cliente, equipo, 2, cantidad=9))
    asesoria.cambiar_disponibilidad(False)
    ejecutar_operacion(14, 'Servicio no disponible', lambda: gestor.crear_reserva(
        'R6', cliente, asesoria, 1))
    asesoria.cambiar_disponibilidad(True)
    ejecutar_operacion(15, 'Asesoría disponible', lambda: gestor.crear_reserva(
        'R7', cliente, asesoria, 1))
    ejecutar_operacion(16, 'Confirmación de reserva', reserva.confirmar)
    ejecutar_operacion(17, 'Procesamiento de reserva', reserva.procesar)
    ejecutar_operacion(18, 'Cancelación prohibida tras procesar', reserva.cancelar)
    print(f'\nRESULTADO: {len(gestor.clientes)} cliente(s), '
          f'{len(gestor.servicios)} servicio(s), {len(gestor.reservas)} reserva(s).')
    print('Errores y eventos almacenados en logs/software_fj.log')

if __name__ == '__main__':
    demostrar()
