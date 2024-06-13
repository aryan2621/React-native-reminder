import uuid


class create_todo_dto:
    def __init__(
        self,
        title: str,
        description: str = "",
        done: bool = False,
        image_url: str = "",
    ):
        if not title:
            raise ValueError("Title is required")
        if not isinstance(done, bool):
            raise ValueError("Done must be a boolean")

        self.id = uuid.uuid4()
        self.title = title
        self.description = description
        self.done = done
        self.image_url = image_url


class get_todo_by_id_dto:
    def __init__(self, id: uuid.UUID):
        if not id:
            raise ValueError("A valid id is required")
        self.id = id


class update_todo_by_id_dto:
    def __init__(
        self,
        id: uuid.UUID,
        title: str = None,
        description: str = None,
        done: bool = None,
        image_url: str = None,
    ):
        if not id:
            raise ValueError("A valid id is required")
        self.title = title
        self.description = description
        self.done = done
        self.image_url = image_url


class delete_todo_by_id_dto:
    def __init__(self, id: uuid.UUID):
        if not id:
            raise ValueError("A valid id is required")
        self.id = id


class register_user_dto:
    def __init__(self, name: str, email: str, password: str):
        if not name:
            raise ValueError("Name is required")
        if not email:
            raise ValueError("Email is required")
        if not password:
            raise ValueError("password is required")
        self.id = uuid.uuid4()
        self.name = name
        self.email = email
        self.password = password


class login_user_dto:
    def __init__(self, email: str, password: str):
        if not email:
            raise ValueError("Email is required")
        if not password:
            raise ValueError("password is required")
        self.email = email
        self.password = password
