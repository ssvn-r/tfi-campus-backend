"""Lo que hace que el campus parezca habitado: novedades, foro, mensajes y eventos.

Las tres pantallas comparten un problema: **sin gente adentro no se entienden**.
Un muro de novedades vacío se lee como una pantalla rota, un foro sin temas no
muestra para qué sirve y un calendario sin nada no deja ver que distingue
entregas, exámenes, clases y eventos de la facultad.

Las reacciones son anónimas
---------------------------
El campus guarda **quiénes** reaccionaron para que nadie reaccione dos veces,
pero no los devuelve nunca: la pantalla muestra los totales y la reacción
propia. Por eso acá se reparten ids de verdad entre las tres reacciones, y no
un número suelto: un contador inventado no sobreviviría a que alguien toque el
botón (ver `rutas/novedades.py`).
"""

from __future__ import annotations

from .. import datos as d
from . import archivos, comun, imagenes
from .gente import CLAUDIA, MARIA, SANTIAGO, SECRETARIA

# (título, cuerpo, correo del autor, ámbito, categoría, portada, hace cuántos
# días, anclada). La portada vacía deja la novedad sin imagen: no todas la
# llevan, y un muro donde todas tienen foto se ve tan falso como uno donde
# ninguna la tiene.
NOVEDADES = [
    (
        "Inscripción a las mesas de examen de diciembre",
        "La inscripción a las mesas del turno de diciembre abre el lunes y cierra 48 horas "
        "antes de cada examen. Se hace desde el campus, en Finales → Inscripciones.\n\n"
        "Si te falta alguna correlativa, el sistema no te va a dejar anotarte y te va a decir "
        "cuál es. En ese caso pasá por Alumnado antes del cierre: hay casos que se resuelven "
        "con una equivalencia ya tramitada que todavía no está cargada.",
        SECRETARIA, "Institucional", "Inscripciones", "inscripciones", -1, True,
    ),
    (
        "La biblioteca extiende su horario por los parciales",
        "Durante noviembre y diciembre la sala de lectura queda abierta de lunes a viernes "
        "hasta las 22, y los sábados de 9 a 13.\n\n"
        "Para reservar una sala de grupo hay que anotarse en el mostrador con un día de "
        "anticipación. Las salas son para grupos de tres o más: si van a estudiar solos, la "
        "sala general tiene lugar de sobra.",
        CLAUDIA, "Institucional", "Biblioteca", "biblioteca", -4, False,
    ),
    (
        "Becas de ayuda económica: resultados de la segunda convocatoria",
        "Ya se pueden consultar los resultados en Bienestar Estudiantil. Quienes queden en "
        "lista de espera van a recibir un aviso por este mismo campus apenas se libere un "
        "lugar.\n\nLa documentación de quienes resultaron adjudicatarios se presenta hasta el "
        "viernes de la semana próxima. Sin esa presentación la beca no se hace efectiva.",
        SECRETARIA, "Institucional", "Becas", "becas", -9, False,
    ),
    (
        "Corte de agua programado para el sábado",
        "El sábado de 7 a 14 no va a haber agua en el pabellón de aulas por mantenimiento de "
        "la cisterna. Las clases de consulta de ese día pasan al pabellón central, misma hora "
        "y mismas aulas numeradas.",
        SECRETARIA, "Institucional", "Campus", "campus", -16, False,
    ),
    (
        "Cierre de la inscripción a materias",
        "La inscripción a materias cierra el 20 de diciembre a las 23.59. Después de esa hora "
        "el sistema no acepta altas ni bajas y los cambios se hacen por nota en Alumnado.\n\n"
        "Revisá que las materias que figuran en «Mis módulos» sean las que vas a cursar: lo "
        "que esté anotado el día del cierre es lo que después aparece en el acta.",
        SECRETARIA, "Institucional", "Inscripciones", "", -2, False,
    ),
    (
        "Jornada de Ciencias Exactas: se abre la inscripción",
        "La jornada es el viernes de la semana que viene, de 9 a 17, en el pabellón central. "
        "Hay charlas de las tres carreras, muestra de trabajos finales y una mesa de egresados "
        "que cuenta en qué están trabajando.\n\nLa inscripción es libre y gratuita, pero el "
        "cupo de los talleres de la tarde es limitado.",
        SECRETARIA, "Institucional", "Campus", "campus", -6, False,
    ),
    (
        "Charla abierta: qué hace un ingeniero de software el primer año",
        "Invitamos a una charla con tres egresados de la carrera que trabajan en desarrollo, "
        "en datos y en infraestructura. Van a contar cómo fue el primer año de trabajo y qué "
        "de la carrera les sirvió de verdad.\n\nEs el jueves a las 17 en el salón de actos. "
        "No hace falta anotarse.",
        "laura.benitez@campustfi.edu.ar", "Académico", "Académico", "", -3, False,
    ),
    (
        "Taller de uso del campus para ingresantes",
        "Si entraste este año y todavía no te movés cómodo en el campus, el martes hay un "
        "taller de una hora en el laboratorio 1: cómo encontrar el material de cada materia, "
        "cómo entregar un trabajo y cómo anotarse a un final.\n\nNo hay que llevar nada: las "
        "máquinas del laboratorio alcanzan.",
        SECRETARIA, "Institucional", "Campus", "", -20, False,
    ),
    (
        "Convocatoria a ayudantes de cátedra",
        "Están abiertas las inscripciones para ayudantes de segunda en seis cátedras de la "
        "licenciatura. Se requiere tener aprobada la materia con 7 o más y la cursada al día.\n\n"
        "Las postulaciones se reciben hasta fin de mes en Secretaría Académica, con el "
        "certificado analítico y una nota de la cátedra.",
        SECRETARIA, "Institucional", "Académico", "", -7, False,
    ),
    (
        "Nuevas máquinas en el laboratorio 3",
        "El laboratorio 3 tiene veinte equipos nuevos con el entorno de las materias de "
        "programación ya instalado. El laboratorio queda libre para estudiar de 8 a 12, salvo "
        "cuando hay clase.",
        "diego.fernandez@campustfi.edu.ar", "Institucional", "Campus", "", -14, False,
    ),
    (
        "Resultados del primer parcial de Programación I",
        "Las notas ya están cargadas en el módulo, en la pestaña de notas. La vista del "
        "parcial es el martes de 18 a 19 en el laboratorio 3.\n\nQuienes tengan que recuperar: "
        "el recuperatorio es en dos semanas y entra el mismo programa. Pasen por la clase de "
        "consulta antes, que para eso está.",
        MARIA, "Académico", "Académico", "", -5, False,
    ),
    (
        "Encuesta sobre el campus virtual",
        "Estamos juntando opiniones sobre el campus para decidir qué mejorar el año que viene. "
        "Son cinco preguntas y es anónima.\n\nInteresa sobre todo lo que no encontrás o lo que "
        "te cuesta hacer: esas respuestas son las que cambian el orden de las pantallas.",
        SECRETARIA, "Institucional", "Campus", "", -8, False,
    ),
    (
        "Cronograma de mesas de examen de diciembre",
        "Ya está publicado el cronograma completo del turno de diciembre, con las dos fechas "
        "de cada materia. Está en Finales → Fechas, y cada mesa dice su aula y su horario.\n\n"
        "Las mesas de las materias de primer año son todas por la mañana; las de segundo y "
        "tercero, por la tarde.",
        SECRETARIA, "Institucional", "Académico", "inscripciones", -10, False,
    ),
    (
        "Material nuevo en la biblioteca de Bases de Datos",
        "Subí a la biblioteca de la materia los apuntes de normalización y la guía de "
        "consultas SQL con sus soluciones. Están en Biblioteca, filtrando por la materia.\n\n"
        "Si encuentran un error, avisen por el foro así lo corrijo para todos.",
        "pablo.ruiz@campustfi.edu.ar", "Académico", "Biblioteca", "", -2, False,
    ),
    (
        "Se suspende la actividad del viernes por asamblea",
        "El viernes no hay actividad académica entre las 14 y las 18 por asamblea de "
        "estudiantes en el aula magna. Las clases de ese horario se recuperan la semana "
        "siguiente, en el mismo día y horario.",
        SECRETARIA, "Institucional", "Campus", "", -11, False,
    ),
    (
        "Cómo pedir una constancia de alumno regular",
        "La constancia se pide por el campus y se retira en Alumnado al día siguiente. Si la "
        "necesitás para un trámite con fecha, pedila con tiempo: en época de inscripciones la "
        "demora llega a tres días.",
        SECRETARIA, "Institucional", "Académico", "", -22, False,
    ),
]


def _reacciones(indice: int, estudiantes: list[int]) -> dict:
    """Reparte reacciones entre la gente de verdad, sin que nadie ponga dos.

    El reparto es fijo —depende de la posición de la novedad— para que dos
    corridas del sembrado den lo mismo y no aparezcan números distintos cada
    vez que se mira la pantalla.
    """
    if not estudiantes:
        return {"leido": [], "util": [], "dudas": []}
    leido, util, dudas = [], [], []
    for lugar, persona in enumerate(estudiantes):
        resto = (lugar + indice) % 7
        if resto in (0, 1, 2):
            leido.append(persona)
        elif resto in (3, 4):
            util.append(persona)
        elif resto == 5:
            dudas.append(persona)
    return {"leido": leido, "util": util, "dudas": dudas}


def _novedades(cuenta: comun.Cuenta, estudiantes: list[int]) -> None:
    for indice, (titulo, cuerpo, correo, ambito, categoria, portada, cuando, anclada) in enumerate(
        NOVEDADES
    ):
        autor = comun.persona_por_correo(correo)
        if not autor:
            continue

        existente = next(
            (p for p in d.publicaciones if comun.plano(p.get("titulo")) == comun.plano(titulo)),
            None,
        )
        if existente:
            cuenta.anotar("novedades", False)
            continue

        publicacion = {
            "id": d.nuevo_id_publicacion(),
            "autorId": autor["id"],
            "ambito": ambito,
            "categoria": categoria,
            "titulo": titulo,
            "cuerpo": cuerpo,
            "imagen": None,
            "fecha": comun.dias(cuando, hora=9 + indice % 8),
            "editada": None,
            "reacciones": _reacciones(indice, estudiantes),
            "anclada": bool(anclada),
        }
        d.publicaciones.append(publicacion)
        cuenta.anotar("novedades", True)

        if portada:
            objeto = archivos.subir_imagen(
                "novedades", (publicacion["id"],), f"portada {portada}",
                imagenes.portada(portada),
                persona_id=autor["id"], registro_id=publicacion["id"],
            )
            # Se guarda la clave del objeto, no la dirección: la dirección va
            # firmada y se arma al leer.
            publicacion["imagenObjeto"] = objeto
            cuenta.sumar("portadas", 1)

    # Una sola puede estar anclada: si la base ya tenía otra, la de acá no la
    # desplaza en silencio.
    ancladas = [p for p in d.publicaciones if p.get("anclada")]
    for sobrante in ancladas[1:]:
        sobrante["anclada"] = False


# ===================== Foro =====================
# (código de materia, título, correo de quien pregunta, [(correo, texto,
# cuántas horas atrás, votos)]). Los primeros son los hilos escritos a mano,
# de las materias que se muestran; después se agregan los generados.
HILOS = [
    ("PROG-2", "¿Cómo encaran el punto 3 del trabajo práctico?",
     "lucia.acosta@campustfi.edu.ar", [
         ("lucia.acosta@campustfi.edu.ar",
          "Llegué a armar la lista pero me trabo al borrar el nodo del medio. ¿Guardan el "
          "anterior en una variable o se fijan con un segundo puntero?", 30, 0),
         ("tomas.vallejos@campustfi.edu.ar",
          "Yo uso dos punteros, uno que va adelante y otro atrás. Cuando el de adelante "
          "encuentra el nodo, el de atrás ya quedó apuntando al anterior.", 27, 3),
         (MARIA,
          "Las dos formas están bien. Si la hacen doblemente enlazada ni siquiera necesitan el "
          "segundo puntero, porque cada nodo ya conoce al anterior. Eso sí: al borrar hay que "
          "acordarse de actualizar los dos enlaces, no uno solo.", 25, 4),
     ]),
    ("SIS-103", "Error en el ejemplo de Fibonacci del apunte",
     "camila.rios@campustfi.edu.ar", [
         ("camila.rios@campustfi.edu.ar",
          "En la página 4 el caso base devuelve 1 para n = 0, y me parece que debería devolver "
          "0. Con el ejemplo del apunte la serie arranca corrida.", 70, 1),
         (MARIA,
          "Buen ojo, Camila. Está mal en el apunte: para n = 0 va 0. Ya subí la versión "
          "corregida a la sección de la unidad 3.", 68, 5),
     ]),
    ("SIS-102", "¿Entra el teorema del valor medio en el primer parcial?",
     SANTIAGO, [
         (SANTIAGO,
          "En el cronograma figura en la semana 8 pero el parcial es en la 7. ¿Lo tomamos o "
          "queda para el segundo?", 50, 0),
         (CLAUDIA,
          "Queda para el segundo parcial. En el primero entra hasta continuidad, incluidos los "
          "límites indeterminados.", 48, 6),
         ("martina.aguirre@campustfi.edu.ar",
          "Gracias, estábamos justo discutiendo eso en el grupo.", 47, 0),
     ]),
    ("BD-1", "Cardinalidades en el modelo entidad-relación",
     "joaquin.medina@campustfi.edu.ar", [
         ("joaquin.medina@campustfi.edu.ar",
          "Una materia que tiene varios docentes y un docente que da varias materias, ¿es "
          "muchos a muchos? Me suena que sí pero quiero confirmar antes de seguir el modelo.",
          6, 0),
         ("sofia.britez@campustfi.edu.ar",
          "Sí, y además te queda una entidad intermedia con el año y el cuatrimestre, porque el "
          "mismo docente puede dar la misma materia en años distintos.", 5, 2),
     ]),
    ("IS-1", "¿Hay plantilla para el documento de requisitos?",
     "agustin.paredes@campustfi.edu.ar", [
         ("agustin.paredes@campustfi.edu.ar",
          "¿Hay una plantilla para el documento o lo armamos con el índice que queramos?", 96, 0),
         ("laura.benitez@campustfi.edu.ar",
          "Pueden usar el índice de la IEEE 830, que está en el programa. Lo importante es que "
          "los requisitos funcionales y los no funcionales estén separados y que cada uno tenga "
          "su criterio de aceptación.", 94, 4),
     ]),
    ("SIS-105", "Diferencia entre memoria caché y memoria principal",
     "nicolas.duarte@campustfi.edu.ar", [
         ("nicolas.duarte@campustfi.edu.ar",
          "Entiendo que la caché es más rápida, pero no me queda claro quién decide qué se "
          "guarda ahí. ¿Lo hace el programa?", 120, 0),
         ("diego.fernandez@campustfi.edu.ar",
          "No: lo decide el hardware, con una política de reemplazo. El programa no elige, "
          "pero sí influye: si recorrés un arreglo en orden, aprovechás la localidad y la caché "
          "te acompaña. Si saltás de posición en posición, no.", 118, 5),
     ]),
    ("ALG-2", "¿Por qué el ordenamiento por burbuja es O(n²)?",
     "micaela.fernandez@campustfi.edu.ar", [
         ("micaela.fernandez@campustfi.edu.ar",
          "Veo que tiene dos ciclos anidados, pero el de adentro va achicándose. ¿Igual cuenta "
          "como n²?", 14, 0),
         (MARIA,
          "Sí. La suma 1 + 2 + … + (n−1) da n(n−1)/2, que sigue creciendo como n². Las "
          "constantes y los términos menores no cambian el orden.", 12, 3),
         ("emanuel.quintana@campustfi.edu.ar",
          "A mí me ayudó pensarlo con n = 1000: son medio millón de comparaciones igual.", 11, 1),
     ]),
    ("SIS-106", "Cómo leer un stack trace sin desesperar",
     "valentina.correa@campustfi.edu.ar", [
         ("valentina.correa@campustfi.edu.ar",
          "Cuando me salta un error en inglés de veinte líneas no sé por dónde empezar.", 40, 0),
         ("silvina.ojeda@campustfi.edu.ar",
          "Empezá por abajo: la última línea dice qué pasó, y la primera de tu archivo dice "
          "dónde. El resto del medio casi siempre es de la biblioteca, no tuyo.", 38, 7),
     ]),
]

# Para los módulos que no tienen hilo escrito, se abre uno con la pregunta que
# aparece en todos los foros del mundo. Mejor eso que un foro vacío.
GENERICOS = [
    ("¿Hasta qué unidad entra el primer parcial?",
     "Miré el cronograma pero quiero confirmarlo con la cátedra antes de ponerme a estudiar."),
    ("Dudas con la guía de ejercicios de la unidad 1",
     "Me trabé en el ejercicio 6 y no encuentro el error. ¿Alguien lo resolvió?"),
]


def _tema(curso: dict, titulo: str, autor: dict, mensajes: list[dict]) -> bool:
    _, creado = comun.asegurar(
        d.temas_foro,
        lambda t: t.get("cursoId") == curso["id"]
        and comun.plano(t.get("titulo")) == comun.plano(titulo),
        lambda: {
            "id": d.nuevo_id_tema(),
            "cursoId": curso["id"],
            "titulo": titulo,
            "autorId": autor["id"],
            "fecha": mensajes[0]["fecha"],
            "mensajes": mensajes,
            "siguen": [autor["id"]],
        },
    )
    return creado


def _foro(cuenta: comun.Cuenta) -> None:
    for codigo, titulo, correo_autor, respuestas in HILOS:
        curso = comun.curso_de_codigo(codigo)
        autor = comun.persona_por_correo(correo_autor)
        if not curso or not autor:
            continue
        mensajes = []
        for correo, texto, hace, votos in respuestas:
            quien = comun.persona_por_correo(correo)
            if not quien:
                continue
            mensajes.append({
                "id": d.nuevo_id_mensaje_foro(),
                "autorId": quien["id"],
                "texto": texto,
                "fecha": comun.horas(hace),
                "votos": [p["id"] for p in d.personas[:votos]],
            })
        if mensajes:
            cuenta.anotar("temas del foro", _tema(curso, titulo, autor, mensajes))

    # Un tema por módulo cargado a fondo que todavía no tenga ninguno.
    from . import modulos as mod

    for codigo in sorted(mod.COMPLETOS | mod.MEDIOS):
        curso = comun.curso_de_codigo(codigo)
        if not curso or any(t.get("cursoId") == curso["id"] for t in d.temas_foro):
            continue
        gente = [p for p in d.participantes_de_curso(curso) if p["id"] != curso.get("docenteId")]
        docente = d.buscar_persona(curso.get("docenteId"))
        if not gente or not docente:
            continue
        titulo, texto = GENERICOS[curso["id"] % len(GENERICOS)]
        mensajes = [{
            "id": d.nuevo_id_mensaje_foro(),
            "autorId": gente[0]["id"],
            "texto": texto,
            "fecha": comun.horas(18 + curso["id"] % 40),
            "votos": [],
        }, {
            "id": d.nuevo_id_mensaje_foro(),
            "autorId": docente["id"],
            "texto": "Lo contesto acá así queda para todos: entra hasta el final de la unidad "
                     "2, con los ejercicios de la guía incluidos. Lo de la unidad 3 se toma en "
                     "el segundo parcial.",
            "fecha": comun.horas(16 + curso["id"] % 40),
            "votos": [g["id"] for g in gente[:2]],
        }]
        cuenta.anotar("temas del foro", _tema(curso, titulo, gente[0], mensajes))


# ===================== Mensajes =====================
CHARLAS = [
    (SANTIAGO, MARIA, [
        (SANTIAGO, "Hola profe, una consulta sobre el trabajo práctico: ¿la lista tiene que ser "
                   "doblemente enlazada o alcanza con simple?", 26),
        (MARIA, "Hola Santiago. Con simple alcanza. Si la hacés doble suma, pero no es "
                "obligatorio.", 25),
        (MARIA, "Ah, y acordate de que el informe va en el mismo archivo, al final.", 25),
        (SANTIAGO, "Perfecto, gracias. Lo subo mañana.", 24),
    ]),
    (SANTIAGO, CLAUDIA, [
        (SANTIAGO, "Buenas tardes. Falté a la clase del martes por un trámite y quería saber si "
                   "puedo presentar la constancia para justificar.", 50),
        (CLAUDIA, "Sí, subila en la sección de asistencias del módulo y la reviso. Con una "
                  "falta no corrés riesgo, igual.", 48),
    ]),
    ("lucia.acosta@campustfi.edu.ar", SANTIAGO, [
        ("lucia.acosta@campustfi.edu.ar", "¿Armamos grupo para el TP de Programación? Somos dos "
                                          "y nos falta uno.", 8),
        (SANTIAGO, "Dale, me sumo. ¿Arrancamos el sábado?", 7),
        ("lucia.acosta@campustfi.edu.ar", "Sábado a las 10 en la biblioteca, sala 2.", 6),
    ]),
    (MARIA, "pablo.ruiz@campustfi.edu.ar", [
        (MARIA, "Pablo, ¿coordinamos para que el parcial de Bases no caiga la misma semana que "
                "el de Programación II? Los chicos de segundo están con los dos.", 72),
        ("pablo.ruiz@campustfi.edu.ar", "Sí, lo corro una semana. Lo cargo hoy en el calendario "
                                        "del campus.", 70),
    ]),
]


def _charlas(cuenta: comun.Cuenta) -> None:
    for correo_a, correo_b, intercambio in CHARLAS:
        a, b = comun.persona_por_correo(correo_a), comun.persona_por_correo(correo_b)
        if not a or not b:
            continue
        mensajes = []
        for correo, texto, hace in intercambio:
            quien = comun.persona_por_correo(correo)
            if not quien:
                continue
            mensajes.append({
                "id": d.nuevo_id_mensaje(),
                "deId": quien["id"],
                "texto": texto,
                "fecha": comun.horas(hace),
                # El último mensaje de la otra persona queda sin leer: es lo
                # que enciende la campanita, y con todo leído la pantalla de
                # Mensajes no muestra para qué sirve.
                "leido": True,
            })
        if mensajes and mensajes[-1]["deId"] != a["id"]:
            mensajes[-1]["leido"] = False

        _, creada = comun.asegurar(
            d.conversaciones,
            lambda c: sorted(c.get("entre") or []) == sorted([a["id"], b["id"]]),
            lambda: {
                "id": d.nuevo_id_conversacion(),
                "entre": [a["id"], b["id"]],
                "mensajes": mensajes,
            },
        )
        cuenta.anotar("conversaciones", creada)


# ===================== Eventos de la facultad =====================
EVENTOS = [
    ("evento", "Jornada de Ciencias Exactas", 5, "09:00", "17:00", "Pabellón central"),
    ("evento", "Charla: salida laboral en sistemas", 3, "17:00", "19:00", "Salón de actos"),
    ("evento", "Cierre de la inscripción a materias", 11, "23:59", "23:59", "Campus virtual"),
    ("evento", "Apertura de la inscripción a mesas de diciembre", 1, "08:00", "23:59",
     "Campus virtual"),
    ("evento", "Taller de uso del campus para ingresantes", -6, "10:00", "11:00", "Lab. 1"),
    ("evento", "Asamblea de estudiantes", -4, "14:00", "18:00", "Aula magna"),
    ("evento", "Acto de colación de grado", 24, "19:00", "21:00", "Teatro Vera"),
    ("evento", "Muestra de trabajos finales integradores", 17, "16:00", "20:00",
     "Pabellón central"),
]


def _eventos(cuenta: comun.Cuenta) -> None:
    for tipo, titulo, cuando, desde, hasta, lugar in EVENTOS:
        _, creado = comun.asegurar(
            d.eventos,
            lambda e, titulo=titulo: comun.plano(e.get("titulo")) == comun.plano(titulo),
            lambda tipo=tipo, titulo=titulo, cuando=cuando, desde=desde, hasta=hasta, lugar=lugar: {
                "id": d.nuevo_id_evento(),
                "tipo": tipo,
                "titulo": titulo,
                "fecha": comun.dias(cuando),
                "desde": desde,
                "hasta": hasta,
                "lugar": lugar,
            },
        )
        cuenta.anotar("eventos de la facultad", creado)

    # Los parciales, que son del módulo y no de la facultad: van con `cursoId`
    # para que el calendario los pinte con el color de la materia.
    from . import modulos as mod

    for orden, codigo in enumerate(sorted(mod.COMPLETOS)):
        curso = comun.curso_de_codigo(codigo)
        if not curso:
            continue
        for numero, cuando, hora in ((1, -18 + orden, "18:00"), (2, 9 + orden, "18:00")):
            titulo = f"{'Primer' if numero == 1 else 'Segundo'} parcial · {curso['nombre']}"
            _, creado = comun.asegurar(
                d.eventos,
                lambda e, titulo=titulo: comun.plano(e.get("titulo")) == comun.plano(titulo),
                lambda titulo=titulo, cuando=cuando, hora=hora, curso=curso: {
                    "id": d.nuevo_id_evento(),
                    "tipo": "examen",
                    "titulo": titulo,
                    "cursoId": curso["id"],
                    "fecha": comun.dias(cuando),
                    "desde": hora,
                    "hasta": f"{int(hora[:2]) + 2:02d}:00",
                    "lugar": "Aula asignada por la cátedra",
                },
            )
            cuenta.anotar("exámenes en el calendario", creado)


def armar(cuenta: comun.Cuenta, estudiantes: list[int]) -> None:
    _novedades(cuenta, estudiantes)
    _foro(cuenta)
    _charlas(cuenta)
    _eventos(cuenta)
