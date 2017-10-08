DEBUG = True

SERVER_NAME = 'localhost:5000'
SECRET_KEY = 'insecurekeyfordev'

SQLALCHEMY_DATABASE_URI = 'sqlite+pysqlite:///world_manager.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

CELERY_USER_NAME = 'world-manager-celery-dev'
CELERY_VHOST = 'world-manager-vhost'
CELERY_BROKER_URL = f'amqp://{CELERY_USER_NAME}:{SECRET_KEY}' \
                    f'@localhost:5672/{CELERY_VHOST}'

CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
