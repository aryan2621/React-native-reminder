class User:
    def __init__(self, name, email, password):
        if not name:
            raise ValueError("Name is required")
        if not email:
            raise ValueError("Email is required")
        if not password:
            raise ValueError("password is required")
        self.name = name
        self.email = email
        self.password = password

    def serialize(self):
        return {
            "name": self.name,
            "email": self.email,
            "password": self.password,
        }
