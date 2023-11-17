from flask import jsonify, render_template

from .. import shared_resource
from .home_page import home


@home.route("/", methods=["GET"])
def home_():
    return render_template("home.html")


@home.route("/get-data")
def get_data():
    # data = list()
    with shared_resource.data_lock:
        data = shared_resource.global_fuzzies

    return jsonify({"data": data})
