"""El material de cada materia, con sus archivos y su cola de revisión.

La biblioteca arranca vacía a propósito: lo que hay adentro lo puso alguien.
Acá se pone eso mismo, por el camino de siempre —material de cátedra publicado
directo, aporte de estudiante esperando revisión—, para que las cuatro
pestañas del apartado tengan de qué hablar: catálogo, guardados, mis aportes y
la cola de quien modera.
"""

from __future__ import annotations

from .. import datos as d
from . import archivos, catalogo, comun

# Qué material se carga en cada materia que se muestra a fondo.
# (tipo, categoría, título, de quién es: "catedra" o el correo de quien aporta)
PLANTILLA = [
    ("apunte", "apuntes-y-resumenes", "Apunte integrador de la cátedra", "catedra"),
    ("guia", "guias-y-ejercicios", "Guía de ejercicios resueltos", "catedra"),
    ("resumen", "apuntes-y-resumenes", "Resumen para el primer parcial", "aporte"),
]

MATERIAS = ["SIS-102", "SIS-103", "SIS-105", "PROG-2", "ALG-2", "BD-1"]


def _bloques(materia: dict, ficha: dict, titulo: str) -> list[tuple[str, str]]:
    bloques = [
        ("titulo", f"{titulo} · {materia['nombre']}"),
        ("bajada", "Biblioteca del campus · material de la materia"),
        ("texto", ficha["resumen"]),
        ("seccion", "Contenido"),
    ]
    for numero, unidad in enumerate(ficha["unidades"], start=1):
        bloques.append(("lista", f"Unidad {numero}. {unidad}"))
    bloques += [
        ("seccion", "Cómo usarlo"),
        ("texto",
         "El material sigue el orden del programa. Cada unidad tiene primero las ideas "
         "centrales y después los ejercicios resueltos paso a paso; conviene intentar el "
         "ejercicio antes de leer la resolución, porque leer una resolución correcta da la "
         "sensación de haber entendido sin que eso haya pasado."),
        ("seccion", "Bibliografía"),
    ]
    for libro in ficha["biblio"]:
        bloques.append(("lista", libro))
    return bloques


def armar(cuenta: comun.Cuenta) -> None:
    for codigo in MATERIAS:
        materia = comun.materia_por_codigo(codigo)
        ficha = catalogo.CATALOGO.get(codigo)
        curso = comun.curso_de_codigo(codigo)
        if not materia or not ficha or not curso:
            continue
        docente_id = curso.get("docenteId")
        alumnos = [p for p in d.participantes_de_curso(curso) if p["id"] != docente_id]

        for tipo, categoria, titulo, de_quien in PLANTILLA:
            de_catedra = de_quien == "catedra"
            if not de_catedra and not alumnos:
                continue
            quien = d.buscar_persona(docente_id) if de_catedra else alumnos[0]
            if not quien:
                continue

            existente = next(
                (m for m in d.materiales
                 if m.get("materiaId") == materia["id"]
                 and comun.plano(m.get("titulo")) == comun.plano(titulo)),
                None,
            )
            if existente:
                cuenta.anotar("material de biblioteca", False)
                continue

            material = {
                "id": d.nuevo_id_material(),
                "titulo": titulo,
                "autor": quien["nombre"],
                "descripcion": f"{titulo} de {materia['nombre']}, con los contenidos de las "
                               f"{len(ficha['unidades'])} unidades del programa.",
                "tipo": tipo,
                "materiaId": materia["id"],
                "anio": str(d.ahora().year),
                "idioma": "es",
                "isbn": None,
                "categoria": categoria,
                "editorial": None,
                "enlace": None,
                "licencia": "Material de cátedra, uso interno",
                "portada": None,
                "archivo": None,
                "subidoPor": quien["id"],
                "estado": "aprobado" if de_catedra else "pendiente",
                "moderadoPor": quien["id"] if de_catedra else None,
                "motivo": None,
                "creado": comun.dias(-20 if de_catedra else -2),
                "actualizado": comun.dias(-20 if de_catedra else -2),
            }
            material["archivo"] = archivos.subir_pdf(
                "biblioteca", (material["id"],), f"{titulo} {codigo}",
                _bloques(materia, ficha, titulo),
                persona_id=quien["id"], registro_id=material["id"],
            )
            d.materiales.append(material)
            cuenta.anotar("material de biblioteca", True)

            if de_catedra:
                d.moderacion_biblioteca.append({
                    "id": d.nuevo_id_moderacion(),
                    "materialId": material["id"],
                    "moderadorId": quien["id"],
                    "accion": "aprobado",
                    "motivo": "Publicado por el docente de la materia",
                    "fecha": material["creado"],
                })

            # Un par de guardados, para que la pestaña no esté vacía.
            if de_catedra and alumnos:
                comun.asegurar(
                    d.favoritos_biblioteca,
                    lambda f, m=material: f.get("personaId") == alumnos[0]["id"]
                    and f.get("materialId") == m["id"],
                    lambda m=material: {
                        "id": f"{alumnos[0]['id']}_{m['id']}",
                        "personaId": alumnos[0]["id"],
                        "materialId": m["id"],
                        "fecha": comun.dias(-6),
                    },
                )
