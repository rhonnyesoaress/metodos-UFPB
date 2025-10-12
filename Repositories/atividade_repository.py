# Repositories/atividade_repository.py
from __future__ import annotations
from typing import Iterable, Any

from Repositories.interfaces import IAtividadeRepository

class AtividadeRepository(IAtividadeRepository):
    """
    Adapter em cima do seu AtividadeManager.
    Suposições:
      - atividade_manager pode ter: listar() / all() / get_all()
    """

    def __init__(self, atividade_manager: Any) -> None:
        self.atividade_manager = atividade_manager

    def listar(self) -> Iterable[Any]:
        for meth in ("listar", "all", "get_all", "list"):
            if hasattr(self.atividade_manager, meth):
                return getattr(self.atividade_manager, meth)()
        raise AttributeError("AtividadeManager não expõe métodos para listar atividades.")
