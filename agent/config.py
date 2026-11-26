import os
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class Config:
    nom_ag: str = "AgenteSEGIP-BOL"
    ver: str = "1.0.0"
    dir_trab: str = os.path.dirname(os.path.abspath(__file__))
    cats: List[str] = None
    ed_min: Dict[str, int] = None
    costos: Dict[str, float] = None
    svc: Dict[str, str] = None

    def __post_init__(self):
        if self.cats is None:
            self.cats = ["P", "A", "M", "T", "B", "C", "D", "JP", "JM", "DP", "DA"]

        self.ed_min = {
            "P": 18,
            "A": 21,
            "M": 16,
            "T": 18,
            "B": 26,
            "C": 31,
            "JP": 16,
            "JM": 16,
            "DP": 18,
            "DA": 18
        }

        self.costos = {
            "P": 225.0,
            "A": 225.0,
            "M": 80.0,
            "T": 80.0,
            "B": 225.0,
            "C": 225.0,
            "JP": 225.0,
            "JM": 80.0,
            "DP": 160.0,
            "DA": 160.0
        }

        self.svc = {
            "lic_nueva": "https://www.segip.gob.bo/licencia-para-conducir/",
            "autoesc": "https://www.segip.gob.bo/licencia-para-conducir/",
            "med": "https://www.segip.gob.bo/",
            "banco": "Banco Union",
            "cudap": "https://estadoDigital.bolivia.gob.bo/cudap",
            "citas": "http://ticketlicencias.segip.gob.bo/"
        }


cfg = Config()
