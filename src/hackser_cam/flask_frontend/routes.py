from .home_page import home
from flask import render_template, jsonify

from .. import shared_resource

@home.route('/', methods=["GET"])
def home_():
    return render_template('home.html')

@home.route('/get-data')
def get_data():

    #data = list()
    with shared_resource.data_lock:
        data = shared_resource.global_fuzzies

    return jsonify({'data': data})
