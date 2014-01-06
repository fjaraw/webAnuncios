# -*- coding: utf-8 -*-
from sqlite3 import dbapi2 as sqlite3
from flask import (Flask,
                render_template,
                url_for,
                request,
                flash,
                redirect,
                g)

app = Flask(__name__)

app.config.update(dict(
    DATABASE='entry.db',
    DEBUG=True,
    SECRET_KEY='development key'
))

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def init_db():
    """Creates the database tables."""
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/form')
@app.route('/form/<error>')
def form(error=None):
    return render_template('form.html', error=error)

@app.route('/add', methods=['POST'])
def add_entry():
    if len(request.form['title']) >= 2:
        db = get_db()
        db.execute('insert into entry (title, description) values (?, ?)',
                     [request.form['title'], request.form['description']])
        db.commit()
        flash('La nueva entrada ha sido correctamente creada')
        return redirect(url_for('show_entries'))
    else:
        return redirect(url_for('form', error = u"El título no puede ser vacío"))
        #return form(error= u"El título no puede ser vacío")

@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('select title, description from entry order by id desc')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)

if __name__ == "__main__":
    app.run()