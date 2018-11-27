
""" Main application module. """

from flask import Flask, request

app = Flask(__name__)

from app.app_config import *
from app.views import tracking
