import time
from flask import Flask

app = Flask(__name__, static_folder='../build', static_url_path='/')


@app.errorhandler(404)
def not_found(e):
    return 'Error404!'


@app.route('/')
def index():
    return '<h1>PP-Labeling-Backend API Works!</h1>'


@app.route('/api/time')
def get_current_time():
    return {'time': time.time()}
