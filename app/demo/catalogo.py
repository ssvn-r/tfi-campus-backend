"""Qué enseña cada materia: lo que el campus muestra como contenido.

De acá sale casi todo lo demás. Con la fundamentación, las unidades y la
bibliografía de una materia se arman solos el programa en PDF, el cronograma,
las secciones del módulo, los apuntes de cada unidad y el material de la
biblioteca. Es la única parte que hay que escribir a mano, y es la que hace
que el campus no se vea relleno con «Lorem ipsum».

Cada entrada es la materia por su código:

    "resumen"   la fundamentación, un párrafo
    "unidades"  las unidades del programa, en orden
    "biblio"    la bibliografía obligatoria
    "catedra"   el correo de quien la tiene a cargo
    "horario"   cuándo se cursa, para el calendario y la ficha del módulo
"""

from __future__ import annotations

# Para no repetir el correo entero en cada materia.
MARIA = "maria.gomez@campustfi.edu.ar"
CLAUDIA = "claudia.ferreyra@campustfi.edu.ar"
PABLO = "pablo.ruiz@campustfi.edu.ar"
LAURA = "laura.benitez@campustfi.edu.ar"
DIEGO = "diego.fernandez@campustfi.edu.ar"
ANA = "ana.martinez@campustfi.edu.ar"
JORGE = "jorge.romero@campustfi.edu.ar"
SILVINA = "silvina.ojeda@campustfi.edu.ar"
MARCELO = "marcelo.ayala@campustfi.edu.ar"
GABRIELA = "gabriela.insaurralde@campustfi.edu.ar"
RAUL = "raul.cabrera@campustfi.edu.ar"
NOELIA = "noelia.villalba@campustfi.edu.ar"
RAMIRO = "ramiro.escobar@campustfi.edu.ar"
VERONICA = "veronica.leiva@campustfi.edu.ar"

# ===================== Licenciatura en Sistemas de Información =====================
CATALOGO: dict[str, dict] = {
    "SIS-101": {
        "catedra": ANA,
        "horario": [(2, "08:00", "11:00", "Aula 7"), (4, "08:00", "10:00", "Aula 7")],
        "resumen": (
            "Primera materia de la formación matemática de la carrera. Trabaja el álgebra "
            "vectorial y matricial como herramienta de cálculo y como lenguaje para describir "
            "objetos geométricos, con la computadora como ayuda para verificar resultados y no "
            "para reemplazar el razonamiento."
        ),
        "unidades": [
            "Vectores en el plano y en el espacio. Producto escalar y vectorial.",
            "Matrices y determinantes. Operaciones y propiedades.",
            "Sistemas de ecuaciones lineales. Método de Gauss y resolución por matrices.",
            "Rectas y planos. Distancias, ángulos y posiciones relativas.",
            "Cónicas y superficies cuádricas. Reconocimiento a partir de la ecuación.",
        ],
        "biblio": [
            "Grossman, S. — Álgebra lineal, 7.ª edición. McGraw-Hill.",
            "Anton, H. — Introducción al álgebra lineal. Limusa.",
        ],
    },
    "SIS-102": {
        "catedra": CLAUDIA,
        "horario": [(1, "18:00", "21:00", "Aula 12"), (3, "18:00", "20:00", "Aula 12")],
        "resumen": (
            "Introduce el cálculo en una variable: la idea de límite, la derivada como razón de "
            "cambio y la integral como acumulación. El énfasis está en interpretar qué mide cada "
            "concepto antes de calcularlo, porque es lo que después permite usarlo en problemas "
            "que no vienen escritos como ejercicio."
        ),
        "unidades": [
            "Funciones reales. Dominio, imagen y representación gráfica.",
            "Límite y continuidad. Indeterminaciones y asíntotas.",
            "Derivada. Reglas de derivación y aplicaciones al estudio de funciones.",
            "Integral indefinida. Métodos de integración.",
            "Integral definida. Áreas y teorema fundamental del cálculo.",
        ],
        "biblio": [
            "Stewart, J. — Cálculo de una variable, 8.ª edición. Cengage.",
            "Rabuffetti, H. — Introducción al análisis matemático. El Ateneo.",
        ],
    },
    "SIS-103": {
        "catedra": MARIA,
        "horario": [(2, "18:00", "22:00", "Lab. 3"), (5, "18:00", "20:00", "Aula 9")],
        "resumen": (
            "La materia donde se aprende a programar. Parte de la noción de algoritmo y llega a "
            "programas con funciones, arreglos y archivos, en Python. La consigna de la cátedra "
            "es que todo lo que se vea en el pizarrón se escriba y se corra en la máquina en la "
            "misma clase: programar es una práctica, no un contenido para leer."
        ),
        "unidades": [
            "Algoritmos, variables y tipos de datos. Entrada y salida.",
            "Estructuras de control: condicionales y repetición.",
            "Funciones. Parámetros, retorno y alcance de las variables.",
            "Arreglos, listas y cadenas de caracteres.",
            "Archivos de texto. Lectura, escritura y procesamiento de datos.",
        ],
        "biblio": [
            "Downey, A. — Piensa en Python, 2.ª edición. O'Reilly (edición libre).",
            "Joyanes Aguilar, L. — Fundamentos de programación. McGraw-Hill.",
        ],
    },
    "SIS-104": {
        "catedra": CLAUDIA,
        "horario": [(1, "18:00", "21:00", "Aula 12"), (4, "20:00", "22:00", "Aula 12")],
        "resumen": (
            "Continúa Análisis Matemático I con funciones de varias variables, series y "
            "ecuaciones diferenciales elementales. Es la base matemática de las materias de "
            "modelado y de las de probabilidad."
        ),
        "unidades": [
            "Sucesiones y series numéricas. Criterios de convergencia.",
            "Funciones de varias variables. Derivadas parciales y gradiente.",
            "Extremos de funciones de dos variables. Multiplicadores de Lagrange.",
            "Integrales dobles. Cálculo de volúmenes.",
            "Ecuaciones diferenciales de primer orden. Variables separables.",
        ],
        "biblio": [
            "Stewart, J. — Cálculo de varias variables. Cengage.",
            "Zill, D. — Ecuaciones diferenciales con aplicaciones. Cengage.",
        ],
    },
    "SIS-105": {
        "catedra": DIEGO,
        "horario": [(3, "18:00", "21:00", "Lab. de redes")],
        "resumen": (
            "Qué hay abajo del programa: cómo se representa la información, cómo está armado un "
            "procesador y por qué un programa puede ser lento sin que el algoritmo tenga nada "
            "malo. Se baja hasta el nivel de ensamblador para que la máquina deje de ser una "
            "caja negra."
        ),
        "unidades": [
            "Representación de la información. Sistemas de numeración y punto flotante.",
            "Álgebra de Boole y circuitos lógicos combinacionales.",
            "Arquitectura de von Neumann. Unidad de control y camino de datos.",
            "Lenguaje ensamblador. Instrucciones, registros y modos de direccionamiento.",
            "Jerarquía de memoria. Caché, memoria principal y entrada/salida.",
        ],
        "biblio": [
            "Tanenbaum, A. — Organización de computadoras, 6.ª edición. Pearson.",
            "Patterson, D. y Hennessy, J. — Estructura y diseño de computadores. Reverté.",
        ],
    },
    "SIS-106": {
        "catedra": SILVINA,
        "horario": [(5, "10:00", "12:00", "Aula 4")],
        "resumen": (
            "Lectura comprensiva de documentación técnica en inglés: manuales, mensajes de "
            "error, estándares y artículos. No se enseña gramática por la gramática: se trabaja "
            "sobre los textos con los que un informático se cruza todos los días."
        ),
        "unidades": [
            "Estrategias de lectura: skimming, scanning y vocabulario técnico.",
            "Tiempos verbales en documentación. Voz pasiva e imperativo.",
            "Manuales y referencias de API. Estructura y convenciones.",
            "Mensajes de error y rastreo de pilas: leer para diagnosticar.",
            "Resumen y traducción de artículos técnicos breves.",
        ],
        "biblio": [
            "Glendinning, E. y McEwan, J. — Oxford English for Information Technology.",
            "Documentación oficial de Python y de MDN Web Docs (material de clase).",
        ],
    },
    "ALG-2": {
        "catedra": MARIA,
        "horario": [(2, "14:00", "17:00", "Lab. 2"), (4, "14:00", "16:00", "Lab. 2")],
        "resumen": (
            "Cómo elegir la estructura de datos adecuada y cómo justificar esa elección. Se "
            "estudian las estructuras lineales y los árboles, los algoritmos de ordenamiento y "
            "búsqueda, y el costo de cada uno en tiempo y en memoria."
        ),
        "unidades": [
            "Análisis de algoritmos. Notación O y comparación de costos.",
            "Recursividad. Caso base, pila de llamadas y recursión múltiple.",
            "Listas enlazadas, pilas y colas. Implementación y aplicaciones.",
            "Árboles binarios de búsqueda. Recorridos y balanceo.",
            "Ordenamiento y búsqueda. Tablas de dispersión.",
        ],
        "biblio": [
            "Cormen, T. y otros — Introducción a los algoritmos. MIT Press.",
            "Weiss, M. — Estructuras de datos y algoritmos en Java. Addison-Wesley.",
        ],
    },
    "MAT-3": {
        "catedra": ANA,
        "horario": [(1, "14:00", "17:00", "Aula 5")],
        "resumen": (
            "Herramientas para trabajar con datos y con incertidumbre: probabilidad, variables "
            "aleatorias, muestreo e inferencia. Todas las prácticas se resuelven con datos "
            "reales y con planilla de cálculo, porque es así como se usa después."
        ),
        "unidades": [
            "Estadística descriptiva. Medidas de posición y de dispersión.",
            "Probabilidad. Condicional, independencia y teorema de Bayes.",
            "Variables aleatorias discretas y continuas. Distribuciones usuales.",
            "Muestreo y distribuciones muestrales. Teorema central del límite.",
            "Estimación e intervalos de confianza. Pruebas de hipótesis.",
        ],
        "biblio": [
            "Walpole, R. y Myers, R. — Probabilidad y estadística para ingeniería. Pearson.",
            "Devore, J. — Probabilidad y estadística. Cengage.",
        ],
    },
    "PROG-2": {
        "catedra": MARIA,
        "horario": [(2, "18:00", "22:00", "Lab. 3"), (5, "18:00", "20:00", "Aula 7")],
        "resumen": (
            "Segunda materia de programación: estructuras de datos dinámicas, modularización y "
            "una primera aproximación al diseño orientado a objetos. El objetivo es pasar de "
            "«el programa funciona» a «el programa se puede leer, probar y cambiar»."
        ),
        "unidades": [
            "Repaso de recursividad y memoria dinámica.",
            "Listas enlazadas simples, dobles y circulares.",
            "Pilas y colas. Aplicaciones: deshacer, recorridos y planificación.",
            "Introducción a objetos: clases, atributos y métodos.",
            "Manejo de errores y pruebas automatizadas.",
        ],
        "biblio": [
            "Weiss, M. — Estructuras de datos en Java. Addison-Wesley.",
            "Martin, R. — Código limpio. Anaya (capítulos 1 a 6).",
        ],
    },
    "BD-1": {
        "catedra": PABLO,
        "horario": [(4, "18:00", "22:00", "Aula 12")],
        "resumen": (
            "Del problema al modelo y del modelo a la base: entidad-relación, normalización y "
            "SQL. Se trabaja sobre un caso que acompaña toda la cursada —el de una biblioteca "
            "universitaria— para que el modelo se vea crecer y no quede en el pizarrón."
        ),
        "unidades": [
            "Modelo entidad-relación. Entidades, atributos y cardinalidades.",
            "Modelo relacional. Claves, integridad referencial y pasaje del MER.",
            "Normalización. Primera, segunda y tercera forma normal.",
            "SQL: consultas, agrupamientos y combinaciones de tablas.",
            "Transacciones, índices y vistas. Nociones de rendimiento.",
        ],
        "biblio": [
            "Elmasri, R. y Navathe, S. — Fundamentos de sistemas de bases de datos. Pearson.",
            "Silberschatz, A. — Fundamentos de bases de datos. McGraw-Hill.",
        ],
    },
    "IS-1": {
        "catedra": LAURA,
        "horario": [(1, "20:00", "22:00", "Aula 9"), (3, "20:00", "22:00", "Aula 9")],
        "resumen": (
            "Cómo se construye software en equipo: relevamiento, requisitos, estimación, control "
            "de versiones y pruebas. La materia se cursa armando un proyecto en grupos de cuatro, "
            "con entregas parciales y revisión entre pares."
        ),
        "unidades": [
            "Ciclos de vida. Modelos en cascada, iterativos y ágiles.",
            "Relevamiento y requisitos. Funcionales, no funcionales y criterios de aceptación.",
            "Modelado con UML. Casos de uso, clases y secuencia.",
            "Gestión de la configuración. Git, ramas y revisión de código.",
            "Verificación y validación. Pruebas unitarias, de integración y de aceptación.",
        ],
        "biblio": [
            "Sommerville, I. — Ingeniería de software, 10.ª edición. Pearson.",
            "Pressman, R. — Ingeniería del software: un enfoque práctico. McGraw-Hill.",
        ],
    },
    "RED-1": {
        "catedra": DIEGO,
        "horario": [(3, "18:00", "21:00", "Lab. de redes")],
        "resumen": (
            "Cómo se comunican dos máquinas: capas, direccionamiento, enrutamiento y los "
            "protocolos que sostienen internet. La práctica se hace con equipos del laboratorio "
            "y con simulador, armando y rompiendo redes a propósito."
        ),
        "unidades": [
            "Modelos OSI y TCP/IP. Encapsulamiento.",
            "Capa física y de enlace. Ethernet, conmutación y VLAN.",
            "Capa de red. IPv4, IPv6, subredes y enrutamiento.",
            "Capa de transporte. TCP, UDP y control de congestión.",
            "Aplicaciones y servicios: DNS, HTTP, DHCP. Seguridad básica.",
        ],
        "biblio": [
            "Tanenbaum, A. — Redes de computadoras, 5.ª edición. Pearson.",
            "Kurose, J. y Ross, K. — Redes de computadoras: un enfoque descendente. Pearson.",
        ],
    },
    "SO-1": {
        "catedra": JORGE,
        "horario": [(2, "18:00", "21:00", "Lab. 1"), (4, "18:00", "21:00", "Lab. 1")],
        "resumen": (
            "Qué hace el sistema operativo cuando nadie lo mira: procesos, planificación, "
            "memoria, archivos y concurrencia. Las prácticas son sobre GNU/Linux, con programas "
            "propios que crean procesos y los sincronizan."
        ),
        "unidades": [
            "Procesos e hilos. Estados y cambio de contexto.",
            "Planificación del procesador. Algoritmos y métricas.",
            "Concurrencia. Exclusión mutua, semáforos e interbloqueo.",
            "Administración de memoria. Paginación y memoria virtual.",
            "Sistemas de archivos y entrada/salida.",
        ],
        "biblio": [
            "Tanenbaum, A. — Sistemas operativos modernos. Pearson.",
            "Silberschatz, A. — Fundamentos de sistemas operativos. McGraw-Hill.",
        ],
    },
    "BD-2": {
        "catedra": PABLO,
        "horario": [(1, "18:00", "21:00", "Aula 12"), (3, "18:00", "21:00", "Aula 12")],
        "resumen": (
            "Segunda parte de bases de datos: optimización de consultas, concurrencia, "
            "administración y modelos no relacionales. Se parte de bases con datos de verdad, "
            "donde una consulta mal escrita se nota."
        ),
        "unidades": [
            "Procesamiento y optimización de consultas. Planes de ejecución.",
            "Transacciones y concurrencia. Niveles de aislamiento y bloqueos.",
            "Respaldo, recuperación y seguridad. Usuarios y permisos.",
            "Procedimientos almacenados y disparadores.",
            "Modelos no relacionales. Documentos, clave-valor y cuándo convienen.",
        ],
        "biblio": [
            "Elmasri, R. y Navathe, S. — Fundamentos de sistemas de bases de datos. Pearson.",
            "Documentación de PostgreSQL 16 (material de cátedra).",
        ],
    },
    "PROG-3": {
        "catedra": MARIA,
        "horario": [(2, "14:00", "17:00", "Lab. 2"), (5, "14:00", "17:00", "Lab. 2")],
        "resumen": (
            "Diseño orientado a objetos: encapsulamiento, herencia, polimorfismo y los patrones "
            "que resuelven los problemas que aparecen una y otra vez. El trabajo integrador es "
            "una aplicación con interfaz gráfica y persistencia."
        ),
        "unidades": [
            "Clases y objetos. Encapsulamiento y responsabilidades.",
            "Herencia y composición. Cuándo conviene cada una.",
            "Polimorfismo e interfaces. Programar contra abstracciones.",
            "Patrones de diseño. Creacionales, estructurales y de comportamiento.",
            "Persistencia e interfaz gráfica. Separación en capas.",
        ],
        "biblio": [
            "Gamma, E. y otros — Patrones de diseño. Addison-Wesley.",
            "Freeman, E. — Head First Design Patterns. O'Reilly.",
        ],
    },
    "MAT-4": {
        "catedra": JORGE,
        "horario": [(3, "08:00", "12:00", "Aula 5")],
        "resumen": (
            "La matemática que usa la computación: lógica, conjuntos, relaciones, grafos y "
            "recurrencias. Es la materia que da el lenguaje para demostrar que un algoritmo hace "
            "lo que dice hacer."
        ),
        "unidades": [
            "Lógica proposicional y de predicados. Métodos de demostración.",
            "Conjuntos, relaciones y funciones. Órdenes y equivalencias.",
            "Combinatoria y recurrencias.",
            "Teoría de grafos. Caminos, árboles y conectividad.",
            "Autómatas finitos y lenguajes regulares.",
        ],
        "biblio": [
            "Rosen, K. — Matemática discreta y sus aplicaciones. McGraw-Hill.",
            "Grimaldi, R. — Matemáticas discreta y combinatoria. Pearson.",
        ],
    },
    "IS-2": {
        "catedra": LAURA,
        "horario": [(4, "18:00", "22:00", "Aula 9")],
        "resumen": (
            "Arquitectura de software, calidad y gestión de proyectos. Continúa el proyecto de "
            "Ingeniería de Software I, ahora con la mirada puesta en que el sistema se pueda "
            "operar, medir y mantener."
        ),
        "unidades": [
            "Arquitecturas. Capas, cliente-servidor, microservicios y sus costos.",
            "Calidad del software. Métricas, deuda técnica y revisiones.",
            "Gestión de proyectos. Planificación, riesgos y seguimiento.",
            "Integración y despliegue continuos.",
            "Mantenimiento y evolución. Reingeniería y documentación.",
        ],
        "biblio": [
            "Bass, L. — Software Architecture in Practice. Addison-Wesley.",
            "Sommerville, I. — Ingeniería de software. Pearson (parte IV).",
        ],
    },
    "RED-2": {
        "catedra": DIEGO,
        "horario": [(1, "18:00", "21:00", "Lab. de redes")],
        "resumen": (
            "Redes de mayor escala: enrutamiento dinámico, calidad de servicio, seguridad "
            "perimetral y administración. Incluye el armado y la documentación de la red de un "
            "edificio como trabajo final."
        ),
        "unidades": [
            "Enrutamiento dinámico. OSPF y BGP.",
            "Redes privadas virtuales y túneles.",
            "Seguridad de red. Cortafuegos, listas de control y detección.",
            "Calidad de servicio y administración del tráfico.",
            "Monitoreo y documentación de la red.",
        ],
        "biblio": [
            "Kurose, J. y Ross, K. — Redes de computadoras. Pearson.",
            "Guías de laboratorio de la cátedra.",
        ],
    },
    "SIS-107": {
        "catedra": LAURA,
        "horario": [(5, "18:00", "21:00", "Aula 4")],
        "resumen": (
            "Cómo se investiga y cómo se escribe lo investigado. Prepara para el trabajo final "
            "integrador: delimitar un problema, revisar antecedentes, elegir una metodología y "
            "defender los resultados por escrito y en forma oral."
        ),
        "unidades": [
            "Conocimiento científico. Problema, objetivos e hipótesis.",
            "Antecedentes y estado del arte. Búsqueda y lectura crítica.",
            "Diseño metodológico. Enfoques cuantitativo y cualitativo.",
            "Recolección y análisis de datos. Instrumentos.",
            "Escritura académica. Citas, referencias y defensa oral.",
        ],
        "biblio": [
            "Hernández Sampieri, R. — Metodología de la investigación. McGraw-Hill.",
            "Normas APA, 7.ª edición (guía de la cátedra).",
        ],
    },
}

# ===================== Profesorado en Matemática =====================
# Las materias de esta carrera y de la siguiente **no están en la base**: las
# crea `demo/planes.py` con estos mismos códigos. Acá está lo que enseñan.
CATALOGO.update({
    "PM-101": {
        "catedra": MARCELO,
        "horario": [(1, "18:00", "21:00", "Aula 3")],
        "resumen": (
            "Álgebra elemental con la mirada puesta en la enseñanza: no alcanza con resolver, "
            "hay que poder explicar por qué cada paso es válido y anticipar dónde se equivoca "
            "quien está aprendiendo."
        ),
        "unidades": [
            "Números reales. Operaciones, orden y valor absoluto.",
            "Polinomios. Factorización y ecuaciones algebraicas.",
            "Sistemas de ecuaciones e inecuaciones.",
            "Matrices y determinantes. Resolución de sistemas.",
        ],
        "biblio": ["Anton, H. — Introducción al álgebra lineal. Limusa."],
    },
    "PM-102": {
        "catedra": MARCELO,
        "horario": [(3, "18:00", "21:00", "Aula 3")],
        "resumen": (
            "Geometría euclidiana con construcciones y demostraciones. Se trabaja con regla y "
            "compás y con software de geometría dinámica, para que la conjetura venga antes de "
            "la demostración."
        ),
        "unidades": [
            "Axiomas de la geometría euclidiana. Rectas y ángulos.",
            "Triángulos. Congruencia, semejanza y puntos notables.",
            "Circunferencia. Ángulos inscriptos y potencia de un punto.",
            "Áreas y perímetros. Teoremas de Pitágoras y de Tales.",
        ],
        "biblio": ["Puig Adam, P. — Curso de geometría métrica. Euler."],
    },
    "PM-103": {
        "catedra": GABRIELA,
        "horario": [(2, "18:00", "21:00", "Aula 6")],
        "resumen": (
            "Primera aproximación al análisis: funciones, límites y continuidad, con atención a "
            "las representaciones —gráfica, tabular y simbólica— que después hay que saber "
            "poner en juego frente a un curso."
        ),
        "unidades": [
            "Funciones reales. Clasificación y gráficas.",
            "Sucesiones. Monotonía y convergencia.",
            "Límite de una función. Propiedades y cálculo.",
            "Continuidad. Teoremas de Bolzano y de Weierstrass.",
        ],
        "biblio": ["Spivak, M. — Calculus. Reverté."],
    },
    "PM-104": {
        "catedra": RAUL,
        "horario": [(4, "18:00", "21:00", "Aula 6")],
        "resumen": (
            "Qué es enseñar y qué es aprender: las corrientes pedagógicas del siglo XX y su "
            "huella en la escuela secundaria argentina, leídas desde el aula de matemática."
        ),
        "unidades": [
            "La pedagogía como campo. Educación, escuela y currículum.",
            "Corrientes del siglo XX. Conductismo, constructivismo y aprendizaje situado.",
            "El sistema educativo argentino. Niveles, leyes y obligatoriedad.",
            "Planificación de la enseñanza. Objetivos, actividades y evaluación.",
        ],
        "biblio": ["Gvirtz, S. y Palamidessi, M. — El ABC de la tarea docente. Aique."],
    },
    "PM-105": {
        "catedra": MARCELO,
        "horario": [(5, "18:00", "21:00", "Aula 3")],
        "resumen": (
            "Estructuras algebraicas: grupos, anillos y cuerpos. Es donde el álgebra deja de ser "
            "una colección de técnicas y pasa a ser una teoría."
        ),
        "unidades": [
            "Espacios vectoriales. Base, dimensión y coordenadas.",
            "Transformaciones lineales. Núcleo e imagen.",
            "Autovalores y autovectores. Diagonalización.",
            "Grupos, anillos y cuerpos. Primeros ejemplos.",
        ],
        "biblio": ["Grossman, S. — Álgebra lineal. McGraw-Hill."],
    },
    "PM-201": {
        "catedra": GABRIELA,
        "horario": [(2, "18:00", "21:00", "Aula 6")],
        "resumen": (
            "Cálculo diferencial e integral en una variable, con demostración de los teoremas "
            "centrales. La materia pide escribir las demostraciones, no solo seguirlas."
        ),
        "unidades": [
            "Derivada. Reglas, derivadas sucesivas y aproximación lineal.",
            "Teoremas del valor medio. Estudio completo de funciones.",
            "Integral de Riemann. Teorema fundamental del cálculo.",
            "Métodos de integración y aplicaciones geométricas.",
        ],
        "biblio": ["Apostol, T. — Calculus, volumen 1. Reverté."],
    },
    "PM-202": {
        "catedra": MARCELO,
        "horario": [(3, "18:00", "21:00", "Aula 3")],
        "resumen": (
            "Geometría analítica y transformaciones del plano, con uso sistemático de software "
            "de geometría dinámica para explorar antes de formalizar."
        ),
        "unidades": [
            "Coordenadas y vectores en el plano y el espacio.",
            "Rectas, planos y cónicas.",
            "Transformaciones del plano. Isometrías y semejanzas.",
            "Geometría del espacio. Poliedros y cuerpos redondos.",
        ],
        "biblio": ["Santaló, L. — Geometría proyectiva. EUDEBA."],
    },
    "PM-203": {
        "catedra": GABRIELA,
        "horario": [(1, "18:00", "21:00", "Aula 6")],
        "resumen": (
            "Cómo se enseña matemática: obstáculos de aprendizaje, errores frecuentes, diseño de "
            "secuencias didácticas y evaluación. Cada unidad termina con una clase planificada y "
            "simulada frente a los compañeros."
        ),
        "unidades": [
            "La didáctica de la matemática como disciplina. Transposición didáctica.",
            "Obstáculos y errores. El error como fuente de información.",
            "Secuencias didácticas. Problemas, consignas y gestión de la clase.",
            "Evaluación en matemática. Instrumentos y criterios.",
        ],
        "biblio": ["Chevallard, Y. — La transposición didáctica. Aique."],
    },
    "PM-204": {
        "catedra": ANA,
        "horario": [(4, "18:00", "21:00", "Aula 5")],
        "resumen": (
            "Probabilidad y estadística para la escuela secundaria: qué se enseña, con qué datos "
            "y con qué herramientas. Incluye el uso de planilla de cálculo en el aula."
        ),
        "unidades": [
            "Estadística descriptiva. Tablas, gráficos y medidas.",
            "Probabilidad. Experimentos aleatorios y simulación.",
            "Variables aleatorias y distribuciones.",
            "Nociones de inferencia. Muestreo y estimación.",
        ],
        "biblio": ["Devore, J. — Probabilidad y estadística. Cengage."],
    },
    "PM-301": {
        "catedra": GABRIELA,
        "horario": [(2, "18:00", "21:00", "Aula 6")],
        "resumen": (
            "Análisis en varias variables y series, con las aplicaciones que después aparecen en "
            "física y en estadística."
        ),
        "unidades": [
            "Series numéricas y de potencias. Series de Taylor.",
            "Funciones de varias variables. Derivadas parciales.",
            "Integrales múltiples. Cambios de coordenadas.",
            "Ecuaciones diferenciales elementales.",
        ],
        "biblio": ["Apostol, T. — Calculus, volumen 2. Reverté."],
    },
    "PM-302": {
        "catedra": RAUL,
        "horario": [(3, "18:00", "21:00", "Aula 6")],
        "resumen": (
            "Segunda didáctica, centrada en el ciclo orientado: funciones, álgebra y "
            "probabilidad en la escuela, con uso de tecnología y trabajo por proyectos."
        ),
        "unidades": [
            "Enseñanza del álgebra y de las funciones.",
            "Tecnología en el aula de matemática.",
            "Proyectos y modelización matemática.",
            "Diseño de la evaluación integradora.",
        ],
        "biblio": ["Sadovsky, P. — Enseñar matemática hoy. Libros del Zorzal."],
    },
    "PM-303": {
        "catedra": RAUL,
        "horario": [(5, "14:00", "19:00", "Escuelas asociadas")],
        "resumen": (
            "La residencia: observación, acompañamiento y práctica frente a curso en escuelas "
            "asociadas, con ateneo semanal de análisis de las clases dadas."
        ),
        "unidades": [
            "Observación institucional y del aula.",
            "Planificación de la unidad didáctica a cargo.",
            "Práctica frente a curso. Registro y autoevaluación.",
            "Ateneo de análisis de la práctica. Portafolio final.",
        ],
        "biblio": ["Anijovich, R. — Transitar la formación pedagógica. Paidós."],
    },
})

# ===================== Licenciatura en Ciencias Químicas =====================
CATALOGO.update({
    "QUI-101": {
        "catedra": NOELIA,
        "horario": [(1, "08:00", "12:00", "Lab. de química 1")],
        "resumen": (
            "Primera materia de la carrera: estructura atómica, enlaces, estequiometría y "
            "soluciones, con trabajo de laboratorio desde la segunda semana. La seguridad en el "
            "laboratorio es contenido de la materia, no una advertencia."
        ),
        "unidades": [
            "Materia y energía. Estructura atómica y tabla periódica.",
            "Enlace químico. Iónico, covalente y metálico.",
            "Estequiometría. Reacciones y cálculos con moles.",
            "Soluciones. Concentración y propiedades.",
            "Seguridad e higiene en el laboratorio. Material y técnicas básicas.",
        ],
        "biblio": [
            "Chang, R. — Química, 12.ª edición. McGraw-Hill.",
            "Atkins, P. — Principios de química. Panamericana.",
        ],
    },
    "QUI-102": {
        "catedra": RAMIRO,
        "horario": [(2, "08:00", "11:00", "Aula 8")],
        "resumen": (
            "La matemática que la química necesita: funciones, derivadas e integrales aplicadas "
            "a velocidades de reacción, equilibrios y curvas de calibración."
        ),
        "unidades": [
            "Funciones y gráficas. Ajuste de rectas.",
            "Límite, continuidad y derivada.",
            "Integral y aplicaciones.",
            "Nociones de estadística para el laboratorio. Error e incertidumbre.",
        ],
        "biblio": ["Stewart, J. — Cálculo. Cengage."],
    },
    "QUI-103": {
        "catedra": RAMIRO,
        "horario": [(4, "08:00", "12:00", "Lab. de física")],
        "resumen": (
            "Mecánica, calor y electricidad, con prácticas de medición y tratamiento de errores. "
            "Es la base de Fisicoquímica."
        ),
        "unidades": [
            "Cinemática y dinámica. Leyes de Newton.",
            "Trabajo, energía y conservación.",
            "Calor y temperatura. Primera ley de la termodinámica.",
            "Electricidad y circuitos elementales.",
        ],
        "biblio": ["Serway, R. — Física para ciencias e ingeniería. Cengage."],
    },
    "QUI-104": {
        "catedra": NOELIA,
        "horario": [(3, "08:00", "12:00", "Lab. de química 1")],
        "resumen": (
            "Los elementos y sus compuestos: periodicidad, química de coordinación y síntesis "
            "inorgánica, con prácticas de obtención y caracterización."
        ),
        "unidades": [
            "Periodicidad y propiedades de los elementos.",
            "Hidrógeno, metales alcalinos y alcalinotérreos.",
            "Elementos del bloque p. Óxidos, ácidos y sales.",
            "Compuestos de coordinación. Nomenclatura y geometría.",
        ],
        "biblio": ["Housecroft, C. — Química inorgánica. Pearson."],
    },
    "QUI-105": {
        "catedra": VERONICA,
        "horario": [(5, "08:00", "12:00", "Lab. de análisis")],
        "resumen": (
            "Cómo se mide cuánto hay de algo: equilibrio en solución, gravimetría y volumetría, "
            "con énfasis en la calidad del dato y la trazabilidad."
        ),
        "unidades": [
            "Equilibrio químico en solución. Ácido-base y precipitación.",
            "Errores, cifras significativas y tratamiento de datos.",
            "Gravimetría. Técnicas y cálculos.",
            "Volumetría. Titulaciones y curvas.",
        ],
        "biblio": ["Skoog, D. — Fundamentos de química analítica. Cengage."],
    },
    "QUI-201": {
        "catedra": VERONICA,
        "horario": [(1, "14:00", "18:00", "Lab. de orgánica")],
        "resumen": (
            "Estructura y reactividad de los compuestos del carbono: grupos funcionales, "
            "mecanismos y estereoquímica, con síntesis en el laboratorio."
        ),
        "unidades": [
            "Estructura y enlace en compuestos orgánicos. Hibridación.",
            "Alcanos, alquenos y alquinos. Nomenclatura y reactividad.",
            "Estereoquímica. Isomería y quiralidad.",
            "Mecanismos de reacción. Sustitución y eliminación.",
        ],
        "biblio": ["McMurry, J. — Química orgánica. Cengage."],
    },
    "QUI-202": {
        "catedra": VERONICA,
        "horario": [(3, "14:00", "18:00", "Lab. de análisis")],
        "resumen": (
            "Análisis instrumental: espectrofotometría, potenciometría y cromatografía, con "
            "validación de métodos sobre muestras reales."
        ),
        "unidades": [
            "Métodos ópticos. Espectrofotometría UV-visible.",
            "Métodos electroquímicos. Potenciometría y conductimetría.",
            "Separaciones. Cromatografía en capa fina y gaseosa.",
            "Validación de métodos analíticos.",
        ],
        "biblio": ["Skoog, D. — Principios de análisis instrumental. Cengage."],
    },
    "QUI-203": {
        "catedra": RAMIRO,
        "horario": [(2, "14:00", "18:00", "Lab. de física")],
        "resumen": (
            "Termodinámica química y cinética: por qué una reacción ocurre y a qué velocidad. "
            "Las prácticas incluyen calorimetría y determinación de órdenes de reacción."
        ),
        "unidades": [
            "Primera y segunda ley. Entalpía, entropía y energía libre.",
            "Equilibrio químico y de fases.",
            "Soluciones y propiedades coligativas.",
            "Cinética química. Órdenes, velocidad y catálisis.",
        ],
        "biblio": ["Atkins, P. — Química física. Panamericana."],
    },
    "QUI-204": {
        "catedra": VERONICA,
        "horario": [(4, "14:00", "18:00", "Lab. de orgánica")],
        "resumen": (
            "Compuestos aromáticos, carbonílicos y biomoléculas, con síntesis de varios pasos y "
            "caracterización por espectroscopía."
        ),
        "unidades": [
            "Compuestos aromáticos. Sustitución electrofílica.",
            "Aldehídos, cetonas y ácidos carboxílicos.",
            "Aminas y compuestos nitrogenados.",
            "Introducción a las biomoléculas. Hidratos de carbono y lípidos.",
        ],
        "biblio": ["McMurry, J. — Química orgánica. Cengage."],
    },
    "QUI-301": {
        "catedra": NOELIA,
        "horario": [(2, "08:00", "12:00", "Lab. de química 2")],
        "resumen": (
            "La química de los seres vivos: proteínas, enzimas, metabolismo y ácidos nucleicos, "
            "con prácticas de determinación enzimática."
        ),
        "unidades": [
            "Aminoácidos y proteínas. Estructura y función.",
            "Enzimas. Cinética e inhibición.",
            "Metabolismo de hidratos de carbono y lípidos.",
            "Ácidos nucleicos y síntesis de proteínas.",
        ],
        "biblio": ["Lehninger, A. — Principios de bioquímica. Omega."],
    },
    "QUI-302": {
        "catedra": NOELIA,
        "horario": [(5, "14:00", "18:00", "Aula 8")],
        "resumen": (
            "Procesos químicos a escala industrial: operaciones unitarias, balances, control de "
            "calidad y tratamiento de efluentes, con visitas a plantas de la región."
        ),
        "unidades": [
            "Operaciones unitarias. Balances de masa y energía.",
            "Procesos industriales inorgánicos y orgánicos.",
            "Control de calidad y normas.",
            "Efluentes y gestión ambiental.",
        ],
        "biblio": ["Austin, G. — Manual de procesos químicos en la industria. McGraw-Hill."],
    },
})
