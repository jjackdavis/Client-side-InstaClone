"""Create User Page."""
import flask
from flask import url_for, redirect
import insta485


@insta485.app.route('/accounts/create/')
def create_user():
    """Create User Page."""
    if 'username' in flask.session:
        return redirect(url_for('edit_info'))
    context = {}
    return flask.render_template("create.html", **context)
