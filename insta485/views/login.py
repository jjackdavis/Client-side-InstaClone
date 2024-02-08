"""Login Page."""
import flask
from flask import url_for, redirect
import insta485


@insta485.app.route('/accounts/login/')
def show_login():
    """Login Page."""
    if 'username' in flask.session:
        return redirect(url_for('show_index'))

    return flask.render_template("login.html")
