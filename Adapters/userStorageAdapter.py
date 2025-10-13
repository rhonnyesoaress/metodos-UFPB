from legacy.LegacyUserStorage import LegacyUserStorage
from Entidades.User import User

class UserStorageAdapter:
    def __init__(self, legacy: LegacyUserStorage):
        self.legacy = legacy

    def load_users(self) -> list[User]:
        rows = self.legacy.load_legacy_users()
        return [User.from_dict(r) for r in rows]

    def save_users(self, users: list[User]) -> None:
        # opcional no adapter; pode não suportar escrita
        pass
