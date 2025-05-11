import os
from flask import Flask


def create_app():
    from .models import init_db
    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    init_db(app)
    # Importar y registrar blueprints
    from .routes.dashboard import dashboard_bp
    from .routes.auth import auth_bp
    from .routes.admin import admin_bp
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, urlprefix='/')

    return app