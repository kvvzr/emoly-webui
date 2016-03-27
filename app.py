import config
from celery import Celery, task
from flask import Flask, render_template, request

app = Flask(__name__)
app.debug = True

app.config.update(
    TEMPLATE_FOLDER=config.dirs['template'],
    STATIC_FOLDER=config.dirs['static'],
    CELERY_BROKER_URL=config.celery_broker_url,
    CELERY_RESULT_BACKEND=config.celery_result_url
)

def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

celery = make_celery(app)

@task(name='tasks.emolize')
def emolize(text):
    return text + 'おい'

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/emoly', methods=['POST'])
def emoly():
    text = request.form['text']
    result = emolize.delay(text)
    return str(result)

@app.route('/result/<job_key>', methods=['GET'])
def result(job_key):
    job = emolize.AsyncResult(job_key)
    ready = job.ready()
    if (ready):
        return str(job.get())
    else:
        return ('', 202)

if __name__ == '__main__':
    app.run()
