"""Delete Page."""
import flask
from flask import url_for, redirect
import insta485


@insta485.app.route('/accounts/delete/')
def delete_account():
    """Delete Page."""
    if 'username' not in flask.session:
        return redirect(url_for('show_login'))
    logname3 = flask.session['username']
    context = {
        "logname": logname3,
    }
    return flask.render_template("delete.html", **context)
