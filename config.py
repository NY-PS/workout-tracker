import os

DEBUG = os.environ.get('FLASK_ENV') == 'development'
BCRYPT_LOG_ROUNDS = 12
LOGS_DIR = os.path.join(
    os.path.abspath(
        os.path.dirname(__file__)
    ),
    'instance',
    'logs'
)
