from dynaconf import settings

broker_url = settings.CELERY_BROKER_URL
imports = ["periodic.tasks"]
result_backend = settings.CELERY_BROKER_URL
result_persistent = False
