from flask import Blueprint, render_template, abort, request, redirect, url_for
import datetime

from OOZero.user_model import getUser
from OOZero.user_session import login_required, current_username
from OOZero.event_model import getEventsByOwner, getEventById, createEvent, editEvent, removeEvent, EventType, getAllEvents
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
    user = getUser(current_username())
    search = request.args.get('q')
    search = search if search else ''
    return render_template('events.html', events=getEventsByOwner(user, search=search),
                           username=current_username, search=search, EventType=EventType, pyDatetimeToMoment=pyDatetimeToMoment)

@events.route('/create', methods=('POST', 'GET'))
@login_required
def create_or_edit():
    """Create or update an event. If id is passed as a a query parameter then update
       the event corresponding to that query parameter.
    """
    error = None
    if request.method == 'POST':
        id = request.form.get('id')
        id = int(id) if id else None
        # Edit or create the event based on whether we have an id and also
        # the type of event that we have.
        name = request.form.get('name')
        owner = getUser(current_username()).id
        event_type = EventType(int(request.form.get('event_type')))
        description = request.form['description']
        startTime = momentToPyDatetime(request.form['start_time']) if event_type == EventType.EVENT or event_type == EventType.REMINDER else None
        endTime = momentToPyDatetime(request.form['end_time']) if event_type == EventType.EVENT else None
        password = request.form['event_password'] if event_type == event_type.ENCRYPTED else None
        
        if id:
            editEvent(id, name=name, owner=owner, event_type=event_type, description=description, start_time=startTime, end_time=endTime, password=password)
        else:
            createEvent(name=name, owner=owner, event_type=event_type, description=description, start_time=startTime, end_time=endTime, password=password)
        return redirect(url_for('events.index'))

    # Get an event if we are editing an event
    id = request.args.get('id')
    event = None
    if id:
        event = getEventById(int(id))

    return render_template('events_create.html', event=event,
                           username=current_username(), EventType=EventType,
                           error=error)


@events.route('/remove/<int:id>', methods=('POST',))
@login_required
def remove(id):
    """Remove an event with this id.
    """
    removeEvent(id)
    return redirect(url_for('events.index'))
