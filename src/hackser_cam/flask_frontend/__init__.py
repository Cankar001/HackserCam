from flask import Flask

app = Flask(__name__)

from .home_page import home

app.register_blueprint(home, url_prefix="")
