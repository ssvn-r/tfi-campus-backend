"""Genera los PDF del campus de demostración, sin dependencias.

Por qué se generan y no viajan en el repositorio
------------------------------------------------
Los documentos de prueba —programas de materia, cronogramas, apuntes, guías de
trabajos prácticos— son **contenido de ejemplo**, no código. Guardarlos como
binarios dejaría medio centenar de archivos en el historial de Git, y el
historial de Git no se puede adelgazar después.

Acá se arman en el momento, se suben a Cloudflare R2 como cualquier archivo del
campus y la ficha queda en Firestore (ver `servicios/almacenamiento.py`). El
repositorio queda con el texto que los produce, que es lo que se revisa.

Un PDF a mano, en treinta líneas
--------------------------------
Un PDF es un catálogo que apunta a una lista de páginas, y cada página a un
flujo de instrucciones de dibujo. Escribirlo directo evita sumar una
dependencia (`reportlab` pesa más que todo el backend) para armar documentos
de cuatro párrafos.

Se usa Helvetica, que es una de las catorce tipografías que **todo** visor de
PDF trae: así no hay que incrustar ninguna. El texto va en WinAnsi (cp1252),
que cubre el castellano entero; lo que no entre se reemplaza y no rompe el
documento.

El ancho de cada carácter sale de la tabla de métricas de Helvetica, en
milésimas de punto. Sin eso no se puede cortar un párrafo en líneas: habría que
suponer todos los caracteres iguales y una línea de «mmm» se saldría de la
hoja.
"""

from __future__ import annotations

import zlib
from typing import Iterable

# ===================== La hoja =====================
# A4 en puntos (72 por pulgada), que es la unidad del PDF.
ANCHO, ALTO = 595.28, 841.89
MARGEN = 56.0
ANCHO_UTIL = ANCHO - 2 * MARGEN

# ===================== Métricas de Helvetica =====================
# En milésimas de punto, como las publica el archivo AFM de la tipografía.
_COMUNES = {
    " ": 278, "!": 278, '"': 355, "#": 556, "$": 556, "%": 889, "&": 667, "'": 191,
    "(": 333, ")": 333, "*": 389, "+": 584, ",": 278, "-": 333, ".": 278, "/": 278,
    ":": 278, ";": 278, "<": 584, "=": 584, ">": 584, "?": 556, "@": 1015,
    "[": 278, "\\": 278, "]": 278, "^": 469, "_": 556, "`": 333,
    "{": 334, "|": 260, "}": 334, "~": 584,
}
_NORMAL = {
    **_COMUNES,
    **{c: 556 for c in "0123456789"},
    "A": 667, "B": 667, "C": 722, "D": 722, "E": 667, "F": 611, "G": 778, "H": 722,
    "I": 278, "J": 500, "K": 667, "L": 556, "M": 833, "N": 722, "O": 778, "P": 667,
    "Q": 778, "R": 722, "S": 667, "T": 611, "U": 722, "V": 667, "W": 944, "X": 667,
    "Y": 667, "Z": 611,
    "a": 556, "b": 556, "c": 500, "d": 556, "e": 556, "f": 278, "g": 556, "h": 556,
    "i": 222, "j": 222, "k": 500, "l": 222, "m": 833, "n": 556, "o": 556, "p": 556,
    "q": 556, "r": 333, "s": 500, "t": 278, "u": 556, "v": 500, "w": 722, "x": 500,
    "y": 500, "z": 500,
}
_NEGRITA = {
    **_COMUNES,
    **{c: 556 for c in "0123456789"},
    ",": 278, ".": 278, "-": 333, ":": 333, ";": 333, "(": 333, ")": 333, "'": 238,
    "A": 722, "B": 722, "C": 722, "D": 722, "E": 667, "F": 611, "G": 778, "H": 722,
    "I": 278, "J": 556, "K": 722, "L": 611, "M": 833, "N": 722, "O": 778, "P": 667,
    "Q": 778, "R": 722, "S": 667, "T": 611, "U": 722, "V": 667, "W": 944, "X": 667,
    "Y": 667, "Z": 611,
    "a": 556, "b": 611, "c": 556, "d": 611, "e": 556, "f": 333, "g": 611, "h": 611,
    "i": 278, "j": 278, "k": 556, "l": 278, "m": 889, "n": 611, "o": 611, "p": 611,
    "q": 611, "r": 389, "s": 556, "t": 333, "u": 611, "v": 556, "w": 778, "x": 556,
    "y": 556, "z": 500,
}
# Las vocales con tilde y la eñe pesan como su letra sin acento; el resto de
# lo que pueda aparecer se estima en el ancho más común.
for _tabla in (_NORMAL, _NEGRITA):
    for _con, _sin in (
        ("á", "a"), ("é", "e"), ("í", "i"), ("ó", "o"), ("ú", "u"), ("ü", "u"), ("ñ", "n"),
        ("Á", "A"), ("É", "E"), ("Í", "I"), ("Ó", "O"), ("Ú", "U"), ("Ñ", "N"),
        ("¿", "?"), ("¡", "!"), ("°", "o"), ("º", "o"), ("ª", "a"), ("·", "."),
        ("–", "-"), ("—", "-"), ("“", '"'), ("”", '"'), ("‘", "'"), ("’", "'"),
    ):
        _tabla[_con] = _tabla[_sin]


def ancho_de(texto: str, tamano: float, negrita: bool = False) -> float:
    tabla = _NEGRITA if negrita else _NORMAL
    return sum(tabla.get(c, 556) for c in texto) * tamano / 1000.0


def partir(texto: str, tamano: float, negrita: bool = False, ancho: float = ANCHO_UTIL) -> list[str]:
    """Corta el párrafo en líneas que entran en el ancho pedido.

    Una palabra más larga que la línea entera —una dirección web, por
    ejemplo— se deja sobresalir en vez de partirla: cortar una URL al medio la
    vuelve inservible, y es peor que un renglón un poco largo.
    """
    lineas: list[str] = []
    actual = ""
    for palabra in texto.split():
        intento = f"{actual} {palabra}".strip()
        if actual and ancho_de(intento, tamano, negrita) > ancho:
            lineas.append(actual)
            actual = palabra
        else:
            actual = intento
    if actual:
        lineas.append(actual)
    return lineas or [""]


# ===================== El documento =====================
# Cada bloque es (clase, texto). Las clases dicen cómo se dibuja:
#   "titulo"   el título de la primera página
#   "bajada"   la línea gris de abajo del título
#   "seccion"  un subtítulo
#   "texto"    un párrafo
#   "lista"    un ítem con viñeta
#   "campo"    "Nombre: valor", con el nombre en negrita
#   "espacio"  un salto
ESTILOS = {
    "titulo": {"tamano": 19, "negrita": True, "antes": 0, "despues": 6, "alto": 23},
    "bajada": {"tamano": 10.5, "negrita": False, "antes": 0, "despues": 16, "alto": 14, "gris": 0.38},
    "seccion": {"tamano": 12.5, "negrita": True, "antes": 13, "despues": 5, "alto": 16},
    "texto": {"tamano": 10.5, "negrita": False, "antes": 0, "despues": 8, "alto": 14.5},
    "lista": {"tamano": 10.5, "negrita": False, "antes": 0, "despues": 4, "alto": 14.5, "sangria": 14},
    "campo": {"tamano": 10.5, "negrita": False, "antes": 0, "despues": 4, "alto": 14.5},
    "espacio": {"tamano": 10.5, "negrita": False, "antes": 0, "despues": 6, "alto": 0},
}


def _texto_pdf(texto: str) -> bytes:
    """Lo escapa y lo pasa a WinAnsi, que es lo que declara la tipografía."""
    crudo = texto.encode("cp1252", "replace")
    for viejo, nuevo in ((b"\\", b"\\\\"), (b"(", b"\\("), (b")", b"\\)")):
        crudo = crudo.replace(viejo, nuevo)
    return crudo


class _Hoja:
    """Las instrucciones de dibujo de una página, que se van acumulando."""

    def __init__(self) -> None:
        self.partes: list[bytes] = []
        self.y = ALTO - MARGEN

    def escribir(self, texto: str, x: float, tamano: float, negrita: bool, gris: float) -> None:
        fuente = b"/FN" if negrita else b"/FR"
        self.partes.append(
            b"BT " + fuente + b" %.2f Tf %.3f g 1 0 0 1 %.2f %.2f Tm (" % (tamano, gris, x, self.y)
            + _texto_pdf(texto)
            + b") Tj ET\n"
        )

    def linea(self, y: float, gris: float = 0.82) -> None:
        self.partes.append(
            b"%.3f G 0.6 w %.2f %.2f m %.2f %.2f l S\n" % (gris, MARGEN, y, ANCHO - MARGEN, y)
        )


def documento(bloques: Iterable[tuple[str, str]], pie: str | None = None) -> bytes:
    """Arma el PDF y devuelve sus bytes."""
    hojas = [_Hoja()]

    def hoja() -> _Hoja:
        return hojas[-1]

    def hay_lugar(alto: float) -> bool:
        return hoja().y - alto > MARGEN + 30

    for clase, texto in bloques:
        estilo = ESTILOS.get(clase, ESTILOS["texto"])
        gris = estilo.get("gris", 0.13)
        sangria = estilo.get("sangria", 0)
        hoja().y -= estilo["antes"]

        if clase == "espacio":
            continue

        negrita_nombre = ""
        if clase == "campo" and ": " in texto:
            negrita_nombre, texto = texto.split(": ", 1)

        ancho = ANCHO_UTIL - sangria - (ancho_de(negrita_nombre + ": ", estilo["tamano"], True) if negrita_nombre else 0)
        lineas = partir(texto, estilo["tamano"], estilo["negrita"], ancho)

        for i, linea in enumerate(lineas):
            if not hay_lugar(estilo["alto"]):
                hojas.append(_Hoja())
            x = MARGEN + sangria
            if i == 0 and clase == "lista":
                hoja().escribir("•", MARGEN, estilo["tamano"], False, 0.45)
            if i == 0 and negrita_nombre:
                hoja().escribir(f"{negrita_nombre}: ", x, estilo["tamano"], True, gris)
                x += ancho_de(f"{negrita_nombre}: ", estilo["tamano"], True)
            hoja().escribir(linea, x, estilo["tamano"], estilo["negrita"], gris)
            hoja().y -= estilo["alto"]

        hoja().y -= estilo["despues"]
        if clase == "bajada":
            hoja().linea(hoja().y + 8)

    if pie:
        for numero, h in enumerate(hojas, start=1):
            y = MARGEN - 18
            h.partes.append(
                b"BT /FR 8.50 Tf 0.50 g 1 0 0 1 %.2f %.2f Tm (" % (MARGEN, y)
                + _texto_pdf(pie)
                + b") Tj ET\n"
            )
            etiqueta = f"{numero} de {len(hojas)}"
            h.partes.append(
                b"BT /FR 8.50 Tf 0.50 g 1 0 0 1 %.2f %.2f Tm ("
                % (ANCHO - MARGEN - ancho_de(etiqueta, 8.5), y)
                + _texto_pdf(etiqueta)
                + b") Tj ET\n"
            )

    return _armar(hojas)


def _armar(hojas: list[_Hoja]) -> bytes:
    """Pega los objetos del PDF y la tabla que dice dónde empieza cada uno."""
    # 1 catálogo · 2 páginas · 3 y 4 las dos tipografías · de 5 en adelante,
    # cada página con su flujo de contenido.
    objetos: list[bytes] = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"",  # se completa abajo, cuando se sabe cuántas páginas hay
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>",
    ]

    primera = len(objetos) + 1
    ids_paginas = []
    for i, h in enumerate(hojas):
        id_pagina = primera + i * 2
        ids_paginas.append(id_pagina)
        flujo = zlib.compress(b"".join(h.partes))
        objetos.append(
            b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 %.2f %.2f] "
            b"/Resources << /Font << /FR 3 0 R /FN 4 0 R >> >> /Contents %d 0 R >>"
            % (ANCHO, ALTO, id_pagina + 1)
        )
        objetos.append(
            b"<< /Length %d /Filter /FlateDecode >>\nstream\n" % len(flujo) + flujo + b"\nendstream"
        )

    objetos[1] = b"<< /Type /Pages /Count %d /Kids [%s] >>" % (
        len(hojas),
        b" ".join(b"%d 0 R" % i for i in ids_paginas),
    )

    salida = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    posiciones = []
    for numero, cuerpo in enumerate(objetos, start=1):
        posiciones.append(len(salida))
        salida += b"%d 0 obj\n" % numero + cuerpo + b"\nendobj\n"

    inicio_tabla = len(salida)
    salida += b"xref\n0 %d\n" % (len(objetos) + 1)
    salida += b"0000000000 65535 f \n"
    for posicion in posiciones:
        salida += b"%010d 00000 n \n" % posicion
    salida += (
        b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n"
        % (len(objetos) + 1, inicio_tabla)
    )
    return bytes(salida)
