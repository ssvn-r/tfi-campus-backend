"""Las piezas que comparten los armadores del campus de demostración.

Todo lo de `app/demo/` escribe en las mismas listas de `datos.py` que usan las
rutas, así que la persistencia por diferencia lo guarda sin que nadie avise
(ver `servicios/persistencia.py`).

**Nada pisa lo que ya está.** Cada cosa se busca por su clave natural —el
correo de una persona, el código de una materia, el título de una novedad— y
se crea solo si falta. Así el sembrado se puede volver a correr sobre una base
que ya tiene campus, que es el caso real: la facultad ya venía usándolo.
"""

from __future__ import annotations

import unicodedata
from datetime import timedelta
from typing import Any, Callable

from .. import datos as d


# ===================== Fechas =====================
def dias(n: int, hora: int = 16, minuto: int = 0) -> str:
    """Una fecha a N días de hoy. Negativo es pasado."""
    momento = d.ahora() + timedelta(days=n)
    return d.iso(momento.replace(hour=hora, minute=minuto, second=0, microsecond=0))


def horas(n: float) -> str:
    """Hace N horas. Es lo que hace que el campus se vea vivo: «hace 3 h»."""
    return d.iso(d.ahora() - timedelta(hours=n))


def minutos(n: float) -> str:
    return d.iso(d.ahora() - timedelta(minutes=n))


# ===================== Comparar texto =====================
def plano(texto: Any) -> str:
    """Sin tildes ni mayúsculas, para comparar títulos sin falsos distintos."""
    crudo = unicodedata.normalize("NFKD", str(texto or ""))
    return "".join(c for c in crudo if not unicodedata.combining(c)).strip().lower()


# ===================== Alta idempotente =====================
def asegurar(
    lista: list[dict],
    igual: Callable[[dict], bool],
    armar: Callable[[], dict],
) -> tuple[dict, bool]:
    """Devuelve el registro que cumple `igual`, o lo crea con `armar`.

    El segundo valor dice si se creó: lo usa el resumen final para informar
    qué agregó esta corrida y qué ya estaba.
    """
    existente = next((x for x in lista if igual(x)), None)
    if existente is not None:
        return existente, False
    nuevo = armar()
    lista.append(nuevo)
    return nuevo, True


class Cuenta:
    """Cuántos registros se crearon, por colección, para el resumen."""

    def __init__(self) -> None:
        self.creados: dict[str, int] = {}
        self.existian: dict[str, int] = {}

    def anotar(self, que: str, creado: bool) -> None:
        destino = self.creados if creado else self.existian
        destino[que] = destino.get(que, 0) + 1

    def sumar(self, que: str, cuantos: int) -> None:
        self.creados[que] = self.creados.get(que, 0) + cuantos

    def resumen(self) -> str:
        if not self.creados:
            return "  (no hizo falta crear nada: ya estaba todo)"
        lineas = []
        for que in sorted(self.creados):
            ya = self.existian.get(que, 0)
            cola = f"  ({ya} ya estaban)" if ya else ""
            lineas.append(f"  {que:34} +{self.creados[que]}{cola}")
        return "\n".join(lineas)


# ===================== Búsquedas que se repiten =====================
def materia_por_codigo(codigo: str) -> dict | None:
    return next((m for m in d.materias_plan if m.get("codigo") == codigo), None)


def curso_de_codigo(codigo: str) -> dict | None:
    """El módulo de esa materia, si la materia ya tiene uno abierto."""
    materia = materia_por_codigo(codigo)
    if not materia or not materia.get("cursoId"):
        return None
    return d.buscar_curso(materia["cursoId"])


def persona_por_correo(correo: str) -> dict | None:
    buscado = correo.strip().lower()
    return next((p for p in d.personas if (p.get("correo") or "").lower() == buscado), None)


def id_de(correo: str) -> int | None:
    persona = persona_por_correo(correo)
    return persona["id"] if persona else None
