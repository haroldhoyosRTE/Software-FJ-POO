"""Registro en archivos de eventos y errores relevantes."""
import logging
from pathlib import Path


def obtener_logger():
    """Crea un logger único para evitar registros duplicados."""
    logger = logging.getLogger('software_fj')
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        carpeta = Path(__file__).resolve().parent / 'logs'
        carpeta.mkdir(exist_ok=True)
        destino = logging.FileHandler(carpeta / 'software_fj.log', encoding='utf-8')
        destino.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(message)s'))
        logger.addHandler(destino)
    return logger

logger = obtener_logger()
