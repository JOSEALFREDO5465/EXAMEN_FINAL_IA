from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class TipLic(Enum):
    PRIMERA = "primera_vez"
    RENO = "renovacion"
    DUPLI = "duplicado"
    ASC_GRAD = "ascenso_gradual"
    ASC_DIR = "ascenso_directo"
    PROV = "provisional"
    DIS_FIS = "discapacidad_fisica"
    DIS_AUD = "discapacidad_auditiva"
    EXT_RES = "extranjero_residente"
    EXT_HOM = "extranjero_homologacion"


class EstTram(Enum):
    INICIO = "iniciado"
    DOCS_OK = "documentos_reunidos"
    PAGO_OK = "pago_realizado"
    CITAS = "citas_agendadas"
    PROCESO = "en_proceso"
    LISTO = "listo_para_retirar"
    FIN = "completado"
    CANC = "cancelado"


@dataclass
class DocReq:
    nom: str
    desc: str
    obli: bool
    cat_lic: str = ""
    notas: str = ""

    def es_ok(self) -> bool:
        return bool(self.nom and self.nom.strip())


@dataclass
class ReqLic:
    tip: TipLic
    cat: str
    ed_min: int
    docs: List[DocReq]
    certs: List[str] = field(default_factory=list)
    costo: float = 0.0
    obs: str = ""


class ReqMgr:
    def __init__(self):
        self._cache: Dict[str, ReqLic] = {}
        self._cargar()

    def _cargar(self) -> None:
        self._agregar(
            TipLic.PRIMERA, "P", 18, 225.0,
            [DocReq("Cedula de Identidad vigente", "Cedula fisica o digital vigente", True, "P"),
             DocReq("Certificado de Evaluacion Medica", "Centro de salud acreditado (Bs 50)", True, "P",
                    "Se registra en el sistema el mismo dia, presentarse al dia siguiente"),
             DocReq("Certificado de Habilidades de Conduccion", "Autoescuela autorizada SEGIP", True, "P"),
             DocReq("Antecedentes Transito/FELCC/FELCN", "Policia Boliviana o CUDAP", True, "P")],
            "Licencia P, primera vez, mayores de 18"
        )
        self._agregar(
            TipLic.PRIMERA, "A", 21, 225.0,
            [DocReq("Cedula de Identidad vigente", "Cedula fisica o digital vigente", True, "A"),
             DocReq("Certificado de Evaluacion Medica", "Centro de salud acreditado (Bs 50)", True, "A",
                    "Se registra en el sistema el mismo dia, presentarse al dia siguiente"),
             DocReq("Certificado de Habilidades de Conduccion", "Autoescuela autorizada SEGIP", True, "A"),
             DocReq("Antecedentes Transito/FELCC/FELCN", "Policia Boliviana o CUDAP", True, "A")],
            "Licencia A, primera vez, mayores de 21"
        )
        self._agregar(
            TipLic.PROV, "M", 16, 225.0,
            [DocReq("Cedula de Identidad vigente", "Cedula fisica o digital vigente", True, "M"),
             DocReq("Autorizacion de padres o tutores", "Menor debe venir acompanado", True, "M"),
             DocReq("Certificado de Habilidades de Conduccion", "Autoescuela autorizada por MINEDU", True, "M"),
             DocReq("Certificado Medico", "Evaluacion fisica, visual y auditiva", True, "M"),
             DocReq("Evaluacion Psicologica", "Profesional autorizado por SEDES", True, "M"),
             DocReq("Antecedentes FELCN/FELCC/Transito", "Policia Boliviana o CUDAP", True, "M")],
            "Licencia provisional M/P para menores de 18"
        )
        self._agregar(
            TipLic.RENO, "P", 18, 225.0,
            [DocReq("Cedula de Identidad vigente", "Cedula fisica o digital vigente", True, "P"),
             DocReq("Certificado de Evaluacion Medica", "Centro de salud acreditado (Bs 50)", True, "P",
                    "Se registra en el sistema el mismo dia, presentarse al dia siguiente"),
             DocReq("Antecedentes de Transito", "Policia Boliviana o CUDAP", True, "P")],
            "Renovacion de licencia P"
        )
        self._agregar(
            TipLic.DUPLI, "P", 18, 160.0,
            [DocReq("Cedula de Identidad vigente", "Cedula fisica o digital vigente", True, "P"),
             DocReq("Denuncia por robo, extravio o destruccion", "Formulario SEGIP gratuito", True, "P")],
            "Duplicado de licencia P"
        )
        self._agregar(
            TipLic.ASC_GRAD, "B", 26, 225.0,
            [DocReq("Cedula de Identidad vigente", "Cedula fisica o digital vigente", True, "B"),
             DocReq("Certificado de Evaluacion Medica", "Centro de salud acreditado (Bs 50)", True, "B",
                    "Se registra en el sistema el mismo dia, presentarse al dia siguiente"),
             DocReq("Certificado de Habilidades de Conduccion", "Autoescuela autorizada SEGIP", True, "B"),
             DocReq("Antecedentes Transito/FELCC/FELCN", "Policia Boliviana o CUDAP", True, "B")],
            "Ascenso de A a B, cinco anos de antiguedad"
        )
        self._agregar(
            TipLic.EXT_RES, "P", 18, 225.0,
            [DocReq("Cedula de Identidad de Extranjero vigente", "Residencia legal en Bolivia", True, "P"),
             DocReq("Certificado de Evaluacion Medica", "Centro de salud acreditado (Bs 50)", True, "P",
                    "Se registra en el sistema el mismo dia, presentarse al dia siguiente"),
             DocReq("Certificado de Habilidades de Conduccion", "Autoescuela autorizada SEGIP", True, "P"),
             DocReq("Antecedentes FELCN/FELCC/Transito", "Policia Boliviana o CUDAP", True, "P")],
            "Licencia para extranjeros residentes"
        )

    def _agregar(self, tip: TipLic, cat: str, ed: int, cst: float, docs: List[DocReq], obs: str) -> None:
        clave = f"{tip.value}_{cat}"
        self._cache[clave] = ReqLic(tip=tip, cat=cat, ed_min=ed, docs=docs, costo=cst, obs=obs)

    def obtener(self, tip: TipLic, cat: str) -> Optional[ReqLic]:
        return self._cache.get(f"{tip.value}_{cat}")

    def listar(self) -> List[str]:
        return [t.value for t in TipLic]

    def val_edad(self, tip: TipLic, cat: str, ed: int) -> bool:
        r = self.obtener(tip, cat)
        if r is None:
            return False
        return ed >= r.ed_min
