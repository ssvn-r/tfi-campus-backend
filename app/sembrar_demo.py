"""Carga el campus de demostración: carreras completas, contenido y actividad.

**Es opcional y se corre a mano**, como `importar_estructura`. El servidor no
lo hace solo: lo que carga es contenido de ejemplo —cátedras, estudiantes,
apuntes, novedades, foro— y eso no tiene que aparecer en la base de la
facultad porque alguien reinició el servidor.

Para qué sirve: dejar el campus **mostrable**. Un campus recién puesto en línea
tiene el plan cargado y nada más: módulos vacíos, muro sin novedades, foro sin
temas y tableros en cero. Así no se puede mostrar lo que hace.

Qué hace, en orden:

    1. Se conecta a Firestore y trae lo que ya hay (nada se pisa).
    2. Da de alta las cátedras y los estudiantes que falten.
    3. Completa los planes de las tres carreras y abre los módulos.
    4. Carga el contenido de cada módulo, con los documentos en PDF subidos
       a Cloudflare R2 como cualquier archivo del campus.
    5. Carga inscripciones, historial, mesas de examen, entregas, notas,
       asistencia, biblioteca, novedades, foro, mensajes y eventos.
    6. Guarda todo por el mismo camino que usa el servidor.

Uso (desde backend/, con el servidor apagado):

    python -m app.sembrar_demo             # muestra qué haría, sin escribir
    python -m app.sembrar_demo --subir     # lo carga de verdad
    python -m app.sembrar_demo --subir --rehacer   # aunque ya se haya corrido

Después hay que **reiniciar el servidor**: la memoria del proceso que está
corriendo no se entera de lo que se escribió por afuera.
"""

from __future__ import annotations

import sys

from dotenv import load_dotenv

# El `.env` trae las credenciales de Firestore y de R2. `app.main` lo carga al
# arrancar el servidor; acá no pasa por ahí, así que hay que cargarlo igual o
# el sembrado escribiría en memoria y se perdería al terminar.
load_dotenv()

from .servicios import certificados  # noqa: E402

certificados.configurar()

from . import datos as d  # noqa: E402
from .servicios import almacenamiento as alm  # noqa: E402
from .servicios import firestore as fs  # noqa: E402
from .servicios import persistencia as p  # noqa: E402

MARCA = "sembradoDemo"


def _ya_sembrado() -> bool:
    if not p.activo():
        return False
    documento = (
        p.fs.obtener_firestore().collection(p.CONFIGURACION_COL).document(MARCA).get()
    )
    return documento.exists


def _anotar_sembrado(cuantos: int) -> None:
    if not p.activo():
        return
    p.fs.obtener_firestore().collection(p.CONFIGURACION_COL).document(MARCA).set(
        {"cuando": d.iso(d.ahora()), "documentos": cuantos}
    )


def main() -> None:
    subir = "--subir" in sys.argv
    rehacer = "--rehacer" in sys.argv

    print("Campus de demostración\n")
    # El servidor inicializa Firestore al arrancar; acá hay que hacerlo a mano o
    # la persistencia se daría por apagada y el sembrado quedaría en memoria.
    try:
        fs.inicializar_firestore()
    except Exception as error:  # noqa: BLE001
        print(f"Firestore no respondió: {error}")
    print(p.iniciar())
    print(alm.iniciar())

    if _ya_sembrado() and not rehacer:
        print(
            "\nEsta base ya tiene el campus de demostración cargado. No se toca nada."
            "\nPara completar lo que falte de todos modos:"
            "\n    python -m app.sembrar_demo --subir --rehacer"
        )
        return

    if not subir:
        print(
            "\nNo se escribió nada. Para cargarlo:"
            "\n    python -m app.sembrar_demo --subir"
        )
        return

    print("\nArmando el campus. Los documentos se generan y se suben, puede tardar un rato.\n")
    from . import demo

    cuenta = demo.armar()
    print(cuenta.resumen())

    escritos = p.guardar_cambios()
    _anotar_sembrado(escritos)

    print(f"\nGuardados {escritos} documentos en Firestore." if p.activo()
          else "\nFirestore apagado: no se guardó nada fuera de la memoria.")
    print(
        f"El campus quedó con {len(d.cursos)} módulos, {len(d.materias_plan)} materias, "
        f"{len(d.personas)} personas, {len(d.publicaciones)} novedades, "
        f"{len(d.temas_foro)} temas de foro y {len(d.archivos_subidos)} archivos."
    )
    print("\nReiniciá el servidor para que tome lo que se acaba de cargar.")


if __name__ == "__main__":
    main()
