from flask import Flask
from flask_cors import CORS


import os

application = Flask(__name__)
application.debug = True
application.secret_key = os.urandom(16)

from app import routes
