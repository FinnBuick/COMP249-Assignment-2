__author__ = 'Steve Cassidy'

from bottle import Bottle, template, static_file

app = Bottle()


@app.route('/')
@app.route('/jobsearch')
def index(db):

    info = {
        'title': 'Welcome to Jobs',
        'message': 'Hello World!'
    }

    return template('index', info)

@app.route('/static/<filename:path>')
def static(filename):
    return static_file(filename=filename, root='static')


@app.route('/about')
def about():

    info = {
        'title': 'Welcome to Jobs',
        'message': 'Hello World!'
    }

    return template('about', info)




if __name__ == '__main__':

    from bottle.ext import sqlite
    from database import DATABASE_NAME
    # install the database plugin
    app.install(sqlite.Plugin(dbfile=DATABASE_NAME))
    app.run(debug=True, port=8010)
