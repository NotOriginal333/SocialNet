from flask import Flask

from .config import Config
from .extensions import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from .routes.proxy import bp as proxy_bp
    app.register_blueprint(proxy_bp)

    return app
