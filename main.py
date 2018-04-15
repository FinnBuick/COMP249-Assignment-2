__author__ = 'Steve Cassidy'

from bottle import Bottle, template, static_file, request
import interface

app = Bottle()


@app.route('/')
@app.route('/jobsearch')
def index(db):
    """Handles the initial page by displaying a list
     of positions to the user"""

    global info

    info = {
        'title': 'Welcome to Jobs',
        'message': 'Hello World!'
    }

    list = interface.position_list(db)

    return template('index', info, list=list)


@app.route('/positions/<id>')
def positions(db, id):
    """Handles the position page by displaying the details of a
    single position listing"""

    position = interface.position_get(db, id)

    return template('position',info, position=position)


@app.route('/static/<filename:path>')
def static(filename):
    """Static file handler"""

    return static_file(filename=filename, root='static')


@app.route('/about')
def about():
    """Handles the about page"""
    return template('about', info)




if __name__ == '__main__':

    from bottle.ext import sqlite
    from database import DATABASE_NAME
    # install the database plugin
    app.install(sqlite.Plugin(dbfile=DATABASE_NAME))
    app.run(debug=True, port=8010)
