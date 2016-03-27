import os

celery_broker_url = 'redis://localhost:6379'
celery_result_url = 'redis://localhost:6379'
dirs = dict(
    template = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'),
    static = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static'),
)

