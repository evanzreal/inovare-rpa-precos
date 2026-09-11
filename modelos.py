"""Dataclass compartilhada pelos caminhos de precificacao."""

from dataclasses import dataclass, field


@dataclass
class LinhaPreco:
    """Uma combinacao de preco coletada de uma locadora."""
    locadora: str
    modelo: str
    versao: str = ""
    pessoa: str = ""           # "fisica" | "juridica"
    meses: int | None = None
    km_mes: int | None = None  # franquia de km/mes
    preco: float | None = None
    bruto: dict = field(default_factory=dict)
