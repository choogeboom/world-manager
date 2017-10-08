
SERVER_NAME = 'actualservername'
SECRET_KEY = 'generateastrong128chartoken'

CELERY_USER_NAME = 'actualusername'
CELERY_VHOST = 'actualvhost'
CELERY_PASSWORD = 'amuchmoresecurepassword'
CELERY_BROKER_URL = f'amqp://{CELERY_USER_NAME}:{CELERY_PASSWORD}' \
                    f'@localhost:5672/{CELERY_VHOST}'

CELERY_RESULT_BACKEND = CELERY_BROKER_URL