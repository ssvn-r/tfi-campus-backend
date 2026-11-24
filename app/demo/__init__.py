"""El campus de demostración: carreras completas, contenido, novedades y foro.

Se arma en este orden, porque cada paso necesita el anterior:

    gente      las cátedras y los estudiantes
    planes     los planes de estudio, los dictados y los módulos que abren
    modulos    el contenido de cada módulo y sus trabajos
    academico  inscripciones, historial, mesas, entregas, notas y asistencia
    biblioteca el material de cada materia
    comunidad  novedades, foro, mensajes y eventos

Todo escribe en las listas de `datos.py`, así que la persistencia por
diferencia lo guarda sola. Nada pisa lo que ya está: ver `demo/comun.py`.
"""

from __future__ import annotations

from . import academico, biblioteca, comunidad, comun, gente, modulos, planes
from .. import datos as d


def armar() -> comun.Cuenta:
    cuenta = comun.Cuenta()

    por_comision = gente.armar(cuenta)
    planes.armar(cuenta)
    # Las materias nuevas abrieron módulos: hay que volver a mirar quién está
    # en cada comisión antes de inscribir a nadie.
    trabajos = modulos.armar(cuenta, por_comision)
    academico.armar(cuenta, por_comision, trabajos)
    # El contenido se cargó antes que las inscripciones, así que los módulos
    # de las carreras nuevas todavía no tenían participantes: se completa lo
    # que haya quedado colgado.
    modulos.armar(cuenta, por_comision)
    biblioteca.armar(cuenta)
    comunidad.armar(cuenta, _estudiantes())
    return cuenta


def _estudiantes() -> list[int]:
    return [p["id"] for p in d.personas if "Estudiante" in (p.get("roles") or [])]
