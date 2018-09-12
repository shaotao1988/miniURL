from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from miniURL.db import get_db
from miniURL.util import shorten_URL, unshorten_URL
from miniURL.auth import login_required

bp_miniURL = Blueprint('miniURL', __name__)

@bp_miniURL.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        long_URL = request.form['long_URL']
        err_msg = None
        shortURL = None
        if not long_URL or long_URL == "":
            err_msg = "Please input URL."
        else:
            db = get_db()
            url = db.execute("SELECT * FROM url WHERE long_URL = ?", (long_URL,)
                        ).fetchone()
            if url:
                shortURL = shorten_URL(url['id'])
            else:
                db.execute("INSERT INTO url (long_URL, owner_id) values (?, ?)", (long_URL, 1))
                db.commit()
                url = db.execute("SELECT * FROM url WHERE long_URL = ?", (long_URL,)
                        ).fetchone()
                shortURL = shorten_URL(['id'])
            return render_template('index.html', short_URL=shortURL)
        
        flash(err_msg, 'error')
    
    return render_template('index.html', short_URL=None)

@bp_miniURL.route('/dashboard')
@login_required
def dashboard():
    return render_template('index.html')
