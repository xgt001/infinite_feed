from flask import Flask
from controllers import facebook

app = Flask(__name__)

app.register_blueprint(facebook, url_prefix='/')
