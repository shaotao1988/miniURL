from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from miniURL.db import get_db

bp_miniURL = Blueprint('miniURL', __name__)

@bp_miniURL.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        long_URL = request.form['long_URL']
        err_msg = None
        if not long_URL or long_URL == "":
            err_msg = "Please input URL."
        else:
            db = get_db()
            url = db.execute("SELECT * FROM url WHERE long_URL = ?", (long_URL,)
                        ).fetchone()
            if url:
                print("URL {} already in database.".format(long_URL))
            else:
                db.execute("INSERT INTO url (long_URL, owner_id) values (?, ?)", (long_URL, 1))
                db.commit()
            return render_template('index.html', short_URL=long_URL)
        
        flash(err_msg, 'error')
    
    return render_template('index.html', short_URL=None)

@bp_miniURL.route('/dashboard')
def dashboard():
    return render_template('index.html')
