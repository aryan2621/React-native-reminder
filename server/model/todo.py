class Todo:
    def __init__(self, id, title, description, done, created_at, image_url):
        self.id = id
        self.title = title
        self.description = description
        self.done = done
        self.created_at = created_at
        self.image_url = image_url

    def __repr__(self):
        return f"<Todo {self.id}>"

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "done": self.done,
            "created_at": self.created_at,
            "image_url": self.image_url,
        }
