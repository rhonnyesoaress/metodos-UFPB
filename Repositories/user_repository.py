# Repositories/user_repository.py
from __future__ import annotations
from typing import Dict, Any, Optional

from Repositories.interfaces import IUserRepository


class UserRepository(IUserRepository):
    """
    Adapter sobre o seu UserManager, priorizando persistência real.
    - Obtém usuário via get_user (preferencial), depois tenta outros nomes comuns.
    - Persiste gabarito via update_gabarito (preferencial). Se não houver, cai em fallback.
    - Garante que o atributo do modelo seja 'gabarito' (singular), conforme seu projeto.
    """

    def __init__(self, user_manager: Any) -> None:
        self.user_manager = user_manager

    # ---------------------------
    # Helpers internos
    # ---------------------------
    def _get_by_username(self, username: str) -> Optional[Any]:
        """
        Tenta obter o usuário usando os métodos mais prováveis do seu UserManager.
        Ordem de tentativa:
          1) get_user(username)
          2) obter_por_username / get_by_username / buscar / get
          3) listar/all + filtro por username/login/email
        """
        # 1) Método preferencial
        if hasattr(self.user_manager, "get_user"):
            try:
                u = self.user_manager.get_user(username)
                if u is not None:
                    return u
            except TypeError:
                pass

        # 2) Outros nomes comuns
        for meth in ("obter_por_username", "get_by_username", "buscar", "get"):
            if hasattr(self.user_manager, meth):
                try:
                    u = getattr(self.user_manager, meth)(username)
                    if u is not None:
                        return u
                except TypeError:
                    # assinatura diferente, ignora e segue
                    pass

        # 3) Fallback por listagem
        users = None
        for meth in ("listar", "all"):
            if hasattr(self.user_manager, meth):
                users = getattr(self.user_manager, meth)()
                break

        if users:
            for u in users:
                if (
                    getattr(u, "username", None) == username
                    or getattr(u, "login", None) == username
                    or getattr(u, "email", None) == username
                ):
                    return u

        return None

    def _persist_user(self, user: Any) -> None:
        """
        Fallback genérico caso você precise salvar o objeto inteiro.
        Se o seu fluxo oficial usa update_gabarito, você pode nem usar este método.
        """
        for meth in ("atualizar", "salvar", "save", "update", "save_users"):
            if hasattr(self.user_manager, meth):
                getattr(self.user_manager, meth)(user)
                return
        # Sem método de persistência explícito: não faz nada.

    # ---------------------------
    # Implementação da interface
    # ---------------------------
    def obter_por_username(self, username: str):
        user = self._get_by_username(username)

        # Se não existe, opcionalmente crie (se o manager suportar)
        if user is None and hasattr(self.user_manager, "create_user"):
            try:
                # ajuste os argumentos conforme sua implementação real
                user = self.user_manager.create_user(username=username, password="")
            except TypeError:
                # tentativa simples caso a assinatura seja diferente
                try:
                    user = self.user_manager.create_user(username)
                except Exception:
                    user = None

        # Se ainda não existir, retorne None (ou lance erro, se preferir)
        if user is None:
            return None

        # Garante o atributo 'gabarito' (singular) como dict
        if not hasattr(user, "gabarito") or getattr(user, "gabarito") is None:
            try:
                setattr(user, "gabarito", {})
            except Exception:
                # se o modelo bloquear setattr, siga mesmo assim
                pass

        return user

    def salvar_gabaritos(self, username: str, gabaritos: Dict[str, str]) -> None:
        """
        Persiste (merge) o gabarito do usuário, priorizando o método oficial do seu manager:
        - update_gabarito(username, dict)
        Caso não exista, faz fallback atualizando o objeto e tentando salvar inteiro.
        """
        user = self.obter_por_username(username)
        if user is None:
            raise ValueError(f"Usuário '{username}' não encontrado para salvar gabaritos.")

        atual = getattr(user, "gabarito", {}) or {}
        novo = {**atual, **(gabaritos or {})}

        # 1) Caminho oficial do seu projeto
        if hasattr(self.user_manager, "update_gabarito"):
            self.user_manager.update_gabarito(username, novo)
            return

        # 2) Fallback: setar no objeto e tentar salvar inteiro
        try:
            setattr(user, "gabarito", novo)
        except Exception:
            pass

        self._persist_user(user)
