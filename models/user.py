class User:
    def __init__(self, username):
        self.username: str = username

    def to_dict(self) -> dict:
        return {
            'username': self.username,
        }

    @staticmethod
    def from_dict(self, username):
        return User(username=username)

    def __str__(self):
        return f"Пользователь: {self.username}"
