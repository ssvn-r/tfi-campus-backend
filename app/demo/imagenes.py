"""Las portadas de las novedades, generadas acá mismo.

Una novedad sin imagen cae en el ícono de megáfono, y la portada de Novedades
—que es la pantalla de inicio del campus— se ve con tres recuadros grises. Con
una portada por categoría, la pantalla se parece a lo que es: un muro.

Son PNG armados con `zlib`, sin Pillow. Un PNG es la firma, unos pocos bloques
con su CRC y los píxeles comprimidos por filas: para un degradado con bandas no
hace falta más, y sumar una dependencia de imágenes al backend por cuatro
portadas de ejemplo no se justifica.

No se usa SVG a propósito: el campus **rechaza** subir SVG porque es un
documento con scripts adentro, y esta imagen se muestra en la pantalla que ve
todo el campus. Lo que no se acepta de un docente tampoco se cuela por acá.
"""

from __future__ import annotations

import struct
import zlib

ANCHO, ALTO = 960, 540

# La paleta del campus (ver `styles/global.css`): oscuro, tinta, principal y
# gris. Cada portada combina dos, para que se distingan entre sí sin salirse
# de la identidad visual.
PALETA = {
    "inscripciones": ((43, 45, 66), (58, 61, 87), (216, 0, 50)),
    "biblioteca": ((58, 61, 87), (141, 153, 174), (237, 242, 244)),
    "campus": ((43, 45, 66), (141, 153, 174), (216, 0, 50)),
    "becas": ((216, 0, 50), (43, 45, 66), (237, 242, 244)),
    "academico": ((58, 61, 87), (43, 45, 66), (141, 153, 174)),
}


def _bloque(tipo: bytes, datos: bytes) -> bytes:
    return (
        struct.pack(">I", len(datos))
        + tipo
        + datos
        + struct.pack(">I", zlib.crc32(tipo + datos) & 0xFFFFFFFF)
    )


def _mezclar(a: tuple[int, int, int], b: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))  # type: ignore[return-value]


def portada(variante: str) -> bytes:
    """Un degradado con bandas diagonales y un acento, en PNG."""
    desde, hasta, acento = PALETA.get(variante, PALETA["academico"])

    filas = bytearray()
    for y in range(ALTO):
        base = _mezclar(desde, hasta, y / (ALTO - 1))
        fila = bytearray(b"\x00")  # filtro 0: la fila va sin predicción
        for x in range(ANCHO):
            # Bandas diagonales: suben de izquierda a derecha y se repiten
            # cada 150 píxeles. La de acento es una sola, más angosta.
            diagonal = (x + y * 0.8) % 150
            if diagonal < 6:
                color = acento
            elif diagonal < 54:
                color = _mezclar(base, hasta, 0.35)
            else:
                color = base
            # Un aclarado suave hacia la esquina de arriba a la izquierda, que
            # es donde la tarjeta apoya el texto.
            cerca = 1 - min(1.0, ((x / ANCHO) ** 2 + (y / ALTO) ** 2) ** 0.5)
            color = _mezclar(color, (255, 255, 255), 0.10 * cerca)
            fila += bytes(color)
        filas += fila

    cabecera = struct.pack(">IIBBBBB", ANCHO, ALTO, 8, 2, 0, 0, 0)  # 8 bits, color RGB
    return (
        b"\x89PNG\r\n\x1a\n"
        + _bloque(b"IHDR", cabecera)
        + _bloque(b"IDAT", zlib.compress(bytes(filas), 9))
        + _bloque(b"IEND", b"")
    )
