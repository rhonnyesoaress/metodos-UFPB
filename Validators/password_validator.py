# Validação de senha
import re

class PasswordValidator:
    @staticmethod
    def validate(password: str):
        """Valida a senha com base nas regras do AWS IAM."""
        aws_iam_policy = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$'
        
        if not re.match(aws_iam_policy, password):
            raise ValueError("A senha não atende aos requisitos de segurança.\n"
                             "Requisitos: 8 a 128 caracteres, 1 maiúscula, 1 minúscula, 1 número e 1 caractere especial.")