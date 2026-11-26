#!/usr/bin/env python3
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
if BASE not in sys.path:
    sys.path.insert(0, BASE)

from agent.config import cfg
from agent.requirements import ReqMgr, TipLic, EstTram
from agent.process import Agente, Paso


def t_cfg():
    assert cfg.nom_ag == "AgenteSEGIP-BOL"
    assert cfg.ver == "1.0.0"
    assert "P" in cfg.cats
    assert cfg.costos["P"] == 225.0
    print("   ok configuracion")


def t_req():
    mgr = ReqMgr()
    r = mgr.obtener(TipLic.PRIMERA, "P")
    assert r is not None
    assert r.ed_min == 18
    assert len(r.docs) == 4
    assert all(d.obli for d in r.docs)
    assert mgr.val_edad(TipLic.PRIMERA, "P", 18) is True
    assert mgr.val_edad(TipLic.PRIMERA, "P", 17) is False
    assert mgr.val_edad(TipLic.PRIMERA, "A", 21) is True
    assert mgr.val_edad(TipLic.PROV, "M", 16) is True
    assert len(mgr.listar()) == 10
    print("   ok requisitos")


def t_proc():
    ag = Agente()
    res = ag.iniciar(TipLic.PRIMERA, "P", 25)
    assert res["exito"] is True
    assert res["cat"] == "P"
    res2 = ag.iniciar(TipLic.PRIMERA, "A", 19)
    assert res2["exito"] is False
    ag.iniciar(TipLic.PRIMERA, "P", 25)
    p = ag.avanzar(Paso.TIPO)
    assert p["sig"] == Paso.EDAD
    s = ag.resumen()
    assert s["cat"] == "P"
    assert s["est"] in [e.value for e in EstTram]
    print("   ok proceso")


def t_cli():
    from agent.cli import main, menu
    assert callable(main)
    assert callable(menu)
    print("   ok cli")


def main_test():
    print("=" * 60)
    print("PRUEBAS - AGENTE SEGIP BOLIVIA")
    print("=" * 60)
    t_cfg()
    t_req()
    t_proc()
    t_cli()
    print("=" * 60)
    print("TODAS LAS PRUEBAS PASARON")
    print("=" * 60)


if __name__ == "__main__":
    main_test()
