import os
from flask import Flask

# Use application factory to create Flask instance
# All the initialize should be here
def create_app(test_config = None):
    app = Flask(__name__, instance_relative_config = True)
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        DATABASE = os.path.join(app.instance_path, 'miniURL.sqlite'),
    )

    if test_config is None:
        # Load the configuration file when not testing(if it exists)
        app.config.from_pyfile('config.py', silent = True)
    else:
        # Load the test config
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    @app.route('/hello')
    def hello():
        return "Hello, World!"

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp_auth)

    return app
