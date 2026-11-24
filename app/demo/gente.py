"""La gente del campus de demostración: cátedras y estudiantes.

Por qué hace falta
------------------
Un campus con una sola docente a cargo de las diecinueve materias se lee como
lo que es: datos de prueba. Y sin estudiantes inscriptos no hay participantes,
no hay foro, no hay entregas y los tableros muestran cero. La población es la
que hace que el resto del campus tenga de qué hablar.

Las cuentas de verdad no se tocan
---------------------------------
Las cuatro personas que ya existen —Santiago, María, la Secretaría y Claudia—
son las que tienen acceso en Firebase Authentication, así que son las que se
usan para mostrar el campus. Acá no se modifican: se las busca por correo y se
las usa tal como están.

Las que se agregan son **población**: aparecen en los módulos, en el foro y en
las planillas, pero no tienen cuenta en Firebase y no entran. Eso es a
propósito: crear veinte accesos reales para una demostración sería dejar veinte
puertas abiertas. Quedan en estado `activa` porque es lo que son para el
campus; dos quedan `pendiente` para que la alerta «cuentas sin activar» del
panel tenga algo de verdad que mostrar.
"""

from __future__ import annotations

from .. import datos as d
from ..servicios import legajos
from . import comun

# ===================== Las cuentas que ya existen =====================
SANTIAGO = "santiago.sosa@campustfi.edu.ar"       # Estudiante
MARIA = "maria.gomez@campustfi.edu.ar"            # Docente
SECRETARIA = "secretaria.academica@campustfi.edu.ar"  # Administrador
CLAUDIA = "claudia.ferreyra@campustfi.edu.ar"     # Supervisor y Docente
PEDRO = "pedro.sanchez@campustfi.edu.ar"          # Estudiante

# ===================== Las cátedras =====================
# El correo es la clave: es con lo que el campus liga una cuenta de Firebase
# con una persona, y es también con lo que acá se decide si hay que crearla.
DOCENTES = [
    ("Pablo Ruiz", "pablo.ruiz@campustfi.edu.ar"),
    ("Laura Benítez", "laura.benitez@campustfi.edu.ar"),
    ("Diego Fernández", "diego.fernandez@campustfi.edu.ar"),
    ("Ana Martínez", "ana.martinez@campustfi.edu.ar"),
    ("Jorge Romero", "jorge.romero@campustfi.edu.ar"),
    ("Silvina Ojeda", "silvina.ojeda@campustfi.edu.ar"),
    ("Marcelo Ayala", "marcelo.ayala@campustfi.edu.ar"),
    ("Gabriela Insaurralde", "gabriela.insaurralde@campustfi.edu.ar"),
    ("Raúl Cabrera", "raul.cabrera@campustfi.edu.ar"),
    ("Noelia Villalba", "noelia.villalba@campustfi.edu.ar"),
    ("Ramiro Escobar", "ramiro.escobar@campustfi.edu.ar"),
    ("Verónica Leiva", "veronica.leiva@campustfi.edu.ar"),
]

# ===================== Los estudiantes =====================
# (nombre, correo, carrera, comisión, año de ingreso, hace cuánto entró al
# campus en minutos). El último dato es el que dibuja el puntito de presencia:
# con todos iguales, la lista de participantes se ve muerta.
ESTUDIANTES = [
    # Primer año de Sistemas: los compañeros de Santiago (comisión 1)
    ("Lucía Acosta", "lucia.acosta@campustfi.edu.ar", 1, 1, 2026, 4),
    ("Tomás Vallejos", "tomas.vallejos@campustfi.edu.ar", 1, 1, 2026, 18),
    ("Camila Ríos", "camila.rios@campustfi.edu.ar", 1, 1, 2026, 55),
    ("Nicolás Duarte", "nicolas.duarte@campustfi.edu.ar", 1, 1, 2026, 240),
    ("Martina Aguirre", "martina.aguirre@campustfi.edu.ar", 1, 1, 2026, 1500),
    ("Facundo Zalazar", "facundo.zalazar@campustfi.edu.ar", 1, 2, 2026, 90),
    ("Valentina Correa", "valentina.correa@campustfi.edu.ar", 1, 2, 2026, 7),
    # Segundo año de Sistemas (comisión 3)
    ("Joaquín Medina", "joaquin.medina@campustfi.edu.ar", 1, 3, 2025, 11),
    ("Sofía Brítez", "sofia.britez@campustfi.edu.ar", 1, 3, 2025, 35),
    ("Agustín Paredes", "agustin.paredes@campustfi.edu.ar", 1, 3, 2025, 420),
    ("Micaela Fernández", "micaela.fernandez@campustfi.edu.ar", 1, 3, 2025, 2),
    ("Lautaro Benítez", "lautaro.benitez@campustfi.edu.ar", 1, 4, 2025, 3000),
    # Tercer año de Sistemas (comisión 5)
    ("Rocío Maidana", "rocio.maidana@campustfi.edu.ar", 1, 5, 2024, 60),
    ("Emanuel Quintana", "emanuel.quintana@campustfi.edu.ar", 1, 5, 2024, 8),
    # Profesorado en Matemática
    ("Ariana Gauna", "ariana.gauna@campustfi.edu.ar", 2, 7, 2026, 25),
    ("Mauro Alegre", "mauro.alegre@campustfi.edu.ar", 2, 7, 2026, 300),
    ("Delfina Ocampo", "delfina.ocampo@campustfi.edu.ar", 2, 9, 2025, 45),
    # Ciencias Químicas
    ("Brenda Sandoval", "brenda.sandoval@campustfi.edu.ar", 3, 13, 2026, 15),
    ("Ignacio Ferreira", "ignacio.ferreira@campustfi.edu.ar", 3, 13, 2026, 130),
    ("Julieta Mansilla", "julieta.mansilla@campustfi.edu.ar", 3, 15, 2025, 70),
]

# Las dos que quedan esperando que alguien les cree el acceso. Es un estado
# real —alta cargada, cuenta sin crear— y es el que mira la secretaría.
SIN_ACTIVAR = {"lautaro.benitez@campustfi.edu.ar", "julieta.mansilla@campustfi.edu.ar"}


def _nuevo_id_persona() -> int:
    return max((p["id"] for p in d.personas), default=0) + 1


def _asegurar_persona(nombre: str, correo: str, roles: list[str], acceso: int) -> tuple[dict, bool]:
    def armar() -> dict:
        persona = {
            "id": _nuevo_id_persona(),
            "nombre": nombre,
            "correo": correo,
            "roles": roles,
            "accesoHaceMin": acceso,
            "dni": None,
            "telefono": None,
            "fechaNacimiento": None,
            "foto": None,
            "estado": "pendiente" if correo in SIN_ACTIVAR else "activa",
            "creada": comun.dias(-420 if "Docente" in roles else -300),
        }
        # Docentes y administración llevan legajo del campus: en un acta o en
        # el registro de auditoría el nombre no identifica a nadie.
        legajos.asegurar_institucional(persona)
        return persona

    return comun.asegurar(
        d.personas, lambda p: (p.get("correo") or "").lower() == correo.lower(), armar
    )


def _asegurar_asociacion(persona: dict, carrera_id: int, comision_id: int, ingreso: int) -> bool:
    """La inscripción a la carrera: legajo, sede, comisión y plan.

    Sin esto la persona tiene el rol de estudiante pero no está en ninguna
    carrera, y entonces no la cuenta ningún tablero ni la ve ninguna planilla:
    el campus la trata como alguien que todavía no se inscribió.
    """
    comision = d.buscar_en(d.comisiones, comision_id) or {}
    plan = next(
        (p for p in d.planes_estudio if p.get("carreraId") == carrera_id and p.get("activo")),
        None,
    )

    def armar() -> dict:
        return {
            "id": d.nuevo_id_asociacion(),
            "personaId": persona["id"],
            "carreraId": carrera_id,
            "sedeId": comision.get("sedeId") or 1,
            "comisionId": comision_id,
            "planId": comision.get("planId") or (plan["id"] if plan else None),
            "ingreso": ingreso,
            "legajo": legajos.proximo_de_carrera(carrera_id, ingreso),
            "desde": comun.dias(-(2026 - ingreso) * 300 - 20),
            "estado": "activa",
        }

    _, creada = comun.asegurar(
        d.asociaciones_academicas,
        lambda a: a["personaId"] == persona["id"] and a["carreraId"] == carrera_id,
        armar,
    )
    return creada


def armar(cuenta: comun.Cuenta) -> dict[str, list[int]]:
    """Da de alta la población y devuelve quién es quién, por comisión.

    El resultado lo usan los otros armadores: las inscripciones a materias, el
    foro y las planillas de asistencia necesitan saber qué estudiantes hay en
    cada comisión, y esa cuenta se hace una sola vez.
    """
    for nombre, correo in DOCENTES:
        _, creado = _asegurar_persona(nombre, correo, ["Docente"], acceso=120)
        cuenta.anotar("docentes", creado)

    por_comision: dict[int, list[int]] = {}
    for nombre, correo, carrera_id, comision_id, ingreso, acceso in ESTUDIANTES:
        persona, creado = _asegurar_persona(nombre, correo, ["Estudiante"], acceso=acceso)
        cuenta.anotar("estudiantes", creado)
        if _asegurar_asociacion(persona, carrera_id, comision_id, ingreso):
            cuenta.anotar("inscripciones a carrera", True)
        por_comision.setdefault(comision_id, []).append(persona["id"])

    # Santiago ya está en el campus y en su comisión: solo se lo ubica en el
    # mapa para que el resto de los armadores lo incluyan como a cualquiera.
    santiago = comun.persona_por_correo(SANTIAGO)
    if santiago:
        por_comision.setdefault(1, []).insert(0, santiago["id"])
    pedro = comun.persona_por_correo(PEDRO)
    if pedro:
        por_comision.setdefault(2, []).append(pedro["id"])

    return {str(k): v for k, v in por_comision.items()}
