from flask import Blueprint, render_template, abort, request, redirect, url_for
import datetime

from OOZero.user_model import getUser
from OOZero.user_session import login_required, current_username
from OOZero.event_model import getEventsByOwner, getEventById, createEvent, editEvent, removeEvent, EventType

events = Blueprint('events', __name__, template_folder='templates')

@events.route('/')
@login_required
def index():
    user = getUser(current_username())
    search = request.args.get('q')
    return render_template('events.html',
                           events=getEventsByOwner(user, search=search),
                           username=current_username(), search=search, EventType=EventType)

@events.route('/create', methods=('POST', 'GET'))
@login_required
def create_or_edit():
    """Create or update an event. If id is passed as a a query parameter then update
       the event corresponding to that query parameter.
    """
    error = None
    if request.method == 'POST':
        id = request.form.get('id')
        name = request.form.get('name')
        owner = getUser(current_username()).id

        start_time = request.form.get('start_time')
        if start_time:
            start_time = datetime.datetime.strptime(start_time, '%m/%d/%Y')

        end_time = request.form.get('end_time')
        if end_time:
            end_time = datetime.datetime.strptime(end_time, '%m/%d/%Y')

        event_type = EventType(int(request.form.get('event_type')))
        description = request.form['description']

        id = int(id) if id else None
        # Edit or create the event based on whether we have an id and also
        # the type of event that we have.
        if event_type == EventType.EVENT:
            if id:
                editEvent(id, name=name, owner=owner, event_type=event_type,
                          description=description, start_time=start_time,
                          end_time=end_time)
            else:
                createEvent(name=name, owner=owner, event_type=event_type,
                            description=description, start_time=start_time,
                            end_time=end_time)
        elif event_type == EventType.REMINDER:
            if id:
                editEvent(id, name=name, owner=owner, event_type=event_type,
                          description=description, start_time=start_time)
            else:
                createEvent(name=name, owner=owner, event_type=event_type,
                            description=description, start_time=start_time)
        else:
            if id:
                editEvent(id, name=name, owner=owner, event_type=event_type,
                          description=description)
            else:
                createEvent(name=name, owner=owner, event_type=event_type,
                            description=description)
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
