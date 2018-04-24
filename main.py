__author__ = 'Finneas Buick'

from bottle import Bottle, template, static_file, request, redirect
import interface, users

app = Bottle()

INFO = {
        'title': 'Welcome to Jobs',
        'message': 'Hello World!'
    }

@app.route('/')
@app.route('/jobsearch')
def index(db):
    """Handles the initial page by displaying a positions
     of positions to the user"""

    positions = interface.position_list(db)
    user = users.session_user(db)

    return template('index', INFO, positions=positions, user=user)


@app.route('/positions/<id>')
def positions(db, id):
    """Handles the position page by displaying the details of a
    single position listing"""

    position = interface.position_get(db, id)

    return template('position',INFO, position=position)


@app.route('/static/<filename:path>')
def static(filename):
    """Static file handler"""

    return static_file(filename=filename, root='static')


@app.route('/about')
def about():
    """Handles the about page"""

    return template('about', INFO)

@app.route('/login', method="POST")
def login(db):
    """Handles login"""

    username = request.forms.get('nick')
    password = request.forms.get('password')

    if users.check_login(db, username, password):
        users.generate_session(db, username)
        redirect('/')
    else:
        positions = interface.position_list(db)
        messages = 'Login Failed, please try again'
        redirect('/')


@app.route('/logout', method='POST')
def logout(db):
    """Handles logout"""

    user = users.session_user(db)
    users.delete_session(db, user)
    redirect('/')


if __name__ == '__main__':

    from bottle.ext import sqlite
    from database import DATABASE_NAME
    # install the database plugin
    app.install(sqlite.Plugin(dbfile=DATABASE_NAME))
    app.run(debug=True, port=8010)
