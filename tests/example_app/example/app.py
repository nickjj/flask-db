from flask import Flask

from flask_sqlalchemy import SQLAlchemy


# Inlining a bunch of things here for the sake of simplicity. Normally you'd
# break these out into separate files.
db = SQLAlchemy()

settings = {
    "SQLALCHEMY_DATABASE_URI": "sqlite:///exampledb",
    "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    "FLASK_DB_SEEDS_PATH": "db/seeds.py"
}


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(24), unique=True, index=True)

    @classmethod
    def find_by_username(cls, username):
        return User.query.filter(User.username == username).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

        return self


def create_app():
    app = Flask(__name__)

    app.config.update(settings)

    db.init_app(app)

    @app.route("/")
    def index():
        return "Hello world"

    return app
