import config
# from celery import Celery, task
from flask import Flask, render_template, request
from gensim.models.word2vec import Word2Vec
from gensim import matutils
from numpy import dot
import MeCab

app = Flask(__name__)
app.debug = True

app.config.update(
    TEMPLATE_FOLDER=config.dirs['template'],
    STATIC_FOLDER=config.dirs['static'],
    # CELERY_BROKER_URL=config.celery_broker_url,
    # CELERY_RESULT_BACKEND=config.celery_result_url
)

mecab = MeCab.Tagger('-d %s' % (config.mecab_dic_dir))

# def make_celery(app):
#     celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
#     celery.conf.update(app.config)
#     TaskBase = celery.Task
#     class ContextTask(TaskBase):
#         abstract = True
#         def __call__(self, *args, **kwargs):
#             with app.app_context():
#                 return TaskBase.__call__(self, *args, **kwargs)
#     celery.Task = ContextTask
#     return celery
#
# celery = make_celery(app)

all_model = Word2Vec.load_word2vec_format('model/all.txt', binary=False, unicode_errors='ignore')
emoji_model = Word2Vec.load_word2vec_format('model/emoji.txt', binary=False, unicode_errors='ignore')

def most_sim_vec(model, word=[]):
    model.init_sims(replace=True)
    dists = dot(model.syn0norm, word)
    best = matutils.argsort(dists, topn=1, reverse=True)
    return model.index2word[best[0]]

# @task(name='tasks.emolize')
def emolize(text):
    result = ''
    for line in text.split('\n'):
        for word in mecab.parse(line).split('\n'):
            features = word.split('\t')
            if len(features) < 2:
                continue
            result += features[0]
            info = features[1].split(',')
            pos = info[0]
            if pos in ['名詞', '動詞', '形容詞', '副詞']:
                try:
                    base = info[6]
                    result += most_sim_vec(emoji_model, all_model[base])
                except Exception:
                    pass
        result += '\n'
    return result

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/emoly', methods=['POST'])
def emoly():
    text = request.form['text']
    # result = emolize.delay(text)
    # return str(result)
    return str(emolize(text))

# @app.route('/result/<job_key>', methods=['GET'])
# def result(job_key):
#     job = emolize.AsyncResult(job_key)
#     ready = job.ready()
#     if (ready):
#         return str(job.get())
#     else:
#         return ('', 202)

if __name__ == '__main__':
    app.run()
