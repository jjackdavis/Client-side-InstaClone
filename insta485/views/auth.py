"""Auth Page."""
import flask
from flask import abort
import insta485


@insta485.app.route('/accounts/auth/')
def status():
    """Doc string."""
    if 'username' in flask.session:
        return '', 200
    abort(403)
