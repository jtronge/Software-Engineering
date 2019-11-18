from flask import Blueprint, render_template, abort, request, redirect, url_for
from OOZero.user_model import getUser
from OOZero.user_session import login_required, current_username
from OOZero.event_model import getAllEvents, createEvent, EventType

events = Blueprint('events', __name__, template_folder='templates')

@events.route('/')
@login_required
def index():
    return render_template('events.html', events=getAllEvents(), username=current_username)

@events.route('/create', methods=['POST', 'GET'])
@login_required
def create():
    error = None
    if request.method == 'POST':
        name = request.form['name']
        owner = getUser(current_username()).id
        event_type = EventType(int(request.form['event_type']))
        description = request.form['description']
        createEvent(name=name, owner=owner, event_type=event_type, description=description)
        return redirect(url_for('events.index'))
    return render_template('events_create.html', username=current_username(), EventType=EventType, error=error)

