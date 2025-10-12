from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Iterable, Any

class IUserRepository(ABC):
    @abstractmethod
    def obter_por_username(self, username: str) -> Any: ...
    @abstractmethod
    def salvar_gabaritos(self, username: str, gabaritos: Dict[str, str]) -> None: ...

class IAtividadeRepository(ABC):
    @abstractmethod
    def listar(self) -> Iterable[Any]: ...
