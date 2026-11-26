from typing import Dict, List, Optional, Any
from enum import Enum
from datetime import datetime
from .requirements import TipLic, EstTram, ReqMgr
from .config import cfg


class Paso(Enum):
    TIPO = "identificar_tipo"
    EDAD = "verificar_edad"
    DOCS = "reunir_documentos"
    CITA = "agendar_cita"
    PAGO = "realizar_pago"
    ENTREGA = "presentar_documentos"
    ESPERA = "esperar_proceso"
    RETIRAR = "retirar_licencia"
    FIN = "completar"


class Agente:
    def __init__(self, mgr: Optional[ReqMgr] = None):
        self.mgr = mgr or ReqMgr()
        self.est: EstTram = EstTram.INICIO
        self.paso: Optional[Paso] = None
        self.hist: List[Dict[str, Any]] = []
        self.datos: Dict[str, Any] = {}
        self.t_ini: Optional[datetime] = None
        self.t_fin: Optional[datetime] = None

    def iniciar(self, tip: TipLic, cat: str, ed: int) -> Dict[str, Any]:
        self._reset()
        self.t_ini = datetime.now()
        ok_ed = self.mgr.val_edad(tip, cat, ed)
        if not ok_ed:
            r = self.mgr.obtener(tip, cat)
            return {
                "exito": False,
                "mensaje": f"Edad minima para {cat} es {r.ed_min if r else 0} anos",
                "paso": Paso.TIPO
            }

        self.datos = {
            "tipo": tip.value,
            "cat": cat,
            "ed": ed,
            "ini": self.t_ini.isoformat(),
            "est": self.est.value
        }
        req = self.mgr.obtener(tip, cat)
        if req:
            self.datos["reqs"] = [
                {"nom": d.nom, "obli": d.obli, "desc": d.desc}
                for d in req.docs
            ]

        self.est = EstTram.INICIO
        self.paso = Paso.TIPO
        self.hist.append({
            "paso": self.paso.value,
            "ts": self.t_ini.isoformat(),
            "acc": "inicio"
        })
        return {
            "exito": True,
            "mensaje": f"Tramite iniciado para licencia {cat}, edad {ed} anos",
            "tipo": tip.value,
            "cat": cat,
            "est": self.est.value
        }

    def avanzar(self, paso: Paso, datos: Optional[Dict] = None) -> Dict[str, Any]:
        self.paso = paso
        self.hist.append({
            "paso": paso.value,
            "ts": datetime.now().isoformat(),
            "acc": "avance",
            "datos": datos or {}
        })
        res = self._trans(paso, datos)
        if res.get("fin"):
            self.t_fin = datetime.now()
            self.est = EstTram.FIN
        return res

    def _trans(self, paso: Paso, datos: Optional[Dict]) -> Dict[str, Any]:
        if paso == Paso.TIPO:
            return {"sig": Paso.EDAD, "mensaje": "Verificando edad..."}

        if paso == Paso.EDAD:
            cat = self.datos.get("cat", "")
            tip = TipLic(self.datos.get("tipo", "primera_vez"))
            req = self.mgr.obtener(tip, cat)
            ed = self.datos.get("ed", 0)
            if req and ed >= req.ed_min:
                return {"sig": Paso.DOCS, "mensaje": "Edad verificada"}
            return {"error": "Edad insuficiente para esta categoria"}

        if paso == Paso.DOCS:
            return {"sig": Paso.CITA, "mensaje": "Documentos reunidos, agende su cita"}

        if paso == Paso.CITA:
            return {"sig": Paso.PAGO, "mensaje": "Cita agendada"}

        if paso == Paso.PAGO:
            return {"sig": Paso.ENTREGA, "mensaje": "Pago realizado en Banco Union"}

        if paso == Paso.ENTREGA:
            return {"sig": Paso.ESPERA, "mensaje": "Documentos presentados en SEGIP"}

        if paso == Paso.ESPERA:
            return {"sig": Paso.RETIRAR, "mensaje": "Tramite aprobado, espere un dia habil"}

        if paso == Paso.RETIRAR:
            self.est = EstTram.FIN
            return {"fin": True, "mensaje": "Licencia lista para retirar"}

        return {"est": "continuar", "mensaje": "Siguiente paso"}

    def resumen(self) -> Dict[str, Any]:
        tiempo = None
        if self.t_ini and self.t_fin:
            d = self.t_fin - self.t_ini
            tiempo = f"{d.days} dias, {d.seconds // 3600} horas"
        return {
            "tipo": self.datos.get("tipo", ""),
            "cat": self.datos.get("cat", ""),
            "ed": self.datos.get("ed", 0),
            "est": self.est.value,
            "paso": self.paso.value if self.paso else "",
            "hist": len(self.hist),
            "tiempo": tiempo,
            "reqs_ok": self._n_reqs()
        }

    def _n_reqs(self) -> int:
        return len([p for p in self.hist if p.get("acc") == "docs_ok"])

    def _reset(self) -> None:
        self.est = EstTram.INICIO
        self.paso = Paso.TIPO
        self.hist = []
        self.datos = {}
        self.t_ini = None
        self.t_fin = None
