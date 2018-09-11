import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from miniURL.db import get_db

bp_auth = Blueprint('auth', __name__, url_prefix='/auth')

@bp_auth.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error_msg = None

        if not username:
            error_msg = 'Username is required'
        elif not password:
            error_msg = 'Password is required'
        elif db.execute(
            'SELECT id FROM user where username = ?', (username,)
        ).fetchone() is not None:
            error_msg = 'Username {} has alread been registered.'.format(username)
        
        if error_msg is None:
            db.execute('INSERT INTO user (username, password) VALUES (?, ?)',
                        (username, generate_password_hash(password)))
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error_msg)

    return render_template('auth/register.html')

@bp_auth.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error_msg = None

        if not username:
            error_msg = 'Username is required'
        elif not password:
            error_msg = 'Password is required'
        else:
            user = db.execute('SELECT * FROM user WHERE username = ?', (username,)
                        ).fetchone()
            if user is None or not check_password_hash(user['password'], password):
                error_msg = 'Incorrect username or password.'
        
        if error_msg is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        
        flash(error_msg)
    
    return render_template('auth/login.html')

@bp_auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

@bp_auth.before_app_request
def load_user_info():
    """
    Load user information if user has logged in before handling every requests.
    """
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute('SELECT * FROM user WHERE id = ?', (user_id,)
            ).fetchone()

def login_required(view):
    """
    Decorator used for other views to require login.
    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
