from flask import Blueprint, render_template, abort, request, redirect, url_for
from OOZero.user_model import getUser
from OOZero.user_session import login_required, current_username
from OOZero.event_model import getAllEvents, createEvent, EventType
import datetime

events = Blueprint('events', __name__, template_folder='templates')

def momentToPyDatetime(date):
    '''Parse datetime string from moment.js to datetime object'''
    return datetime.datetime.strptime(date, '%m/%d/%Y %H:%M %p')

def pyDatetimeToMoment(date):
    '''Format datetime object to moment.js string'''
    if date is None:
        return ""
    else:
        return datetime.datetime.strftime(date, '%m/%d/%Y %H:%M %p')

@events.route('/')
@login_required
def index():
    search = request.args.get('q')
    search = search if search else ''
    return render_template('events.html', events=getAllEvents(search=search),
                           username=current_username, search=search, EventType=EventType, pyDatetimeToMoment=pyDatetimeToMoment)

@events.route('/create', methods=['POST', 'GET'])
@login_required
def create():
    error = None
    if request.method == 'POST':
        name = request.form['name']
        owner = getUser(current_username()).id
        event_type = EventType(int(request.form['event_type']))
        description = request.form['description']
        startTime = momentToPyDatetime(request.form['start_time']) if event_type == EventType.EVENT or event_type == EventType.REMINDER else None
        endTime = momentToPyDatetime(request.form['end_time']) if event_type == EventType.EVENT else None
        password = request.form['event_password'] if event_type == event_type.ENCRYPTED else None
        createEvent(name=name, owner=owner, event_type=event_type, description=description, start_time=startTime, end_time=endTime, password=password)
        return redirect(url_for('events.index'))
    return render_template('events_create.html', username=current_username(), EventType=EventType, error=error)

