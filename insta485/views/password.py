"""Update Password Page."""
import flask
from flask import url_for, redirect
import insta485


@insta485.app.route('/accounts/password/')
def update_password():
    """Update Password Page."""
    if 'username' not in flask.session:
        return redirect(url_for('show_login'))
    logname2 = flask.session['username']
    context1 = {
        "logname": logname2,
    }
    return flask.render_template("password.html", **context1)
