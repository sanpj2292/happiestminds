from dictionary import app
from flask import render_template, request
import os
from .common.utils import readFile, insert_words, get_dictionary
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
        context['data'] = insert_words(list(words_set))

    return render_template('index.html', **context)


@app.route('/search_word', methods=['GET'])
def search_word():
    context = {}
    if request.method == 'GET':
        if request.args.get('word') is not None:
            dictionary = get_dictionary(request.args['word'])
            if dictionary is not None:
                context['word'] = dictionary.word.capitalize()
                context['meaning'] = dictionary.meanings
                context['synonym'] = dictionary.synonyms
                context['antonym'] = dictionary.antonyms
            else:
                context['empty'] = 'Not available in DB!'
        else:
            context['empty'] = 'The search box is Empty! Kindly please fill it and try again!!'

        return render_template('index.html', **context)