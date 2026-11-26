import os
import sys

if __package__ is None or __package__ == "":
    BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if BASE not in sys.path:
        sys.path.insert(0, BASE)
    from agent.config import cfg
    from agent.requirements import TipLic, ReqMgr
    from agent.process import Agente
else:
    from .config import cfg
    from .requirements import TipLic, ReqMgr
    from .process import Agente


def bienvenida():
    print("=" * 70)
    print("AGENTE INTELIGENTE DE LICENCIAS SEGIP - BOLIVIA")
    print("=" * 70)
    print(f"Version: {cfg.ver}")
    print(f"Agente: {cfg.nom_ag}")
    print()


def menu():
    print("Menu Principal:")
    print("  1. Iniciar nuevo tramite de licencia")
    print("  2. Ver requisitos por tipo de licencia")
    print("  3. Ver categorias y costos")
    print("  4. Salir")
    print()


def nuevo(ag):
    print("\n--- Iniciar Nuevo Tramite ---")
    print("Tipos de licencia disponibles:")
    tips = ag.mgr.listar()
    for i, t in enumerate(tips, 1):
        print(f"  {i}. {t.replace('_', ' ').title()}")
    print("  0. Cancelar")

    try:
        opc = input("\nSeleccione el tipo de tramite (numero): ").strip()
        if opc == "0":
            print("Operacion cancelada.")
            return

        i = int(opc) - 1
        if 0 <= i < len(tips):
            tip = TipLic(tips[i].replace(" ", "_").lower())
            print(f"\nTipo seleccionado: {tips[i]}")
            cat = input("Ingrese la categoria deseada (P, A, M, T, B, C, etc.): ").strip().upper()
            try:
                ed = int(input("Ingrese su edad actual: ").strip())
                res = ag.iniciar(tip, cat, ed)
                if res["exito"]:
                    print(f"\n{res['mensaje']}")
                    print(f"   Categoria: {res['cat']}")
                    print(f"   Tipo: {res['tipo']}")
                    if "reqs" in ag.datos:
                        print("\nRequisitos necesarios:")
                        for n, r in enumerate(ag.datos["reqs"], 1):
                            m = "si" if r["obli"] else "no"
                            print(f"   {n}. [{m}] {r['nom']}")
                    print(f"\nSiguiente paso: {res.get('est', 'iniciado')}")
                else:
                    print(f"\nError: {res['mensaje']}")
            except ValueError:
                print("Ingrese una edad valida (numero entero).")
        else:
            print("Opcion invalida. Seleccione un numero de la lista.")
    except ValueError:
        print("Ingrese un numero valido.")


def ver_req(ag):
    print("\n--- Requisitos por Tipo de Licencia ---")
    tips = ag.mgr.listar()
    for s in tips:
        try:
            tip = TipLic(s.replace(" ", "_").lower())
            r = ag.mgr.obtener(tip, "P")
            if r:
                print(f"\n{tip.value.upper()} - Categoria P")
                print(f"   Edad minima: {r.ed_min} anos")
                print(f"   Costo estimado: Bs. {r.costo:.0f}")
                print("   Documentos requeridos:")
                for d in r.docs:
                    est = "obligatorio" if d.obli else "recomendado"
                    print(f"     - [{est}] {d.nom}")
                    if d.notas:
                        print(f"       Nota: {d.notas}")
        except Exception:
            continue
    print("\n" + "=" * 50)


def ver_costos():
    print("\n--- Categorias de Licencia y Costos SEGIP ---")
    print("=" * 50)
    cc = {
        "P (Particular)": 225,
        "A (Profesional)": 225,
        "M (Motociclista)": 80,
        "T (Motocarro)": 80,
        "B (Transporte)": 225,
        "C (Carga)": 225,
        "JP (Provicional)": 225,
        "JM (Provicional Menor)": 80,
        "DP (Duplicado Particular)": 160,
        "DA (Duplicado Profesional)": 160,
    }
    for cat, cst in cc.items():
        print(f"  {cat:20} Bs. {cst:3.0f}")
    print("=" * 50)


def main():
    bienvenida()
    ag = Agente(ReqMgr())
    while True:
        menu()
        opc = input("Seleccione una opcion (1-4): ").strip()
        if opc == "1":
            nuevo(ag)
            input("\nPresione Enter para continuar...")
        elif opc == "2":
            ver_req(ag)
            input("\nPresione Enter para continuar...")
        elif opc == "3":
            ver_costos()
            input("\nPresione Enter para continuar...")
        elif opc == "4":
            print("\nGracias por usar el Agente SEGIP. Hasta luego.")
            print("Los requisitos pueden variar, verifique en www.segip.gob.bo")
            break
        else:
            print("Opcion no valida. Seleccione 1-4.")


if __name__ == "__main__":
    main()
