from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from app.main import main_bp
    app.register_blueprint(main_bp)

    # Other app setup (e.g., logging, extensions)

    return app

# Import models at the bottom to avoid circular dependencies
from app import models
