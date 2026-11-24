"""Las carreras completas: planes, materias, dictados y quién tiene cada cátedra.

Qué estaba y qué falta
----------------------
La base tiene las tres carreras y las dieciocho comisiones, pero el plan de
estudios cargado es **uno solo**, el de Sistemas. Las otras dos carreras
existen en el listado y no tienen ni una materia: en la pantalla de Módulos no
aparecen, en Estructura se ven vacías y en el panel de control cuentan cero.

Acá se completan los otros dos planes con sus materias y correlatividades, se
le asigna a cada materia la cátedra que la dicta y se abre el módulo de cada
una. Un módulo existe desde que la institución le asigna la materia a alguien
—no desde que se anota el primer alumno—, así que asignar la cátedra es lo que
hace aparecer el módulo (ver `servicios/modulos.py`).

Las correlatividades no son de adorno
-------------------------------------
Se cargan con la condición que pide cada plan: **regular** para cursar y
**aprobada** para rendir. Es lo que después decide quién puede inscribirse a
qué, así que un plan de ejemplo sin correlatividades mostraría una pantalla de
inscripción donde todo está siempre habilitado, que es justo lo que no se
quiere mostrar.
"""

from __future__ import annotations

from .. import datos as d
from ..servicios import modulos as servicio_modulos
from . import catalogo, comun

# (código, nombre, año, cuatrimestre, cupo, carga horaria, requisitos para
# cursar, requisitos para rendir). Los requisitos se escriben por código, que
# es lo legible; se resuelven a identificadores al crearlos.
PROFESORADO = [
    ("PM-101", "Álgebra I", 1, 1, 50, 96, [], []),
    ("PM-102", "Geometría I", 1, 1, 50, 96, [], []),
    ("PM-103", "Introducción al Análisis Matemático", 1, 1, 50, 128, [], []),
    ("PM-104", "Pedagogía", 1, 2, 60, 64, [], []),
    ("PM-105", "Álgebra II", 1, 2, 45, 96, [("PM-101", "Regular")], [("PM-101", "Aprobada")]),
    ("PM-201", "Análisis Matemático I", 2, 1, 45, 128,
     [("PM-103", "Regular")], [("PM-103", "Aprobada")]),
    ("PM-202", "Geometría II", 2, 1, 45, 96, [("PM-102", "Regular")], [("PM-102", "Aprobada")]),
    ("PM-203", "Didáctica de la Matemática I", 2, 1, 40, 96,
     [("PM-104", "Regular")], [("PM-104", "Aprobada")]),
    ("PM-204", "Probabilidad y Estadística", 2, 2, 45, 96, [("PM-103", "Regular")], []),
    ("PM-301", "Análisis Matemático II", 3, 1, 40, 128,
     [("PM-201", "Regular")], [("PM-201", "Aprobada")]),
    ("PM-302", "Didáctica de la Matemática II", 3, 1, 35, 96,
     [("PM-203", "Aprobada")], [("PM-203", "Aprobada")]),
    ("PM-303", "Práctica Profesional Docente", 3, 2, 25, 160,
     [("PM-203", "Aprobada"), ("PM-202", "Regular")], [("PM-302", "Aprobada")]),
]

QUIMICA = [
    ("QUI-101", "Química General e Inorgánica", 1, 1, 70, 160, [], []),
    ("QUI-102", "Matemática I", 1, 1, 70, 96, [], []),
    ("QUI-103", "Física I", 1, 1, 70, 128, [], []),
    ("QUI-104", "Química Inorgánica", 1, 2, 60, 128,
     [("QUI-101", "Regular")], [("QUI-101", "Aprobada")]),
    ("QUI-105", "Introducción a la Química Analítica", 1, 2, 60, 128,
     [("QUI-101", "Regular")], [("QUI-101", "Aprobada")]),
    ("QUI-201", "Química Orgánica I", 2, 1, 50, 160,
     [("QUI-104", "Regular")], [("QUI-104", "Aprobada")]),
    ("QUI-202", "Química Analítica I", 2, 1, 50, 160,
     [("QUI-105", "Regular")], [("QUI-105", "Aprobada")]),
    ("QUI-203", "Fisicoquímica I", 2, 1, 50, 128,
     [("QUI-103", "Regular"), ("QUI-102", "Regular")], [("QUI-103", "Aprobada")]),
    ("QUI-204", "Química Orgánica II", 2, 2, 45, 160,
     [("QUI-201", "Regular")], [("QUI-201", "Aprobada")]),
    ("QUI-301", "Bioquímica", 3, 1, 40, 128,
     [("QUI-204", "Regular")], [("QUI-204", "Aprobada")]),
    ("QUI-302", "Química Industrial", 3, 2, 40, 96,
     [("QUI-203", "Regular")], [("QUI-203", "Aprobada")]),
]

# Qué comisión dicta cada año, por carrera. Son las que ya están en la base:
# dos por año y por carrera, y el dictado se carga en la de la noche, que es la
# que tiene cursada completa.
COMISION_DEL_ANIO = {
    2: {1: 7, 2: 9, 3: 11},   # Profesorado en Matemática
    3: {1: 13, 2: 15, 3: 17},  # Licenciatura en Ciencias Químicas
}


def _requisitos(pares: list[tuple[str, str]], codigos: dict[str, int]) -> dict:
    return {
        "modo": "todas",
        "requisitos": [
            {"materiaId": codigos[codigo], "condicion": condicion}
            for codigo, condicion in pares
            if codigo in codigos
        ],
    }


def _asegurar_plan(carrera_id: int, nombre: str, anio: int) -> dict:
    plan, _ = comun.asegurar(
        d.planes_estudio,
        lambda p: p.get("carreraId") == carrera_id and p.get("nombre") == nombre,
        lambda: {
            "id": d.nuevo_id_plan(),
            "carreraId": carrera_id,
            "nombre": nombre,
            "anio": anio,
            "activo": True,
            "creado": comun.dias(-420),
        },
    )
    return plan


def _asegurar_materia(
    definicion: tuple, carrera_id: int, plan_id: int, codigos: dict[str, int], cuenta: comun.Cuenta
) -> dict:
    codigo, nombre, anio, cuatrimestre, cupo, carga, cursar, rendir = definicion
    ficha = catalogo.CATALOGO.get(codigo, {})

    def armar() -> dict:
        return {
            "id": d.nuevo_id_materia(),
            "codigo": codigo,
            "nombre": nombre,
            "anio": anio,
            "cuatrimestre": cuatrimestre,
            "correlativas": {
                "cursar": _requisitos(cursar, codigos),
                "rendir": _requisitos(rendir, codigos),
            },
            "cupo": cupo,
            "cursoId": None,
            "carreraId": carrera_id,
            "planId": plan_id,
            "descripcion": ficha.get("resumen"),
            "cargaHoraria": carga,
            "modalidad": "Presencial",
            "activa": True,
        }

    materia, creada = comun.asegurar(
        d.materias_plan,
        lambda m: m.get("codigo") == codigo and m.get("planId") == plan_id,
        armar,
    )
    cuenta.anotar("materias del plan", creada)
    return materia


def _completar_fichas(cuenta: comun.Cuenta) -> None:
    """Le pone descripción y carga horaria a las materias que no la tienen.

    Solo rellena lo que está vacío: si alguien cargó una descripción desde
    Administración, la de acá no la pisa. Una materia sin descripción se ve
    como una ficha a medio cargar en todas las pantallas que la muestran.
    """
    # Horas por cuatrimestre según la carga semanal que figura en el horario.
    for materia in d.materias_plan:
        ficha = catalogo.CATALOGO.get(materia.get("codigo"))
        if not ficha:
            continue
        if not materia.get("descripcion"):
            materia["descripcion"] = ficha["resumen"]
            cuenta.sumar("descripciones de materias", 1)
        if not materia.get("cargaHoraria"):
            semanales = sum(
                int(hasta[:2]) - int(desde[:2]) for _dia, desde, hasta, _aula in ficha["horario"]
            )
            materia["cargaHoraria"] = max(semanales, 2) * 16
            cuenta.sumar("cargas horarias", 1)


def _asegurar_dictado(comision_id: int, materia_id: int, docente_id: int | None, horario: str | None):
    def armar() -> dict:
        return {
            "id": d.nuevo_id_dictado(),
            "comisionId": comision_id,
            "materiaId": materia_id,
            "docentes": [docente_id] if docente_id else [],
            "horario": horario,
            "creado": comun.dias(-400),
        }

    return comun.asegurar(
        d.dictados,
        lambda x: x.get("comisionId") == comision_id and x.get("materiaId") == materia_id,
        armar,
    )


DIAS = ["", "lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]


def horario_legible(ficha: dict) -> str | None:
    """«Martes y jueves de 18:00 a 21:00», a partir de los días de clase."""
    tramos = ficha.get("horario") or []
    if not tramos:
        return None
    dias = [DIAS[t[0]] for t in tramos]
    nombres = " y ".join(dias) if len(dias) < 3 else ", ".join(dias[:-1]) + " y " + dias[-1]
    desde = min(t[1] for t in tramos)
    hasta = max(t[2] for t in tramos)
    return f"{nombres.capitalize()} de {desde} a {hasta}"


def _asignar_catedras(cuenta: comun.Cuenta) -> None:
    """Pone en cada dictado el docente que dice el catálogo.

    En la base todas las materias quedaron a nombre de la misma docente, que es
    lo que pasa cuando se prueba con una sola cuenta. Un campus donde una
    persona dicta diecinueve materias no se puede mostrar: el reparto por
    cátedra es lo que hace que los permisos del docente signifiquen algo.
    """
    for materia in d.materias_plan:
        ficha = catalogo.CATALOGO.get(materia.get("codigo"))
        if not ficha:
            continue
        docente_id = comun.id_de(ficha["catedra"])
        if not docente_id:
            continue
        horario = horario_legible(ficha)
        for dictado in d.dictados:
            if dictado.get("materiaId") != materia["id"]:
                continue
            if dictado.get("docentes") != [docente_id]:
                dictado["docentes"] = [docente_id]
                cuenta.sumar("cátedras asignadas", 1)
            if not dictado.get("horario"):
                dictado["horario"] = horario


def _abrir_modulos(cuenta: comun.Cuenta) -> None:
    """Abre el módulo de cada materia que tenga cátedra asignada."""
    for materia in d.materias_plan:
        if not d.docentes_de_materia(materia["id"]):
            continue
        antes = len(d.cursos)
        servicio_modulos.modulo_para(materia)
        servicio_modulos.sincronizar_docente(materia)
        cuenta.anotar("módulos abiertos", len(d.cursos) > antes)


def armar(cuenta: comun.Cuenta) -> None:
    # --- Profesorado en Matemática ---
    plan_pm = _asegurar_plan(2, "Plan 2024", 2024)
    codigos: dict[str, int] = {}
    for definicion in PROFESORADO:
        materia = _asegurar_materia(definicion, 2, plan_pm["id"], codigos, cuenta)
        codigos[definicion[0]] = materia["id"]

    # --- Licenciatura en Ciencias Químicas ---
    # Esta carrera ya tiene un plan cargado desde Administración: se usa ese.
    plan_lcq = next(
        (p for p in d.planes_estudio if p.get("carreraId") == 3 and p.get("activo")), None
    ) or _asegurar_plan(3, "Plan 2026", 2026)
    codigos_q: dict[str, int] = {}
    for definicion in QUIMICA:
        materia = _asegurar_materia(definicion, 3, plan_lcq["id"], codigos_q, cuenta)
        codigos_q[definicion[0]] = materia["id"]

    # Las comisiones de estas dos carreras estaban sin plan: una comisión sin
    # plan no sabe qué materias dicta, y entonces entrar en ella no inscribe
    # en nada.
    for carrera_id, plan in ((2, plan_pm), (3, plan_lcq)):
        for comision in d.comisiones:
            if comision.get("carreraId") == carrera_id and not comision.get("planId"):
                comision["planId"] = plan["id"]
                cuenta.sumar("comisiones con plan", 1)

    # Los dictados de las materias nuevas, en la comisión del año que cursan.
    for carrera_id, definiciones, mapa in ((2, PROFESORADO, codigos), (3, QUIMICA, codigos_q)):
        for definicion in definiciones:
            codigo, _nombre, anio = definicion[0], definicion[1], definicion[2]
            comision_id = COMISION_DEL_ANIO[carrera_id][anio]
            ficha = catalogo.CATALOGO.get(codigo, {})
            docente_id = comun.id_de(ficha.get("catedra", ""))
            _, creado = _asegurar_dictado(
                comision_id, mapa[codigo], docente_id, horario_legible(ficha)
            )
            cuenta.anotar("dictados", creado)

    _completar_fichas(cuenta)
    _asignar_catedras(cuenta)
    _abrir_modulos(cuenta)
