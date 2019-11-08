from flask import Blueprint, render_template, abort

events = Blueprint('events', __name__, template_folder='templates')

@events.route('/')
def index():
    pass

@events.route('/', method=['POST', 'GET'])
def create():
    pass

