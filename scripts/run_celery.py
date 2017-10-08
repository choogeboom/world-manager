from world_manager.app import create_celery_app

app = create_celery_app()

app.start(['', 'worker', '-B', '-l', 'info'])
