"""Edit Page."""
import flask
from flask import url_for, redirect
import insta485


@insta485.app.route('/accounts/edit/')
def edit_info():
    """Edit Page."""
    if 'username' not in flask.session:
        return redirect(url_for('show_login'))

    connection, logname = authorize_user()

    curr = connection.execute(
        "SELECT email "
        "FROM users "
        "WHERE username = ? ",
        (logname,)
    )
    email = curr.fetchone()["email"]

    curr = connection.execute(
        "SELECT fullname "
        "FROM users "
        "WHERE username = ? ",
        (logname,)
    )
    fullname = curr.fetchone()["fullname"]

    curr = connection.execute(
        "SELECT filename "
        "FROM users "
        "WHERE username = ? ",
        (logname,)
    )
    filename = curr.fetchone()["filename"]

    context = {
        "logname": logname,
        "email": email,
        "fullname": fullname,
        "filename": filename
    }
    return flask.render_template("edit.html", **context)


def authorize_user():
    """Authorize."""
    logname = flask.session['username']
    connection = insta485.model.get_db()
    return connection, logname
