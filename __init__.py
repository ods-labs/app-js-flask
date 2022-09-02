import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    from .config import ProductionConfig, DevelopementConfig
    if os.environ.get('FLASK_ENV') == 'development':
        app.config.from_object(DevelopementConfig)
    else:
        app.config.from_object(ProductionConfig)

    db.init_app(app)

    from .blueprints import pages, rest_api_v1
    app.register_blueprint(pages.bp)
    app.register_blueprint(rest_api_v1.bp)

    return app