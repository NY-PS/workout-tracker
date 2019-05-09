from flask import Flask, render_template
from flask_login import LoginManager
from utils import get_config

import os

LOGIN_MANAGER = LoginManager()
LOGIN_MANAGER.login_view = 'auth.login'


def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)

    # load the default configuration
    app.config.from_object('config')

    # load the instance config, if it exists
    app.config.from_pyfile('config.py', silent=True)

    app.config['SECRET_KEY'] = get_config()['secret_key']

    # ensure the instance directory exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    LOGIN_MANAGER.init_app(app)

    @app.route('/')
    def index():
        return render_template('index.html')

    # apply the app blueprints
    from workout_tracker.views import auth
    app.register_blueprint(auth.bp)

    return app
