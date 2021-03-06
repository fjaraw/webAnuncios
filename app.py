# -*- coding: utf-8 -*-
import os
from functools import wraps
from sqlite3 import dbapi2 as sqlite3
from flask import (Flask,
                session,
                render_template,
                url_for,
                request,
                flash,
                redirect,
                g)

import hashlib

salt = "a1s2d3f4g5"

app = Flask(__name__)

app.config.update(dict(
    DATABASE='entry.db',
    DEBUG=True,
    SECRET_KEY=u'0moHo~#3CD`M/:6'
))
#conexion con base de datos
def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv
#incicaliza base de datos
def init_db():
    """Creates the database tables."""
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
# obtener base de datos
def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db
#cerrar base de datos
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

#inicio de sesion
def logged_in(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user') is not None:
            return f(*args, **kwargs)
        else:
            flash('Please log in first.', 'error')
            return redirect(url_for('login'))
    return decorated_function
#formulario de anuncio
@app.route('/form')
@app.route('/form/<error>')
@logged_in
def form(error=None):
    return render_template('form.html', error=error)
#agregar anuncio
@app.route('/add', methods=['POST'])
@logged_in
def add_entry():
    if len(request.form['title']) >= 2:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('insert into entry (title, description, ubicacion, tag, fk_id_user) values (?, ?, ?, ?, ?)',
                     [request.form['title'], request.form['description'], request.form['ubicacion'], request.form['tag'], session.get('name')])
        db.commit()
        f = request.files["file_img"]
        #print f.__dict__
        if f.filename != "":
            pk = cursor.lastrowid
            name, ext = os.path.splitext(f.filename)
            filename = "{0}{1}".format(pk, ext)
            f.save('static/files/{0}'.format(filename))
            cursor.execute('update entry set image = ? WHERE id = ?', [filename, pk])
            db.commit()
        flash('La nueva entrada ha sido correctamente creada')
        return redirect(url_for('show_entries'))
    else:
        return redirect(url_for('form', error = u"El título no puede ser vacío"))
#modulo principal
@app.route('/index')
@logged_in
def show_entries():
    db = get_db()
    cur = db.execute('select title from entry order by title asc')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)

#iniciar sesion
@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form["user"]
        password = request.form["password"]
	hash_pass = hashlib.sha512((salt + password).encode('utf-8')).hexdigest()
        db = get_db()
        result = db.execute('select name, user from user where user=? and pass = ?', 
                            [user, hash_pass])
        matches = result.fetchall()
        if len(matches) > 0: #The user and pass combination exits
            user_data = matches[0]
            session['user'] = user
            session['name'] = user_data[1]
            return redirect(url_for('show_entries'))
        else:
            error = u"Usuario o contraseña incorrecto"
            return render_template('login.html', error=error)
        
    else:
        return render_template('login.html')

#cierre de sesion
@app.route('/logout')
@logged_in
def logout():
    # remove the user from the session if it's there
    session.pop('user')
    return redirect(url_for('login'))
#registrar usuario
@app.route('/signup', methods=['GET', 'POST'])
def signup():	
    if request.method == 'POST':
    	if len(request.form['name']) >= 2:
        	db = get_db()
       	 	cursor = db.cursor()
        	cursor.execute('insert into user (name, user, pass, dir, tel, mail) values (?, ?, ?, ?, ?, ?)',
                     [request.form['name'], request.form['user'], hashlib.sha512((salt + request.form['password']).encode('utf-8')).hexdigest(), request.form['dir'], request.form['tel'], request.form['e-mail']])
        	db.commit()
        	user = request.form["user"]
        	password = request.form["password"]
		hash_pass = hashlib.sha512((salt + password).encode('utf-8')).hexdigest()
        	result = db.execute('select name, user from user where user=? and pass = ?', 
                            [user, hash_pass])
        	matches = result.fetchall()
        	if len(matches) > 0: #The user and pass combination exits
            		user_data = matches[0]
            		session['user'] = user
            		session['name'] = user_data[1]
        		return redirect(url_for('show_entries'))
    		else:
        		return render_template('signup.html')
    	else:
        	return redirect(url_for('signup', error = u"El nombre no puede ser vacío"))
    else:
        return render_template('signup.html')

#busqueda
@app.route('/search', methods=['GET', 'POST'])
def search():    
	if request.method == 'POST':
		if len(request.form['busq']) >= 2:
			busqueda = "%"+request.form['busq']+"%"
			db = get_db()
			cur = db.execute('select title from entry where description LIKE ? OR title LIKE ?', (busqueda,busqueda))
			entries = cur.fetchall()
			print entries																																											
			return render_template('show_entries.html', entries=entries)
		else:
			return redirect(url_for('search', error = u"No ha buscado nada"))
	else:
		return render_template('search.html')

#configurar cuenta
@app.route('/config')
def config():
	u = session.get("user")
	db = get_db()
  	cur = db.execute('select name, pass, dir, tel, mail from user where user=?',(u,))
  	entries = cur.fetchall()
	return render_template('config.html', entries=entries)

@app.route('/setup', methods=['GET', 'POST'])
def config2():
	if request.method == 'POST':
		if len(request.form['name']) >= 2:
			u = session.get('user')
			db = get_db()
			cursor=db.execute('UPDATE user set name=?, pass=?, dir=?, tel=?, mail=? where user=?',(request.form["name"], hashlib.sha512((salt + request.form["pass"]).encode('utf-8')).hexdigest(), request.form["dir"], request.form["tel"], request.form["e-mail"], u))			
			db.commit()
  			return redirect(url_for('config'))	
		else:
			return redirect(url_for('config2', error = u"El nombre no puede ser vacío"))
	else:
		return render_template('config.html')
#filtros de busqueda
@app.route('/index/<ids>')
@logged_in
def route(ids):
    db = get_db()
    cur = db.execute('select title, description, ubicacion, image, tag, fk_id_user from entry where title=?',(ids,))
    entries = cur.fetchall()
    return render_template('route.html', entries=entries, id=id)

@app.route('/arriendo')
@logged_in
def arriendo():
    db = get_db()
    cur = db.execute('select title, description, image, tag from entry where tag="a"')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)

@app.route('/compra')
@logged_in
def compra():
    db = get_db()
    cur = db.execute('select title, description, image, tag from entry where tag="c"')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)

@app.route('/venta')
@logged_in
def venta():
    db = get_db()
    cur = db.execute('select title, description, image, tag from entry where tag="v"')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)

@app.route('/servicio')
@logged_in
def servicio():
    db = get_db()
    cur = db.execute('select title, description, image, tag from entry where tag="s"')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)

@app.route('/anuncios')
@logged_in
def anuncios():
	db = get_db()
	user = session.get('user')
	cur = db.execute('select title from entry where fk_id_user=? order by title asc',(user,))
	entries = cur.fetchall()
	return render_template('show_entries.html', entries=entries, id=id)

if __name__ == "__main__":
    app.run()
