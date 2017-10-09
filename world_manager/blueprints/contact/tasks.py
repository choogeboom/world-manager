from utils.flask_mailplus import send_template_message
from world_manager.app import create_celery_app

celery = create_celery_app()


@celery.task()
def deliver_contact_email(email, message):
    """
    Send a contact e-mail

    :param email:
    :param message:
    :return:
    """
    context = {'email': email, 'message': message}

    send_template_message(subject='[World Manager] Contact',
                          sender=email,
                          recipients=[celery.conf.get('MAIL_USERNAME')],
                          reply_to=email,
                          template='contact/mail/index',
                          ctx=context)
