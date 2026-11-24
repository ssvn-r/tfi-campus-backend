"""El contenido de cada módulo: secciones, páginas, documentos, trabajos y anuncios.

De dónde sale el texto
----------------------
De `catalogo.py`. Cada materia trae su fundamentación, sus unidades y su
bibliografía, y con eso se arman el programa en PDF, el cronograma, una sección
por unidad con su apunte y los trabajos prácticos. Nada dice «contenido de
ejemplo»: lo que se lee en la pantalla es el programa de la materia.

Tres profundidades, y por qué
-----------------------------
Cargar cuarenta y dos módulos con cinco unidades cada uno sería un campus de
doscientas secciones que nadie va a abrir, y media hora de subidas a R2. Se
cargan a fondo los módulos que se van a mostrar —los que cursa el estudiante de
la demostración y los que dicta la docente—, a medias el resto de Sistemas, y
con lo mínimo las dos carreras nuevas: programa, bienvenida y las primeras
unidades. Un módulo con el programa y la bienvenida ya no se ve vacío, que es
lo que importa cuando alguien entra a mirar.
"""

from __future__ import annotations

from .. import datos as d
from . import archivos, catalogo, comun

# Los módulos que se cargan a fondo: los seis que cursa Santiago, los cuatro
# que dicta María y dos más para que la grilla de segundo año tenga adentro
# algo que mirar.
COMPLETOS = {
    "SIS-102", "SIS-103", "SIS-104", "SIS-105", "SIS-106", "SIS-107",
    "ALG-2", "PROG-2", "PROG-3", "BD-1", "IS-1",
}
# El resto de Sistemas: programa, cronograma y las dos primeras unidades.
MEDIOS = {"SIS-101", "MAT-3", "RED-1", "SO-1", "BD-2", "MAT-4", "IS-2", "RED-2"}

CARRERAS = {1: "Licenciatura en Sistemas de Información",
            2: "Profesorado en Matemática",
            3: "Licenciatura en Ciencias Químicas"}

ORDINALES = ["", "primera", "segunda", "tercera", "cuarta", "quinta", "sexta"]


def profundidad(codigo: str) -> str:
    if codigo in COMPLETOS:
        return "completo"
    if codigo in MEDIOS:
        return "medio"
    return "basico"


def _unidades_a_cargar(codigo: str, cuantas: int) -> int:
    return {"completo": cuantas, "medio": 2, "basico": 2}[profundidad(codigo)]


def partes_de_unidad(texto: str) -> tuple[str, list[str]]:
    """Separa «Título. Subtema, subtema y subtema.» en sus dos partes."""
    titulo, _, resto = texto.partition(". ")
    sueltos = [
        p.strip(" .")
        for p in resto.replace(" y ", ", ").split(",")
        if p.strip(" .")
    ]
    return titulo.strip(" ."), sueltos


# ===================== Los documentos =====================
def _bloques_programa(materia: dict, ficha: dict, docente: dict | None) -> list[tuple[str, str]]:
    plan = d.buscar_en(d.planes_estudio, materia.get("planId")) or {}
    bloques: list[tuple[str, str]] = [
        ("titulo", f"Programa de {materia['nombre']}"),
        ("bajada", f"{CARRERAS.get(materia.get('carreraId'), '')} · "
                   f"{plan.get('nombre', 'Plan vigente')} · ciclo {d.ahora().year}"),
        ("campo", f"Código: {materia['codigo']}"),
        ("campo", f"Cátedra: {docente['nombre'] if docente else 'Sin asignar'}"),
        ("campo", f"Año y cuatrimestre: {materia['anio']}.º año · "
                  f"{materia['cuatrimestre']}.er cuatrimestre"),
        ("campo", f"Carga horaria: {materia.get('cargaHoraria') or '—'} horas"),
        ("campo", f"Modalidad: {materia.get('modalidad') or 'Presencial'}"),
        ("seccion", "Fundamentación"),
        ("texto", ficha["resumen"]),
        ("seccion", "Unidades"),
    ]
    for numero, unidad in enumerate(ficha["unidades"], start=1):
        bloques.append(("lista", f"Unidad {numero}. {unidad}"))

    correlativas = _texto_correlativas(materia)
    if correlativas:
        bloques += [("seccion", "Correlatividades"), *[("lista", c) for c in correlativas]]

    bloques += [
        ("seccion", "Régimen de cursada"),
        ("texto",
         "Para regularizar hay que aprobar los dos parciales —hay un recuperatorio por "
         "parcial—, entregar los trabajos prácticos obligatorios y cumplir con el 70 % de "
         "asistencia. Quien no alcance la regularidad rinde la materia en condición de libre, "
         "con examen escrito y oral sobre el programa completo."),
        ("seccion", "Evaluación"),
        ("texto",
         "La nota de cursada sale de los parciales y de los trabajos prácticos. El final es "
         "escrito y oral, y se aprueba con 6 (seis). Las fechas de los parciales y de los "
         "trabajos están en el cronograma, que se publica en este mismo módulo."),
        ("seccion", "Bibliografía"),
    ]
    for libro in ficha["biblio"]:
        bloques.append(("lista", libro))
    return bloques


def _texto_correlativas(materia: dict) -> list[str]:
    salida = []
    for para, etiqueta in (("cursar", "Para cursar"), ("rendir", "Para rendir el final")):
        grupo = (materia.get("correlativas") or {}).get(para) or {}
        requisitos = grupo.get("requisitos") or []
        if not requisitos:
            continue
        nombres = []
        for requisito in requisitos:
            otra = d.buscar_en(d.materias_plan, requisito.get("materiaId"))
            if otra:
                nombres.append(f"{otra['nombre']} ({str(requisito.get('condicion')).lower()})")
        if nombres:
            unidas = " y ".join(nombres) if grupo.get("modo") == "todas" else " o ".join(nombres)
            salida.append(f"{etiqueta}: {unidas}.")
    return salida


def _bloques_cronograma(materia: dict, ficha: dict) -> list[tuple[str, str]]:
    bloques: list[tuple[str, str]] = [
        ("titulo", f"Cronograma · {materia['nombre']}"),
        ("bajada", f"{CARRERAS.get(materia.get('carreraId'), '')} · ciclo {d.ahora().year}"),
        ("texto",
         "El cronograma es orientativo: si una clase se suspende, las semanas siguientes se "
         "corren y se avisa por los anuncios del módulo."),
        ("seccion", "Clases por semana"),
    ]
    semana = 1
    for numero, unidad in enumerate(ficha["unidades"], start=1):
        titulo, _ = partes_de_unidad(unidad)
        bloques.append(("campo", f"Semanas {semana} y {semana + 1}: Unidad {numero} — {titulo}"))
        semana += 2
    bloques += [
        ("seccion", "Evaluaciones"),
        ("campo", "Primer parcial: semana 7, en el horario de clase"),
        ("campo", "Recuperatorio del primer parcial: semana 9"),
        ("campo", "Segundo parcial: semana 14, en el horario de clase"),
        ("campo", "Recuperatorio del segundo parcial: semana 16"),
        ("seccion", "Trabajos prácticos"),
        ("texto",
         "Los trabajos se entregan por el campus, en la sección de la unidad que corresponde. "
         "La entrega vale la última versión subida: si te equivocaste de archivo, volvés a "
         "entregar y listo."),
    ]
    return bloques


def _bloques_apunte(materia: dict, ficha: dict, numero: int) -> list[tuple[str, str]]:
    unidad = ficha["unidades"][numero - 1]
    titulo, subtemas = partes_de_unidad(unidad)
    ordinal = ORDINALES[numero] if numero < len(ORDINALES) else f"{numero}.ª"
    bloques: list[tuple[str, str]] = [
        ("titulo", f"Unidad {numero} · {titulo}"),
        ("bajada", f"{materia['nombre']} · apunte de cátedra"),
        ("texto",
         f"Este apunte acompaña la {ordinal} unidad de {materia['nombre']}. No reemplaza la "
         f"clase ni la bibliografía: ordena lo que se vio, marca dónde conviene detenerse y "
         f"deja la práctica mínima que hay que tener hecha antes del parcial."),
        ("seccion", "De qué se trata"),
        ("texto", unidad if unidad.endswith(".") else unidad + "."),
    ]
    if subtemas:
        bloques.append(("seccion", "Los puntos de la unidad"))
        for subtema in subtemas:
            bloques.append(("lista", subtema[0].upper() + subtema[1:] + "."))
    bloques += [
        ("seccion", "Para no perderse"),
        ("texto",
         "Lo que más cuesta en esta unidad no son las cuentas: es decidir qué herramienta "
         "corresponde a cada problema. Antes de resolver, escribí en una línea qué te están "
         "pidiendo y con qué contás. Si eso no se puede escribir, todavía no hay que empezar a "
         "resolver."),
        ("seccion", "Práctica mínima"),
        ("lista", "Resolvé los ejercicios 1 a 8 de la guía de la unidad."),
        ("lista", "Rehacé sin mirar el ejemplo que se desarrolló en clase."),
        ("lista", "Anotá las dudas que te queden y traelas a la clase de consulta."),
        ("seccion", "Bibliografía de la unidad"),
    ]
    for libro in ficha["biblio"]:
        bloques.append(("lista", libro))
    return bloques


def _bloques_guia_tp(materia: dict, ficha: dict, numero: int, consigna: str) -> list[tuple[str, str]]:
    titulo, _ = partes_de_unidad(ficha["unidades"][min(numero, len(ficha["unidades"])) - 1])
    return [
        ("titulo", f"Trabajo práctico {numero} · {materia['nombre']}"),
        ("bajada", f"Unidad {numero} — {titulo}"),
        ("seccion", "Consigna"),
        ("texto", consigna),
        ("seccion", "Qué se entrega"),
        ("lista", "Un único archivo PDF con la resolución y las decisiones que tomaron."),
        ("lista", "Si hay código o planillas, van en el mismo archivo, al final, como anexo."),
        ("lista", "La primera página lleva el nombre completo y el legajo de cada integrante."),
        ("seccion", "Cómo se corrige"),
        ("texto",
         "Se evalúa que el resultado sea correcto y que esté justificado. Un resultado bien "
         "sin justificación no aprueba, y una justificación bien escrita con un error de "
         "cálculo no desaprueba: lo que se mide es el razonamiento."),
        ("seccion", "Entrega"),
        ("texto",
         "Por el campus, en esta misma sección. Vale la última versión subida. Se puede "
         "entregar después de la fecha, pero la entrega queda marcada como tardía y eso lo "
         "mira la cátedra al corregir."),
    ]


# ===================== Las secciones del módulo =====================
def _carpeta(curso: dict, titulo: str, descripcion: str | None) -> tuple[dict, bool]:
    carpetas = d.asegurar_contenido(curso)
    return comun.asegurar(
        carpetas,
        lambda c: comun.plano(c.get("titulo")) == comun.plano(titulo),
        lambda: {
            "id": d.nuevo_id_carpeta(),
            "titulo": titulo,
            "descripcion": descripcion,
            "items": [],
        },
    )


def _item(carpeta: dict, curso: dict, titulo: str, armar) -> tuple[dict, bool]:
    return comun.asegurar(
        carpeta["items"],
        lambda i: comun.plano(i.get("titulo")) == comun.plano(titulo),
        lambda: {"id": f"{curso['id']}-{d.nuevo_id_carpeta()}", **armar()},
    )


def _item_pagina(carpeta: dict, curso: dict, titulo: str, parrafos: list[str]) -> bool:
    _, creado = _item(
        carpeta, curso, titulo,
        lambda: {"tipo": "pagina", "titulo": titulo, "cuerpo": parrafos},
    )
    return creado


def _item_archivo(
    carpeta: dict, curso: dict, titulo: str, nombre: str, bloques: list, docente_id: int | None
) -> bool:
    """Un elemento de tipo archivo, con el PDF subido de verdad a R2."""
    existente = next(
        (i for i in carpeta["items"] if comun.plano(i.get("titulo")) == comun.plano(titulo)), None
    )
    if existente and existente.get("archivo"):
        return False

    item_id = existente["id"] if existente else f"{curso['id']}-{d.nuevo_id_carpeta()}"
    ficha = archivos.subir_pdf(
        "modulos", (curso["id"], item_id), nombre, bloques,
        persona_id=docente_id, registro_id=item_id,
    )
    nuevo = {
        "id": item_id,
        "tipo": "archivo",
        "titulo": titulo,
        "formato": "PDF",
        "tamano": archivos.peso(ficha),
        "archivo": ficha,
    }
    if existente:
        existente.update(nuevo)
        return False
    carpeta["items"].append(nuevo)
    return True


def _item_tarea(
    carpeta: dict, curso: dict, titulo: str, *, limite: str, publicada: str,
    consigna: str | None = None, modalidad: str = "virtual", formato: str = "entrega",
    preguntas: list | None = None,
) -> tuple[dict | None, bool]:
    """El elemento y su trabajo. El trabajo vive en `tareas`, no en el ítem."""
    existente = next(
        (i for i in carpeta["items"] if comun.plano(i.get("titulo")) == comun.plano(titulo)), None
    )
    if existente:
        return d.buscar_tarea(existente.get("tareaId")), False

    tarea = {
        "id": d.nuevo_id_tarea(),
        "cursoId": curso["id"],
        "titulo": titulo,
        "publicada": publicada,
        "fechaLimite": limite,
        "entregada": False,
        "cerrada": None,
        "consigna": consigna,
        "modalidad": modalidad,
        "formato": formato if modalidad == "virtual" else "presencial",
        "preguntas": preguntas or [],
    }
    d.tareas.append(tarea)
    carpeta["items"].append(
        {
            "id": f"{curso['id']}-{d.nuevo_id_carpeta()}",
            "tipo": "tarea",
            "titulo": titulo,
            "tareaId": tarea["id"],
        }
    )
    return tarea, True


def _item_tablero(carpeta: dict, curso: dict, titulo: str, columnas: list[dict]) -> bool:
    _, creado = _item(
        carpeta, curso, titulo,
        lambda: {"tipo": "tablero", "titulo": titulo, "columnas": columnas},
    )
    return creado


# ===================== Anuncios =====================
def _anuncio(curso: dict, titulo: str, cuerpo: str, autor: dict, cuando: str) -> bool:
    lista = d.anuncios.setdefault(curso["id"], [])
    _, creado = comun.asegurar(
        lista,
        lambda a: comun.plano(a.get("titulo")) == comun.plano(titulo),
        lambda: {
            "id": d.nuevo_id_anuncio(),
            "titulo": titulo,
            "cuerpo": cuerpo,
            "autor": autor["nombre"],
            "autorId": autor["id"],
            "fecha": cuando,
        },
    )
    return creado


# ===================== Clases semanales =====================
def _clases(curso: dict, ficha: dict, cuenta: comun.Cuenta) -> None:
    """El horario del módulo, que es lo que el calendario expande a cada semana."""
    for dia, desde, hasta, aula in ficha.get("horario") or []:
        _, creada = comun.asegurar(
            d.clases,
            lambda c, dia=dia, desde=desde: (
                c.get("cursoId") == curso["id"] and c.get("dia") == dia and c.get("desde") == desde
            ),
            lambda dia=dia, desde=desde, hasta=hasta, aula=aula: {
                "cursoId": curso["id"],
                "dia": dia,
                "desde": desde,
                "hasta": hasta,
                "aula": aula,
            },
        )
        cuenta.anotar("horarios de clase", creada)


# ===================== Los cuestionarios escritos a mano =====================
# Solo los de las materias de María Gómez, que es la cuenta con la que se
# muestra el lado docente. Un cuestionario generado a partir del título de la
# unidad daría preguntas que no se pueden contestar, y eso se nota en la
# primera que se abre.
CUESTIONARIOS: dict[str, dict] = {
    "SIS-103": {
        "titulo": "Autoevaluación: estructuras de control y funciones",
        "consigna": "Diez minutos, una sola vez. Es para que midas cómo venís antes del parcial.",
        "preguntas": [
            ("¿Qué devuelve una función que llega al final sin ejecutar ningún return?",
             ["Cero", "None", "El último valor calculado", "Lanza un error"], 1),
            ("¿Cuántas veces se ejecuta el cuerpo de «for i in range(2, 10, 3)»?",
             ["2", "3", "4", "8"], 1),
            ("Una variable definida dentro de una función…",
             ["Se puede usar en todo el programa",
              "Existe solo mientras la función se ejecuta",
              "Reemplaza a la global del mismo nombre para siempre",
              "No se puede modificar"], 1),
            ("¿Cuál de estas condiciones es verdadera si x vale 5?",
             ["x > 5", "x != 5", "0 < x <= 5", "not x"], 2),
        ],
    },
    "ALG-2": {
        "titulo": "Autoevaluación: complejidad y recursividad",
        "consigna": "Diez minutos. Se puede rendir una sola vez.",
        "preguntas": [
            ("¿Cuál es el costo de buscar un elemento en una lista enlazada sin ordenar?",
             ["O(1)", "O(log n)", "O(n)", "O(n²)"], 2),
            ("¿Qué le falta a una función recursiva que no termina nunca?",
             ["Un caso base", "Un bucle", "Una variable global", "Un try/except"], 0),
            ("En un árbol binario de búsqueda equilibrado, buscar cuesta…",
             ["O(1)", "O(log n)", "O(n)", "O(n log n)"], 1),
            ("¿Qué estructura conviene para deshacer acciones en orden inverso?",
             ["Una cola", "Una pila", "Un árbol", "Un diccionario"], 1),
        ],
    },
    "PROG-2": {
        "titulo": "Autoevaluación: listas enlazadas y objetos",
        "consigna": "Diez minutos, una sola vez. Las respuestas se comentan en la clase siguiente.",
        "preguntas": [
            ("Para borrar un nodo del medio de una lista simplemente enlazada hace falta…",
             ["El nodo siguiente", "El nodo anterior", "Recorrerla dos veces", "Nada más"], 1),
            ("En una lista doblemente enlazada, cada nodo guarda…",
             ["Solo el siguiente", "Solo el anterior",
              "El anterior y el siguiente", "Todos los nodos"], 2),
            ("¿Qué significa encapsular?",
             ["Esconder los datos detrás de métodos que los cuidan",
              "Poner todo en una sola clase",
              "Usar herencia siempre que se pueda",
              "Evitar las funciones"], 0),
            ("Una cola se usa cuando…",
             ["El último que entra es el primero que sale",
              "El primero que entra es el primero que sale",
              "Hay que ordenar los elementos",
              "Se necesita acceso directo por posición"], 1),
        ],
    },
    "PROG-3": {
        "titulo": "Autoevaluación: herencia, polimorfismo y patrones",
        "consigna": "Diez minutos. Entra lo visto en las unidades 1 a 3.",
        "preguntas": [
            ("Conviene usar composición en lugar de herencia cuando…",
             ["La relación es «tiene un» y no «es un»",
              "Hay más de dos clases",
              "La clase padre es abstracta",
              "Nunca: la herencia siempre es mejor"], 0),
            ("¿Qué permite el polimorfismo?",
             ["Que una clase tenga varios constructores",
              "Tratar objetos distintos a través de una misma interfaz",
              "Heredar de más de una clase",
              "Cambiar el tipo de una variable"], 1),
            ("El patrón Singleton sirve para…",
             ["Crear objetos sin conocer su clase",
              "Garantizar una única instancia de una clase",
              "Recorrer una colección",
              "Separar la interfaz de la implementación"], 1),
            ("Una clase que hace demasiadas cosas incumple…",
             ["El principio de responsabilidad única",
              "El principio de sustitución",
              "La ley de Demeter",
              "El patrón Observer"], 0),
        ],
    },
}


def _preguntas(definicion: dict) -> list[dict]:
    return [
        {
            "id": numero,
            "texto": texto,
            "opciones": list(opciones),
            "correcta": correcta,
            "puntaje": 1,
        }
        for numero, (texto, opciones, correcta) in enumerate(definicion["preguntas"], start=1)
    ]


# ===================== Las consignas de los trabajos =====================
def _consigna(materia: dict, ficha: dict, numero: int) -> str:
    titulo, subtemas = partes_de_unidad(ficha["unidades"][min(numero, len(ficha["unidades"])) - 1])
    foco = subtemas[0] if subtemas else titulo
    return (
        f"Resolvé la guía de la unidad {numero} de {materia['nombre']} y entregá un informe que "
        f"muestre cómo llegaste a cada resultado. El eje del trabajo es {foco.lower()}: no "
        f"alcanza con el resultado final, hay que justificar por qué el camino elegido es "
        f"válido. Se entrega en grupos de hasta dos personas."
    )


def _tablero_de(materia: dict, ficha: dict, gente: list[dict], docente: dict | None) -> list[dict]:
    """El tablero de consultas, con preguntas que miran al programa de verdad."""
    u1, _ = partes_de_unidad(ficha["unidades"][0])
    u2, _ = partes_de_unidad(ficha["unidades"][min(1, len(ficha["unidades"]) - 1)])
    alumnos = [p["nombre"] for p in gente] or ["Estudiante"]
    return [
        {
            "titulo": "Preguntas",
            "publicaciones": [
                {"id": 1, "autor": alumnos[0], "fecha": comun.horas(26),
                 "texto": f"¿El parcial entra hasta {u2.lower()} o hasta la unidad siguiente?"},
                {"id": 2, "autor": alumnos[min(1, len(alumnos) - 1)], "fecha": comun.horas(9),
                 "texto": "¿El trabajo práctico se puede hacer de a dos o es individual?"},
            ],
        },
        {
            "titulo": "Respondidas",
            "publicaciones": [
                {"id": 3, "autor": alumnos[min(2, len(alumnos) - 1)], "fecha": comun.horas(70),
                 "texto": f"¿Dónde está el apunte de {u1.lower()}?"},
                {"id": 4, "autor": (docente or {}).get("nombre", "Cátedra"),
                 "fecha": comun.horas(68),
                 "texto": "En la sección de la unidad 1, junto con la guía de ejercicios."},
            ],
        },
    ]


def armar(cuenta: comun.Cuenta, por_comision: dict[str, list[int]]) -> dict:
    """Carga el contenido de todos los módulos. Devuelve los trabajos creados.

    Los trabajos los necesita `academico.py` para las entregas y las notas: se
    crean acá, donde se sabe en qué sección vive cada uno.
    """
    creados: dict[str, list[dict]] = {}

    for materia in sorted(d.materias_plan, key=lambda m: (m.get("carreraId") or 0, m.get("id"))):
        codigo = materia.get("codigo")
        ficha = catalogo.CATALOGO.get(codigo)
        if not ficha:
            continue
        curso = d.buscar_curso(materia.get("cursoId"))
        if not curso:
            continue

        nivel = profundidad(codigo)
        docente = d.buscar_persona(curso.get("docenteId"))
        docente_id = docente["id"] if docente else None
        gente = [p for p in d.participantes_de_curso(curso) if p["id"] != docente_id]
        creados[codigo] = []

        # ---------- Información del módulo ----------
        info, creada = _carpeta(
            curso, "Información del módulo",
            "Bienvenida, programa de la materia y cronograma de cursada",
        )
        cuenta.anotar("secciones", creada)

        cuenta.anotar("páginas", _item_pagina(info, curso, "Bienvenida al módulo", [
            f"Bienvenidos a {materia['nombre']}. {ficha['resumen']}",
            "El módulo está organizado por unidades: en cada sección vas a encontrar el apunte "
            "de la cátedra, la guía de ejercicios y, cuando corresponda, el trabajo práctico "
            "con su fecha de entrega. Lo que se sube queda avisado en los anuncios.",
            "Las consultas van al tablero del módulo o al foro, no por mensaje privado: así la "
            "respuesta le sirve a todo el curso. Para algo personal —una justificación de "
            "inasistencia, un problema con una entrega— sí usá Mensajes.",
        ]))

        cuenta.anotar("documentos", _item_archivo(
            info, curso, "Programa de la materia",
            f"Programa {codigo} {materia['nombre']}",
            _bloques_programa(materia, ficha, docente), docente_id,
        ))

        if nivel != "basico":
            cuenta.anotar("documentos", _item_archivo(
                info, curso, "Cronograma de clases y evaluaciones",
                f"Cronograma {codigo}", _bloques_cronograma(materia, ficha), docente_id,
            ))

        # ---------- Una sección por unidad ----------
        cuantas = _unidades_a_cargar(codigo, len(ficha["unidades"]))
        for numero in range(1, cuantas + 1):
            titulo_unidad, subtemas = partes_de_unidad(ficha["unidades"][numero - 1])
            carpeta, creada = _carpeta(
                curso, f"Unidad {numero} · {titulo_unidad}",
                ", ".join(subtemas[:3]) or None,
            )
            cuenta.anotar("secciones", creada)

            cuenta.anotar("documentos", _item_archivo(
                carpeta, curso, f"Apunte de la unidad {numero}",
                f"Apunte U{numero} {codigo}",
                _bloques_apunte(materia, ficha, numero), docente_id,
            ))

            if nivel == "completo":
                cuenta.anotar("páginas", _item_pagina(
                    carpeta, curso, f"Guía de lectura de la unidad {numero}",
                    [
                        f"Antes de la clase: leé el apunte de la unidad {numero} y marcá lo que "
                        f"no te cierre. No hace falta entenderlo todo de entrada; hace falta "
                        f"saber qué no entendiste.",
                        "Después de la clase: rehacé el ejemplo que se desarrolló en el pizarrón "
                        "sin mirar los apuntes. Si te sale, seguí con la guía de ejercicios.",
                    ] + ([f"Lo que más se usa después: {subtemas[0].lower()}."] if subtemas else []),
                ))

        # ---------- Trabajos prácticos ----------
        if nivel == "completo":
            unidades_tp = [1, 2]
            fechas = [(comun.dias(-26), comun.dias(-6)), (comun.dias(-5), comun.dias(4))]
        elif nivel == "medio":
            unidades_tp = [1]
            fechas = [(comun.dias(-8), comun.dias(7))]
        else:
            unidades_tp = [1]
            fechas = [(comun.dias(-6), comun.dias(9))]

        for orden, numero in enumerate(unidades_tp, start=1):
            carpeta_tp, _ = _carpeta(
                curso, f"Unidad {numero} · {partes_de_unidad(ficha['unidades'][numero - 1])[0]}",
                None,
            )
            publicada, limite = fechas[orden - 1]
            titulo_tp = f"Trabajo práctico {orden}: {partes_de_unidad(ficha['unidades'][numero - 1])[0]}"
            consigna = _consigna(materia, ficha, numero)

            if nivel == "completo":
                cuenta.anotar("documentos", _item_archivo(
                    carpeta_tp, curso, f"Guía del trabajo práctico {orden}",
                    f"Guia TP{orden} {codigo}",
                    _bloques_guia_tp(materia, ficha, numero, consigna), docente_id,
                ))

            tarea, creada = _item_tarea(
                carpeta_tp, curso, titulo_tp,
                limite=limite, publicada=publicada, consigna=consigna,
            )
            cuenta.anotar("trabajos prácticos", creada)
            if tarea:
                creados[codigo].append(tarea)

        # ---------- El cuestionario, donde está escrito ----------
        definicion = CUESTIONARIOS.get(codigo)
        if definicion:
            carpeta_q, _ = _carpeta(curso, "Autoevaluaciones",
                                    "Cuestionarios de opción múltiple, para medirse antes del parcial")
            tarea, creada = _item_tarea(
                carpeta_q, curso, definicion["titulo"],
                limite=comun.dias(6), publicada=comun.dias(-4),
                consigna=definicion["consigna"], formato="cuestionario",
                preguntas=_preguntas(definicion),
            )
            cuenta.anotar("cuestionarios", creada)
            if tarea:
                creados[codigo].append(tarea)

        # ---------- El tablero de consultas ----------
        if nivel == "completo":
            carpeta_c, creada = _carpeta(curso, "Consultas",
                                         "Preguntas, comentarios e inquietudes sobre la materia")
            cuenta.anotar("secciones", creada)
            cuenta.anotar("tableros", _item_tablero(
                carpeta_c, curso, "Preguntas, comentarios e inquietudes",
                _tablero_de(materia, ficha, gente, docente),
            ))

        # ---------- Anuncios ----------
        if docente:
            u1 = partes_de_unidad(ficha["unidades"][0])[0]
            cuenta.anotar("anuncios", _anuncio(
                curso, f"Ya está el programa de {materia['nombre']}",
                "Subí el programa y el cronograma a la sección «Información del módulo». "
                "Léanlos en la primera semana: ahí están las fechas de los parciales y el "
                "régimen de cursada.",
                docente, comun.dias(-30),
            ))
            if nivel != "basico":
                cuenta.anotar("anuncios", _anuncio(
                    curso, f"Apunte de la unidad 1 disponible",
                    f"Está en la sección de la unidad 1, junto con la guía de ejercicios. "
                    f"Es el material de {u1.lower()}.",
                    docente, comun.dias(-12),
                ))
            if nivel == "completo":
                cuenta.anotar("anuncios", _anuncio(
                    curso, "Fechas de los parciales",
                    "El primer parcial es en la semana 7 y el segundo en la semana 14, los dos "
                    "en el horario de clase. Los recuperatorios, dos semanas después de cada "
                    "parcial. Las fechas exactas están en el calendario del campus.",
                    docente, comun.dias(-9),
                ))
                cuenta.anotar("anuncios", _anuncio(
                    curso, "La clase de esta semana cambia de aula",
                    "Nos vemos en el laboratorio, no en el aula de siempre: vamos a trabajar con "
                    "las máquinas. Lleven la notebook si la tienen.",
                    docente, comun.horas(20),
                ))

        _clases(curso, ficha, cuenta)

    return creados
