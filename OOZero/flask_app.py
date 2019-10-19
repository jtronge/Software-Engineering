from OOZero import create_app
from flask import Flask, render_template, request, redirect, url_for
from OOZero.user_model import authenticateUser, addUser
from OOZero.user_session import login_required, user_login, user_logout

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
def events():
    '''Main events listing page.'''
    # TODO
    pass

@app.route('/events/create', methods=['POST', 'GET'])
def events_create():
    '''Create new events'''
    if request.method == 'POST':
        # TODO
        pass
    return render_template('events_create.html', error=error)

if __name__ == '__main__':
    app.run()
