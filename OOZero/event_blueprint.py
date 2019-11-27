from flask import Blueprint, render_template, abort, request, redirect, url_for
import datetime

from OOZero.user_model import getUser
from OOZero.user_session import login_required, current_username
from OOZero.event_model import getEventsByOwner, createEvent, EventType

events = Blueprint('events', __name__, template_folder='templates')

@events.route('/')
@login_required
def index():
    user = getUser(current_username())
    search = request.args.get('q')
    return render_template('events.html',
                           events=getEventsByOwner(user, search=search),
                           username=current_username(), search=search, EventType=EventType)

@events.route('/create', methods=['POST', 'GET'])
@login_required
def create():
    error = None
    if request.method == 'POST':
        name = request.form['name']
        owner = getUser(current_username()).id
        start_time = request.form['start_time']
        if start_time:
            start_time = datetime.datetime.strptime(start_time, '%m/%d/%Y')
        end_time = request.form['end_time']
        if end_time:
            end_time = datetime.datetime.strptime(end_time, '%m/%d/%Y')
        event_type = EventType(int(request.form['event_type']))
        description = request.form['description']

        # Create the event based on the different types
        if event_type == EventType.EVENT:
            createEvent(name=name, owner=owner, event_type=event_type,
                        description=description, start_time=start_time,
                        end_time=end_time)
        elif event_type == EventType.REMINDER:
            createEvent(name=name, owner=owner, event_type=event_type,
                        description=description, start_time=start_time)
        else:
            createEvent(name=name, owner=owner, event_type=event_type,
                        description=description)
        return redirect(url_for('events.index'))
    return render_template('events_create.html',
                           username=current_username(), EventType=EventType,
                           error=error)

