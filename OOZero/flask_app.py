from OOZero import create_app
from flask import Flask, render_template, request, redirect, url_for
from OOZero.model import db
from OOZero.user_model import authenticateUser, addUser, getUser
from OOZero.event_model import Event
from OOZero.user_session import login_required, user_login, user_logout, user_current

app = create_app()

@app.route('/')
@login_required
def home():
    return render_template('home.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        # Authenticate the given user with this username and password
        username = request.form['username']
        password = request.form['password']
        user = authenticateUser(username, password)
        if user:
            user_login(user)
            return redirect(url_for('home'))
        else:
            error = 'Incorrect username or password entered.'

    return render_template('login.html', error=error)

@app.route('/logout', methods=['POST', 'GET'])
def logout():
    user_logout()
    return redirect(url_for('home'))

@app.route('/events')
@login_required
def events():
    """Main events listing page."""
    events = db.session.query(Event).all()
    return render_template('events.html', events=events)

@app.route('/events/create', methods=['POST', 'GET'])
@login_required
def events_create():
    """Create new events"""
    error = None
    if request.method == 'POST':
        # Get the current user
        user = getUser(user_current())
        event = Event(owner=user, name=request.form['name'],
                      description=request.form['description'],
                      start_time=request.form['start_time'],
                      end_time=request.form['end_time'],
                      event_type=request.form['event_type'])
        db.session.add(event)
        db.commit()
        return redirect(url_for('events'))
    return render_template('events_create.html', error=error)

if __name__ == '__main__':
    app.run()
