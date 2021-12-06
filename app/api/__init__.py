from flask import Blueprint

bp = Blueprint('api', __name__)

from app.api import companies, friends_in_common, people, errors
