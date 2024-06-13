import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_migrate import Migrate
from model.todo import Todo
from utils.dto import (
    create_todo_dto,
    get_todo_by_id_dto,
    update_todo_by_id_dto,
    register_user_dto,
    login_user_dto,
)
from flask_bcrypt import Bcrypt
import jwt
from functools import wraps
import os
import uuid

app = Flask(__name__)

# Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL", "mysql://root:Rishabh%402621@localhost/test"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "supersecretkey")

# Initialize extensions
sql_db = SQLAlchemy(app)
migrate = Migrate(app, sql_db)
bcrypt = Bcrypt(app)


# Models
class DBModel(sql_db.Model):
    id = sql_db.Column(
        sql_db.String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    title = sql_db.Column(sql_db.String(100), nullable=False)
    description = sql_db.Column(sql_db.String(100), nullable=True)
    done = sql_db.Column(sql_db.Boolean, default=False)
    created_at = sql_db.Column(
        sql_db.DateTime(timezone=True), server_default=func.now()
    )
    image_url = sql_db.Column(sql_db.Text, nullable=True)
    user_id = sql_db.Column(sql_db.String(36), sql_db.ForeignKey("user_db_model.id"))

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "done": self.done,
            "created_at": self.created_at,
            "image_url": self.image_url,
            "user_id": self.user_id,
        }


class UserDBModel(sql_db.Model):
    id = sql_db.Column(
        sql_db.String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    name = sql_db.Column(sql_db.String(100), nullable=False)
    email = sql_db.Column(sql_db.String(100), nullable=False, unique=True)
    password = sql_db.Column(sql_db.String(100), nullable=False)
    created_at = sql_db.Column(
        sql_db.DateTime(timezone=True), server_default=func.now()
    )
    image_url = sql_db.Column(sql_db.Text, nullable=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "created_at": self.created_at,
            "image_url": self.image_url,
        }


def encode_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow()
        + datetime.timedelta(days=1),  # Token expires in 1 day
    }
    return jwt.encode(payload, app.config["SECRET_KEY"], algorithm="HS256")


def decode_token(token):
    try:
        payload = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def auth(request):
    auth_header = request.headers.get("Authorization")
    if auth_header:
        token = auth_header.split(" ")[1]
        return decode_token(token)
    return None


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = auth(request)
        if user_id is None:
            app.logger.error("Unauthorized")
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)

    return decorated_function


@app.route("/")
def hello():
    return "Hello, the server is running!"


@app.route("/register", methods=["POST"])
def register():
    try:
        dto = register_user_dto(
            name=request.json.get("name"),
            email=request.json.get("email"),
            password=request.json.get("password"),
        )
        existing_user = UserDBModel.query.filter_by(email=dto.email).first()
        if existing_user:
            app.logger.error("User already exists")
            return jsonify({"error": "User already exists"}), 400

        user = UserDBModel(
            name=dto.name,
            email=dto.email,
            password=bcrypt.generate_password_hash(dto.password).decode("utf-8"),
        )
        sql_db.session.add(user)
        sql_db.session.commit()
        return jsonify(user.serialize()), 201
    except Exception as e:
        app.logger.error(f"Error registering user: {e}")
        return jsonify({"error": "Error registering user"}), 500


@app.route("/login", methods=["POST"])
def login():
    try:
        dto = login_user_dto(
            email=request.json["email"], password=request.json["password"]
        )
        user = UserDBModel.query.filter_by(email=dto.email).first()
        if not user or not bcrypt.check_password_hash(user.password, dto.password):
            app.logger.error("Invalid email or password")
            return jsonify({"error": "Invalid email or password"}), 401

        token = encode_token(user.id)
        return jsonify({"token": token})
    except Exception as e:
        app.logger.error(f"Error logging in: {e}")
        return jsonify({"error": "Error logging in"}), 500


@app.route("/check", methods=["GET"])
def check():
    try:
        user_id = auth(request)
        if user_id is None:
            app.logger.error("Invalid or expired token")
            return jsonify({"error": "Invalid or expired token"}), 401
        user = UserDBModel.query.get(user_id)
        return jsonify(user.serialize())
    except Exception as e:
        app.logger.error(f"Error checking token: {e}")
        return jsonify({"error": "Error checking token"}), 500


@app.route("/refresh", methods=["POST"])
def refresh():
    try:
        user_id = auth(request)
        if user_id is None:
            app.logger.error("Invalid or expired token")
            return jsonify({"error": "Invalid or expired token"}), 401
        token = encode_token(user_id)
        return jsonify({"token": token})
    except Exception as e:
        app.logger.error(f"Error refreshing token: {e}")
        return jsonify({"error": "Error refreshing token"}), 500


@app.route("/user", methods=["GET"])
@login_required
def get_user():
    try:
        user_id = auth(request)
        user = UserDBModel.query.get(user_id)
        return jsonify(user.serialize())
    except Exception as e:
        app.logger.error(f"Error fetching user: {e}")
        return jsonify({"error": "Error fetching user"}), 500


@app.route("/todos", methods=["GET"])
@login_required
def get_todos():
    try:
        user_id = auth(request)
        todos = DBModel.query.filter_by(user_id=user_id).all()
        return jsonify({"todos": [todo.serialize() for todo in todos]})
    except Exception as e:
        app.logger.error(f"Error fetching todos: {e}")
        return jsonify({"error": "Error fetching todos"}), 500


@app.route("/todos/<string:id>", methods=["GET"])
@login_required
def get_todo_by_id(id):
    try:
        todo = DBModel.query.get(id)
        if not todo:
            app.logger.error("Todo not found")
            return jsonify({"error": "Todo not found"}), 404
        return jsonify(todo.serialize())
    except Exception as e:
        app.logger.error(f"Error fetching todo by id: {e}")
        return jsonify({"error": "Error fetching todo"}), 500


@app.route("/todos", methods=["POST"])
@login_required
def create_todo():
    try:
        user_id = auth(request)
        dto = create_todo_dto(
            title=request.json.get("title"),
            description=request.json.get("description"),
            done=request.json.get("done"),
            image_url=request.json.get("image_url"),
        )
        todo = DBModel(
            title=dto.title,
            description=dto.description,
            done=dto.done,
            image_url=dto.image_url,
            user_id=user_id,
        )
        sql_db.session.add(todo)
        sql_db.session.commit()
        return jsonify(todo.serialize()), 201
    except ValueError as e:
        app.logger.error(f"Validation error: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        app.logger.error(f"Error creating todo: {e}")
        return jsonify({"error": "Error creating todo"}), 500


@app.route("/todos/<string:id>", methods=["PUT"])
@login_required
def update_todo_by_id(id):
    try:
        todo = DBModel.query.get(id)
        if not todo:
            app.logger.error("Todo not found")
            return jsonify({"error": "Todo not found"}), 404
        dto = update_todo_by_id_dto(
            id=id,
            title=request.json.get("title"),
            description=request.json.get("description"),
            done=request.json.get("done"),
            image_url=request.json.get("image_url"),
        )
        if dto.title is not None:
            todo.title = dto.title if dto.title else None
        if dto.description is not None:
            todo.description = dto.description if dto.description else None
        if isinstance(dto.done, bool):
            todo.done = dto.done
        if dto.image_url is not None:
            todo.image_url = dto.image_url if dto.image_url else None
        sql_db.session.commit()
        return jsonify(todo.serialize())
    except ValueError as e:
        app.logger.error(f"Validation error: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        app.logger.error(f"Error updating todo: {e}")
        return jsonify({"error": "Error updating todo"}), 500


@app.route("/todos/<string:id>", methods=["DELETE"])
@login_required
def delete_todo_by_id(id):
    try:
        todo = DBModel.query.get(id)
        if not todo:
            app.logger.error("Todo not found")
            return jsonify({"error": "Todo not found"}), 404
        sql_db.session.delete(todo)
        sql_db.session.commit()
        return jsonify({"message": "Todo deleted"})
    except Exception as e:
        app.logger.error(f"Error deleting todo: {e}")
        return jsonify({"error": "Error deleting todo"}), 500


@app.route("/update_user", methods=["PUT"])
@login_required
def update_user():
    try:
        user_id = auth(request)
        user = UserDBModel.query.get(user_id)
        if not user:
            app.logger.error("User not found")
            return jsonify({"error": "User not found"}), 404
        image_url = request.json.get("image_url")
        user.image_url = image_url
        sql_db.session.commit()
        return jsonify(user.serialize())
    except Exception as e:
        app.logger.error(f"Error updating user: {e}")
        return jsonify({"error": "Error updating user"}), 500


if __name__ == "__main__":
    app.run(port=5000, debug=True, threaded=True)
