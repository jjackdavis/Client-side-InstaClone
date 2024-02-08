"""Logout Page."""
import flask
from flask import url_for, redirect
import insta485


@insta485.app.route('/accounts/logout/', methods=['POST'])
def show_logout():
    """Logout Page."""
    flask.session.clear()
    return redirect(url_for('show_login'))
