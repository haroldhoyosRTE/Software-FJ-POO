# Software FJ — Sistema integral de clientes, servicios y reservas

Proyecto académico en **Python 3**, correspondiente al Ejercicio 1 de la Fase 4 de Programación Orientada a Objetos (UNAD).

## Funcionalidades
- Clientes con validación y encapsulación de datos personales.
- Servicios abstractos y tres derivados: salas, equipos y asesorías.
- Reservas con estados pendiente, confirmada, procesada y cancelada.
- Cálculo polimórfico de costos con parámetros opcionales de impuestos y descuentos (simulación de sobrecarga en Python).
- Excepciones personalizadas, encadenamiento con `raise ... from`, y bloques `try/except/else/finally`.
- Eventos y errores en `logs/software_fj.log` (se crea automáticamente; no se sube a GitHub).
- Información mantenida **solo en objetos y listas durante la ejecución**, sin base de datos.

## Cómo ejecutar
En la carpeta del proyecto, con Python 3.10 o superior:

```bash
python main.py
```

Se ejecutan **18 operaciones**, con entradas válidas e inválidas, sin interrumpir el programa.

## Ejecutar pruebas automatizadas

```bash
python -m unittest -v test_sistema.py
```

## Archivos
| Archivo | Responsabilidad |
|---|---|
| `modelos.py` | Entidad abstracta y Cliente |
| `servicios.py` | Servicio abstracto, sala, equipo y asesoría |
| `reservas.py` | Reserva y gestor con listas internas |
| `excepciones.py` | Jerarquía de excepciones propias |
| `registro.py` | Registro de eventos y errores |
| `main.py` | Simulación de 18 operaciones |
| `test_sistema.py` | Pruebas unitarias |

**Nota:** la aplicación simula reservas, sin calendario real ni bloqueo temporal de disponibilidad. Esta decisión mantiene el alcance del ejercicio sin base de datos.

## Referencias
- Python Software Foundation. (2024). *Errores y excepciones*. https://docs.python.org/es/3.12/tutorial/errors.html
- Python Software Foundation. (s. f.). *abc — Clases base abstractas*. https://docs.python.org/es/3/library/abc.html
- Python Software Foundation. (s. f.). *logging — Registro de eventos para Python*. https://docs.python.org/es/3/library/logging.html
