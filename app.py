import os

from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-change-me")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if not app.config["SQLALCHEMY_DATABASE_URI"]:
        raise RuntimeError("DATABASE_URL is not set. Check your .env file.")

    db.init_app(app)
    migrate.init_app(app, db)

    import models  # noqa: F401 — register models for migrations

    @app.route("/")
    def hello_world():
        return "<p>Hello, World!</p>"

    @app.route("/health")
    def health():
        return jsonify({"status": "ok"})

    @app.route("/health/db")
    def health_db():
        db.session.execute(text("SELECT 1"))
        return jsonify({"status": "ok", "database": "connected"})

    return app


app = create_app()
