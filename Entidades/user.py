# user.py
class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password  # Em um sistema real, você usaria hashing aqui

    def check_password(self, password: str) -> bool:
        return self.password == password