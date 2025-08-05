# Validação de login
class LoginValidator:
    @staticmethod
    def validate(username: str):
        """Valida o username (login) com base nas regras."""
        if not username:
            raise ValueError("O login não pode ser vazio.")
        if len(username) > 12:
            raise ValueError("O login deve ter no máximo 12 caracteres.")
        if any(char.isdigit() for char in username):
            raise ValueError("O login não pode conter números.")