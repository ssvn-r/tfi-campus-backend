"""Sube los documentos del campus de demostración y deja su ficha.

Usa el mismo camino que la aplicación: el archivo va a Cloudflare R2 por
`servicios/almacenamiento.py` y la ficha —nombre, tipo, tamaño, quién lo subió
y a qué registro pertenece— queda en Firestore. Nada de esto es un atajo: si
funciona acá, funciona cuando lo sube un docente desde la pantalla.

**Si R2 no está configurado el campus sigue andando**: el almacenamiento cae en
su guardado en memoria y lo avisa. Los documentos quedan disponibles mientras
el servidor no se reinicie, que es exactamente lo que hace la aplicación en ese
caso. Para que los documentos de la demostración sobrevivan a un reinicio hace
falta R2.
"""

from __future__ import annotations

from .. import datos as d
from ..servicios import almacenamiento as alm
from ..servicios import archivos as servicio_archivos
from . import comun, documentos

PIE = "CampusTFI · FaCENA – UNNE · documento de ejemplo del campus de demostración"


def subir_pdf(
    modulo: str,
    partes: tuple,
    nombre: str,
    bloques: list[tuple[str, str]],
    *,
    persona_id: int | None,
    registro_id=None,
) -> dict:
    """Arma el PDF, lo sube y devuelve la ficha que se guarda en el registro.

    Si el objeto ya tiene ficha no se vuelve a subir: el sembrado se puede
    repetir sin duplicar archivos ni pagar la subida dos veces.
    """
    limpio = servicio_archivos.nombre_seguro(nombre, "pdf")
    objeto = alm.clave(modulo, *partes, nombre=limpio)

    existente = alm.ficha_de(objeto)
    if existente:
        return {
            "nombre": existente.get("nombre") or limpio,
            "tamano": existente.get("tamano") or 0,
            "tipo": "application/pdf",
            "objectKey": objeto,
        }

    contenido = documentos.documento(bloques, pie=PIE)
    alm.subir(objeto, contenido, "application/pdf")
    alm.registrar(
        objeto,
        nombre=limpio,
        tipo="application/pdf",
        tamano=len(contenido),
        persona_id=persona_id,
        modulo=modulo,
        registro_id=registro_id,
    )
    return {
        "nombre": limpio,
        "tamano": len(contenido),
        "tipo": "application/pdf",
        "objectKey": objeto,
    }


def subir_imagen(
    modulo: str, partes: tuple, nombre: str, contenido: bytes, *, persona_id: int | None, registro_id=None
) -> str:
    """Lo mismo para una imagen. Devuelve la clave del objeto.

    La dirección con la que se muestra **no se guarda**: la arma quien lee, y
    por eso acá solo vuelve la clave (ver «La dirección se arma al leer» en la
    documentación del proyecto).
    """
    limpio = servicio_archivos.nombre_seguro(nombre, "png")
    objeto = alm.clave(modulo, *partes, nombre=limpio)
    if alm.ficha_de(objeto):
        return objeto

    alm.subir(objeto, contenido, "image/png")
    alm.registrar(
        objeto,
        nombre=limpio,
        tipo="image/png",
        tamano=len(contenido),
        persona_id=persona_id,
        modulo=modulo,
        registro_id=registro_id,
    )
    return objeto


def peso(ficha: dict) -> str:
    return servicio_archivos.peso_legible(ficha.get("tamano") or 0)


def archivos_del_campus() -> int:
    return len(d.archivos_subidos)


__all__ = ["subir_pdf", "subir_imagen", "peso", "PIE", "comun"]
