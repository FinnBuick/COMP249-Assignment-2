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
    user = users.session_user(db)
    return template('position',INFO, position=position, user=user)


@app.route('/static/<filename:path>')
def static(filename):
    """Static file handler"""

    return static_file(filename=filename, root='static')


@app.route('/about')
def about(db):
    """Handles the about page"""
    user = users.session_user(db)
    return template('about', INFO, user=user)

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
        user = None
        return template('index', INFO, positions=positions, user=user, messages='Login Failed, please try again')

@app.route('/logout', method='POST')
def logout(db):
    """Handles logout"""

    user = users.session_user(db)
    users.delete_session(db, user)
    redirect('/')


@app.route('/post', method='POST')
def post_job(db):
    """Handles posting a new job and adding it to the database when a valid user is logged in"""

    user = users.session_user(db)
    title = request.forms.get('title')
    company = request.forms.get('company')
    location = request.forms.get('location')
    description = request.forms.get('description')

    interface.position_add(db, user, title, location, company, description)

    redirect('/')

if __name__ == '__main__':

    from bottle.ext import sqlite
    from database import DATABASE_NAME
    # install the database plugin
    app.install(sqlite.Plugin(dbfile=DATABASE_NAME))
    app.run(debug=True, port=8010)
