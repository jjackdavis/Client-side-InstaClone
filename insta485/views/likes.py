"""Likes process."""
import flask
from flask import url_for, request, redirect, abort
import insta485


@insta485.app.route('/likes/', methods=['POST'])
def likes():
    """To like/unlike."""
    operation = flask.request.form.get('operation')
    postid = flask.request.form.get('postid')
    logname = flask.session['username']
    # Connect to database
    connection = insta485.model.get_db()

    # To like a post
    if operation == 'like':
        # Make sure they have not liked it previously
        curr = connection.execute(
            "SELECT * FROM likes "
            "WHERE owner = ? "
            "AND postid = ?",
            (logname, postid)
        )
        already_liked = curr.fetchone()
        if already_liked:
            abort(409)

        # Actually like the post
        connection.execute(
            "INSERT INTO likes "
            "(owner, postid) VALUES "
            "(?, ?)",
            (logname, postid)
        )
    else:
        # Make sure they cannot unlike if have not already liked
        curr = connection.execute(
            "SELECT * FROM likes "
            "WHERE owner = ? "
            "AND postid = ?",
            (logname, postid)
        )
        result = curr.fetchone()
        if not result:
            abort(409)

        connection.execute(
            "DELETE FROM likes "
            "WHERE owner = ? "
            "AND postid = ?",
            (logname, postid)
        )

    connection.commit()

    this_path = request.args.get('target')
    if this_path:
        return redirect(this_path)
    return redirect(url_for('show_index'))
