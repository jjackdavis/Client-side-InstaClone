"""Following Page."""
import flask
from flask import abort
from insta485.views.comments import redirection
import insta485


@insta485.app.route('/following/', methods=['POST'])
def follow():
    """Following Page."""
    operation = flask.request.form.get('operation')
    username = flask.request.form.get('username')
    logname = flask.session['username']
    # Connect to database
    connection = insta485.model.get_db()

    if operation == 'follow':
        # Make sure user is not already following
        curr = connection.execute(
            "SELECT * FROM following "
            "WHERE username1 = ? "
            "AND username2 = ?",
            (logname, username)
        )
        already_following = curr.fetchone()
        if already_following:
            abort(409)

        connection.execute(
            "INSERT INTO following "
            "(username1, username2) VALUES "
            "(?, ?)",
            (logname, username)
        )
    else:
        # Make sure user is not already not following
        curr = connection.execute(
            "SELECT * FROM following "
            "WHERE username1 = ? "
            "AND username2 = ?",
            (logname, username)
        )
        already_following = curr.fetchone()
        if already_following is None:
            abort(409)

        connection.execute(
            "DELETE FROM following "
            "WHERE username1 = ? "
            "AND username2 = ?",
            (logname, username)
        )

    connection.commit()
    return redirection()
