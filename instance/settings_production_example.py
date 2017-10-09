
SERVER_NAME = 'actualservername'
SECRET_KEY = 'generateastrong128chartoken'

MAIL_USERNAME = 'you@gmail.com'
MAIL_PASSWORD = 'areallystrongpassword'

CELERY_USER_NAME = 'actualusername'
CELERY_VHOST = 'actualvhost'
CELERY_PASSWORD = 'amuchmoresecurepassword'
CELERY_BROKER_URL = f'amqp://{CELERY_USER_NAME}:{CELERY_PASSWORD}' \
                    f'@localhost:5672/{CELERY_VHOST}'

CELERY_RESULT_BACKEND = CELERY_BROKER_URL
