from flask import Flask
from .common.database import Database
import os

app = Flask(__name__)
app.secret_key = '615ddcac99174986940fef298c01b957'
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                           'static', 'upload')
ALLOWED_EXTENSIONS = {'txt'}
db = Database.initialize()