"""El expediente del campus: quién cursa qué, qué aprobó, qué entregó y qué le falta.

Es la parte que sostiene a todas las demás. Sin historial académico no hay
correlatividades que comprobar y la pantalla de inscripción dice que sí a todo;
sin inscripciones no hay participantes en los módulos; sin entregas el docente
no tiene nada que corregir y el panel de control muestra ceros.

Las tres reglas que se respetan acá
-----------------------------------
1. **La condición la manda el historial, no la inscripción.** `Aprobada`
   habilita las correlativas, `Regular` habilita a rendir el final.
2. **Una mesa se rinde si la materia está regular.** Por eso las mesas que se
   crean son de materias donde hay gente regular: una mesa a la que nadie
   puede anotarse no muestra nada.
3. **Lo que se entrega vale la última versión.** Las entregas llevan su
   archivo de verdad, subido a R2 como cualquier otra.
"""

from __future__ import annotations

from .. import datos as d
from . import archivos, catalogo, comun, modulos
from .gente import SANTIAGO

# Qué año cursa cada comisión. Sale de la comisión misma, pero tenerlo acá
# evita recorrer la lista en cada vuelta.
LLAMADO = "Turno diciembre · 1.er llamado"
SEGUNDO_LLAMADO = "Turno diciembre · 2.º llamado"


def _materias_de(carrera_id: int, anio: int) -> list[dict]:
    return [
        m for m in d.materias_plan
        if m.get("carreraId") == carrera_id and m.get("anio") == anio and m.get("activa", True)
    ]


def _inscribir(persona_id: int, materia: dict) -> bool:
    _, creada = comun.asegurar(
        d.inscripciones_materias,
        lambda i: i["personaId"] == persona_id and i["materiaId"] == materia["id"],
        lambda: {
            "id": d.nuevo_id_inscripcion_materia(),
            "personaId": persona_id,
            "materiaId": materia["id"],
            "fecha": comun.dias(-40),
        },
    )
    return creada


def _historial(persona_id: int, materia_id: int, condicion: str, nota=None, hace=-60) -> bool:
    _, creado = comun.asegurar(
        d.historial_academico,
        lambda h: h["personaId"] == persona_id and h["materiaId"] == materia_id,
        lambda: {
            "personaId": persona_id,
            "materiaId": materia_id,
            "condicion": condicion,
            "nota": nota,
            "fecha": comun.dias(hace),
        },
    )
    return creado


def _cursada(cuenta: comun.Cuenta, por_comision: dict[str, list[int]]) -> None:
    """Inscribe a cada estudiante en las materias de su año y le arma el pasado.

    El pasado importa tanto como el presente: un alumno de segundo que no tiene
    aprobado nada de primero no debería poder estar cursando, y la pantalla de
    inscripción lo diría. Sin historial, el campus muestra a todo el mundo
    habilitado para todo.
    """
    for clave, gente in por_comision.items():
        comision = d.buscar_en(d.comisiones, int(clave))
        if not comision:
            continue
        carrera_id = comision.get("carreraId")
        anio = comision.get("anio") or 1

        for orden, persona_id in enumerate(gente):
            # Lo que está cursando ahora
            for materia in _materias_de(carrera_id, anio):
                if _inscribir(persona_id, materia):
                    cuenta.anotar("inscripciones a materias", True)
                # Quien se inscribió a una materia la está cursando, salvo que
                # ya tenga otra condición cargada.
                if d.condicion_en(persona_id, materia["id"]) is None:
                    _historial(persona_id, materia["id"], "En curso", hace=-40)

            # Lo que ya cursó: los años anteriores, con variedad. Uno de cada
            # cinco queda libre en una materia y otro regular, porque un campus
            # donde todos aprobaron todo no sirve para mostrar ninguna regla.
            for anterior in range(1, anio):
                for lugar, materia in enumerate(_materias_de(carrera_id, anterior)):
                    resto = (orden + lugar) % 5
                    if resto == 0:
                        condicion, nota = "Regular", None
                    elif resto == 1 and lugar % 3 == 0:
                        condicion, nota = "Libre", None
                    else:
                        condicion, nota = "Aprobada", 6 + (orden + lugar) % 5
                    if _historial(persona_id, materia["id"], condicion, nota,
                                  hace=-200 * (anio - anterior)):
                        cuenta.anotar("historial académico", True)


def _santiago(cuenta: comun.Cuenta) -> None:
    """El expediente de la cuenta con la que se muestra el campus.

    Se arma a mano y no con la regla general porque es el que se va a mirar de
    cerca: tiene una materia aprobada con su final rendido, dos regulares —que
    son las que lo habilitan a anotarse a una mesa— y el resto en curso.
    """
    persona = comun.persona_por_correo(SANTIAGO)
    if not persona:
        return
    yo = persona["id"]

    plan = {
        "SIS-101": ("Aprobada", 8, -210),   # cursada y final aprobados
        "SIS-102": ("Regular", None, -45),  # cursada aprobada, final pendiente
        "SIS-103": ("Regular", None, -45),
        "SIS-104": ("En curso", None, -40),
        "SIS-105": ("En curso", None, -40),
        "SIS-106": ("En curso", None, -40),
        "SIS-107": ("En curso", None, -40),
    }
    for codigo, (condicion, nota, hace) in plan.items():
        materia = comun.materia_por_codigo(codigo)
        if not materia:
            continue
        registro = next(
            (h for h in d.historial_academico
             if h["personaId"] == yo and h["materiaId"] == materia["id"]), None
        )
        if registro:
            registro.update({"condicion": condicion, "nota": nota})
        else:
            _historial(yo, materia["id"], condicion, nota, hace)
            cuenta.anotar("historial académico", True)

    # Los finales que ya rindió: uno desaprobado y el siguiente aprobado. Dos
    # resultados de la misma materia es lo normal en un expediente y es lo que
    # hace que la pantalla de resultados muestre algo más que una fila.
    algebra = comun.materia_por_codigo("SIS-101")
    if algebra:
        for nota, condicion, hace, llamado in (
            (4, "Desaprobado", -250, "Turno julio · 1.er llamado"),
            (8, "Aprobado", -210, "Turno julio · 2.º llamado"),
        ):
            _, creado = comun.asegurar(
                d.resultados_finales,
                lambda r, nota=nota: r.get("personaId") == yo
                and r.get("materiaId") == algebra["id"] and r.get("nota") == nota,
                lambda nota=nota, condicion=condicion, hace=hace, llamado=llamado: {
                    "id": d.nuevo_id_resultado_final(),
                    "personaId": yo,
                    "materiaId": algebra["id"],
                    "mesaId": None,
                    "fecha": comun.dias(hace),
                    "nota": nota,
                    "condicion": condicion,
                    "llamado": llamado,
                },
            )
            cuenta.anotar("finales rendidos", creado)


# ===================== Las mesas de examen =====================
# (código, cuándo es, apertura y cierre de la inscripción, cupo, estado).
MESAS = [
    ("SIS-102", 12, -5, 9, 40, "programada", "Escrito y oral"),
    ("SIS-103", 15, -5, 12, 35, "programada", "Escrito"),
    ("SIS-101", 18, 3, 16, 40, "programada", "Escrito y oral"),
    ("SIS-105", 20, -2, 17, None, "programada", "Oral"),
    ("SIS-106", 13, -6, 10, 60, "programada", "Escrito"),
    ("ALG-2", -3, -25, -6, 30, "programada", "Escrito y oral"),      # ya tomada, acta abierta
    ("BD-1", -12, -35, -15, 30, "programada", "Escrito"),            # acta cerrada
    ("PROG-2", 25, 8, 22, 30, "cancelada", "Escrito y oral"),
    ("MAT-3", 16, -4, 13, 45, "programada", "Escrito"),
    ("IS-1", 22, 2, 19, 35, "programada", "Oral"),
]


def _mesas(cuenta: comun.Cuenta) -> dict[str, dict]:
    creadas: dict[str, dict] = {}
    for codigo, cuando, abre, cierra, cupo, estado, instancia in MESAS:
        materia = comun.materia_por_codigo(codigo)
        if not materia:
            continue
        docentes = d.docentes_de_materia(materia["id"])
        if not docentes:
            continue
        # El tribunal: el titular primero —eso es lo que lo hace titular— y
        # alguien más de la casa.
        otros = [p["id"] for p in d.personas
                 if "Docente" in (p.get("roles") or []) and p["id"] not in docentes]
        tribunal = [docentes[0]] + otros[:1]
        cancelada = estado == "cancelada"

        mesa, creada = comun.asegurar(
            d.mesas_examen,
            lambda m: m.get("materiaId") == materia["id"]
            and comun.plano(m.get("llamado")) == comun.plano(LLAMADO),
            lambda: {
                "id": d.nuevo_id_mesa(),
                "materiaId": materia["id"],
                "tribunal": tribunal,
                "fecha": comun.dias(cuando, hora=9 if materia["anio"] == 1 else 14),
                "desde": "09:00" if materia["anio"] == 1 else "14:00",
                "hasta": "12:00" if materia["anio"] == 1 else "17:00",
                "modalidad": "Presencial",
                "lugar": f"Aula {10 + materia['id'] % 8} – Pabellón A",
                "cupo": cupo,
                "inscripcionDesde": comun.dias(abre, hora=8),
                "inscripcionHasta": comun.dias(cierra, hora=23, minuto=59),
                "llamado": LLAMADO,
                "instancia": instancia,
                "estado": "cancelada" if cancelada else "programada",
                "motivoCancelacion": (
                    "La cátedra reprograma la mesa por superposición con el cierre de actas. "
                    "La nueva fecha se publica la semana próxima."
                ) if cancelada else None,
                "actaCerrada": False,
                "historial": [],
            },
        )
        cuenta.anotar("mesas de examen", creada)
        creadas[codigo] = mesa
    return creadas


def _inscribir_a_finales(cuenta: comun.Cuenta, mesas: dict[str, dict]) -> None:
    """Anota en cada mesa a quienes están en condiciones de rendirla."""
    for codigo, mesa in mesas.items():
        if mesa.get("estado") == "cancelada":
            continue
        materia = comun.materia_por_codigo(codigo)
        if not materia:
            continue
        candidatos = [
            h["personaId"] for h in d.historial_academico
            if h["materiaId"] == materia["id"] and h.get("condicion") == "Regular"
        ]
        for persona_id in candidatos[:8]:
            _, creada = comun.asegurar(
                d.inscripciones_finales,
                lambda i, persona_id=persona_id: i.get("personaId") == persona_id
                and i.get("mesaId") == mesa["id"],
                lambda persona_id=persona_id: {
                    "id": d.nuevo_id_inscripcion_final(),
                    "personaId": persona_id,
                    "mesaId": mesa["id"],
                    "fecha": comun.dias(-3),
                    "estado": "Inscripto",
                    "comision": "A",
                    "nota": None,
                    "resultado": None,
                },
            )
            cuenta.anotar("inscripciones a mesas", creada)


def _actas(cuenta: comun.Cuenta, mesas: dict[str, dict]) -> None:
    """Carga las notas de las dos mesas que ya se tomaron.

    Una queda con el acta **abierta** y a medio cargar —es lo que el docente
    ve cuando entra a terminar de corregir— y la otra cerrada, con los
    resultados ya volcados al historial. Las dos son estados reales del
    circuito y las dos se ven distinto en la pantalla.
    """
    for codigo, cerrar in (("ALG-2", False), ("BD-1", True)):
        mesa = mesas.get(codigo)
        materia = comun.materia_por_codigo(codigo)
        if not mesa or not materia:
            continue
        inscriptos = [i for i in d.inscripciones_finales if i.get("mesaId") == mesa["id"]]
        if not inscriptos:
            continue

        for lugar, inscripcion in enumerate(inscriptos):
            if not cerrar and lugar >= len(inscriptos) // 2:
                continue  # el acta abierta queda a medio cargar, a propósito
            nota = [8, 6, 4, 9, 7, 2, 10][lugar % 7]
            condicion = "Aprobado" if nota >= 6 else "Desaprobado"
            if lugar == 2 and not cerrar:
                nota, condicion = None, "Ausente"
            inscripcion["nota"] = nota
            inscripcion["resultado"] = condicion
            inscripcion["estado"] = "Ausente" if condicion == "Ausente" else "Rindió"

            if not cerrar:
                continue

            _, creado = comun.asegurar(
                d.resultados_finales,
                lambda r, inscripcion=inscripcion: r.get("mesaId") == mesa["id"]
                and r.get("personaId") == inscripcion["personaId"],
                lambda inscripcion=inscripcion, nota=nota, condicion=condicion: {
                    "id": d.nuevo_id_resultado_final(),
                    "personaId": inscripcion["personaId"],
                    "materiaId": materia["id"],
                    "mesaId": mesa["id"],
                    "fecha": mesa["fecha"],
                    "nota": nota,
                    "condicion": condicion,
                    "llamado": mesa["llamado"],
                },
            )
            cuenta.anotar("finales rendidos", creado)

            # Aprobar el final es lo que cambia la condición en el plan: es la
            # juntura entre las dos mitades del apartado.
            if condicion == "Aprobado":
                registro = next(
                    (h for h in d.historial_academico
                     if h["personaId"] == inscripcion["personaId"]
                     and h["materiaId"] == materia["id"]), None
                )
                if registro:
                    registro.update({"condicion": "Aprobada", "nota": nota})

        if cerrar:
            mesa["actaCerrada"] = True
            mesa["historial"] = [{
                "accion": "acta cerrada",
                "quien": mesa["tribunal"][0],
                "fecha": comun.dias(-11),
                "detalle": "Acta cerrada con todos los resultados cargados",
            }]


# ===================== Entregas y notas =====================
def _bloques_entrega(alumno: dict, tarea: dict, curso: dict) -> list[tuple[str, str]]:
    return [
        ("titulo", tarea["titulo"]),
        ("bajada", f"{curso['nombre']} · {alumno['nombre']}"),
        ("campo", f"Estudiante: {alumno['nombre']}"),
        ("campo", f"Materia: {curso['nombre']}"),
        ("seccion", "Resolución"),
        ("texto",
         "Para resolver el trabajo partí de la guía de la unidad y fui anotando cada decisión "
         "que tomé. Lo que sigue es el desarrollo, con los pasos en el orden en que los hice y "
         "las dudas que me quedaron al final."),
        ("seccion", "Desarrollo"),
        ("lista", "Punto 1. Planteo del problema y datos con los que cuento."),
        ("lista", "Punto 2. Camino elegido y por qué descarté el otro."),
        ("lista", "Punto 3. Resolución paso a paso, con las cuentas intermedias."),
        ("lista", "Punto 4. Verificación del resultado con un caso de prueba."),
        ("seccion", "Conclusiones"),
        ("texto",
         "El resultado coincide con la verificación del punto 4. La parte que más me costó fue "
         "justificar por qué el método elegido vale para el caso general y no solo para el "
         "ejemplo, y es lo que quiero repasar en la clase de consulta."),
        ("seccion", "Dudas que me quedaron"),
        ("lista", "Si hay otra forma de llegar al mismo resultado con menos pasos."),
        ("lista", "Cómo presentar la verificación cuando el caso de prueba es muy grande."),
    ]


def _entregas(cuenta: comun.Cuenta, trabajos: dict[str, list[dict]]) -> None:
    """Las entregas de los trabajos ya vencidos, con su archivo y su nota.

    **Una queda sin corregir en cada módulo**, a propósito: es lo que enciende
    la alerta de «trabajos vencidos sin corregir» del panel de control y lo
    primero que ve el docente al entrar.
    """
    for codigo, tareas in trabajos.items():
        if modulos.profundidad(codigo) != "completo":
            continue
        curso = comun.curso_de_codigo(codigo)
        if not curso:
            continue
        vencidos = [t for t in tareas if d.desde_iso(t["fechaLimite"]) < d.ahora()
                    and t.get("formato") == "entrega"]
        if not vencidos:
            continue
        tarea = vencidos[0]
        docente_id = curso.get("docenteId")
        alumnos = [p for p in d.participantes_de_curso(curso) if p["id"] != docente_id][:4]

        for lugar, alumno in enumerate(alumnos):
            ya = next(
                (e for e in d.entregas
                 if e.get("tareaId") == tarea["id"] and e.get("personaId") == alumno["id"]), None
            )
            if ya:
                continue
            ficha = archivos.subir_pdf(
                "entregas", (tarea["id"], alumno["id"]),
                f"{tarea['titulo']} {alumno['nombre']}",
                _bloques_entrega(alumno, tarea, curso),
                persona_id=alumno["id"], registro_id=tarea["id"],
            )
            d.entregas.append({
                "id": d.nuevo_id_entrega(),
                "tareaId": tarea["id"],
                "personaId": alumno["id"],
                "fecha": comun.dias(-7 + lugar % 3),
                "archivo": ficha,
                "comentario": None,
            })
            cuenta.anotar("entregas", True)

            # La última entrega de cada trabajo queda sin corregir.
            if lugar == len(alumnos) - 1:
                continue
            nota = [9, 7, 6, 8][lugar % 4]
            comentarios = [
                "Muy prolijo y bien justificado. Revisá la notación del punto 3.",
                "Está bien resuelto. Falta explicar por qué descartaste la otra opción.",
                "Alcanza para aprobar, pero la verificación del final quedó floja.",
                "Buen trabajo. El anexo con el código ayuda a seguir el razonamiento.",
            ]
            d.calificaciones.append({
                "id": d.nuevo_id_calificacion(),
                "cursoId": curso["id"],
                "tareaId": tarea["id"],
                "personaId": alumno["id"],
                "nota": nota,
                "estado": "Aprobado" if nota >= 6 else "Desaprobado",
                "comentario": comentarios[lugar % 4],
                "docenteId": docente_id,
                "fecha": comun.dias(-4),
            })
            cuenta.anotar("notas de trabajos", True)


# ===================== Progreso del alumno =====================
def _progreso(cuenta: comun.Cuenta) -> None:
    """Lo que cada uno marcó como visto. Es lo que dibuja las barras de avance.

    Con todo en cero, las barras de los módulos se ven rojas y el campus
    parece recién estrenado; con todo marcado, el panel de tareas no muestra
    nada pendiente. Se marca algo más de la mitad, que es como se ve un
    cuatrimestre a esta altura.
    """
    for persona in d.personas:
        if "Estudiante" not in (persona.get("roles") or []):
            continue
        for inscripcion in list(d.inscripciones_materias):
            if inscripcion["personaId"] != persona["id"]:
                continue
            materia = d.buscar_materia(inscripcion["materiaId"])
            curso = d.buscar_curso((materia or {}).get("cursoId"))
            if not curso:
                continue
            marcables = [
                item
                for carpeta in d.contenidos.get(curso["id"], [])
                for item in carpeta.get("items", [])
                if d.es_marcable(item)
            ]
            cuantos = int(len(marcables) * (0.75 if persona["id"] % 3 == 0 else 0.55))
            for item in marcables[:cuantos]:
                _, creado = comun.asegurar(
                    d.progreso_alumnos,
                    lambda p, item=item: p.get("personaId") == persona["id"]
                    and p.get("cursoId") == curso["id"] and p.get("itemId") == item["id"],
                    lambda item=item: {
                        "personaId": persona["id"],
                        "cursoId": curso["id"],
                        "itemId": item["id"],
                        "fecha": comun.dias(-10),
                    },
                )
                cuenta.anotar("material marcado como visto", creado)


# ===================== Asistencia =====================
def _asistencia(cuenta: comun.Cuenta) -> None:
    """Clases dictadas y lista tomada en los módulos que se muestran.

    Sin esto, el porcentaje de asistencia del panel y la pantalla de
    Asistencias están en cero, y el mínimo del 70 % no se puede mostrar
    funcionando. Se cargan doce clases por módulo, con faltas repartidas: uno
    de los estudiantes queda por debajo del mínimo, que es el caso que la
    facultad necesita ver.
    """
    for codigo in ("SIS-103", "SIS-102", "PROG-2", "ALG-2"):
        curso = comun.curso_de_codigo(codigo)
        ficha = catalogo.CATALOGO.get(codigo)
        if not curso or not ficha:
            continue
        docente_id = curso.get("docenteId")
        alumnos = [p for p in d.participantes_de_curso(curso) if p["id"] != docente_id]
        if not alumnos:
            continue

        comun.asegurar(
            d.planificacion_asistencia,
            lambda p: p.get("cursoId") == curso["id"],
            lambda: {
                "cursoId": curso["id"],
                "clasesPlanificadas": 32,
                "actualizadoPor": docente_id,
                "fecha": comun.dias(-90),
            },
        )

        for numero in range(12):
            cuando = comun.dias(-84 + numero * 7)
            if any(
                c.get("cursoId") == curso["id"] and d.clave_dia(c["fecha"]) == d.clave_dia(cuando)
                for c in d.clases_asistencia
            ):
                continue
            unidad = ficha["unidades"][min(numero // 3, len(ficha["unidades"]) - 1)]
            clase = {
                "id": d.nuevo_id_clase_asistencia(),
                "cursoId": curso["id"],
                "fecha": cuando,
                "tema": modulos.partes_de_unidad(unidad)[0],
                "estado": "dictada",
                "docenteId": docente_id,
                "cerrada": True,
                "registradaEl": cuando,
                "motivo": None,
            }
            d.clases_asistencia.append(clase)
            cuenta.anotar("clases dictadas", True)

            for lugar, alumno in enumerate(alumnos):
                # El patrón deja a una persona con muchas faltas y al resto con
                # alguna suelta.
                if lugar == len(alumnos) - 1 and numero % 3 != 0:
                    estado = "ausente"
                elif (numero + lugar) % 11 == 0:
                    estado = "justificada" if lugar % 2 else "ausente"
                else:
                    estado = "presente"
                d.asistencias.append({
                    "id": d.nuevo_id_asistencia(),
                    "claseId": clase["id"],
                    "personaId": alumno["id"],
                    "estado": estado,
                    "observacion": None,
                    "registradoPor": docente_id,
                    "fecha": cuando,
                })
                cuenta.anotar("asistencias tomadas", True)


def armar(cuenta: comun.Cuenta, por_comision: dict[str, list[int]], trabajos: dict) -> None:
    _cursada(cuenta, por_comision)
    _santiago(cuenta)
    mesas = _mesas(cuenta)
    _inscribir_a_finales(cuenta, mesas)
    _actas(cuenta, mesas)
    _entregas(cuenta, trabajos)
    _progreso(cuenta)
    _asistencia(cuenta)
