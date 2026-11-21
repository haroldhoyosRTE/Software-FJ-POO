"""Errores de dominio del sistema Software FJ."""

class ErrorSoftwareFJ(Exception):
    """Error esperado y controlable de la aplicación."""

class DatoInvalidoError(ErrorSoftwareFJ):
    """Entrada incorrecta de usuario o configuración."""

class ClienteDuplicadoError(ErrorSoftwareFJ):
    """La identificación ya se encuentra registrada."""

class ServicioNoDisponibleError(ErrorSoftwareFJ):
    """El servicio no puede ofrecerse actualmente."""

class ReservaInvalidaError(ErrorSoftwareFJ):
    """La reserva incumple los requisitos del sistema."""

class OperacionNoPermitidaError(ErrorSoftwareFJ):
    """La transición de estado solicitada no está permitida."""
