from dictionary import app, db
from flask import render_template, request
import os
from .common.utils import readFile, getWordData
from werkzeug.utils import secure_filename

@app.route('/')
def index():
    return render_template('index.html', context={'page_name': 'Home'})

@app.route('/createDict/', methods=['POST'])
def create_dict():
    context = {}
    if request.method == 'POST':
        f = request.files['file']
        fname = secure_filename(f.filename)
        fpath = os.path.join(app.config['UPLOAD_FOLDER'], fname)
        f.save(fpath)
        context['file'] = request.files['file'].filename
        context['is_uploaded'] = True
        context['page_name'] = 'Create Dict'
        words_set = readFile(fpath)
        context['data'] = getWordData(list(words_set))

    return render_template('index.html', **context)