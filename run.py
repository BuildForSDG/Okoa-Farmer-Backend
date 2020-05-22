from flask import Flask

app = Flask(__name__)


def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)

    from src.models.Model import db
    db.init_app(app)

    return app
