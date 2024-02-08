"""Doc string."""
import flask
from flask import url_for, request, redirect, abort
import insta485


@insta485.app.route('/comments/', methods=['POST'])
def comment_actions():
    """Doc string."""
    operation = flask.request.form.get('operation')
    logname = flask.session['username']
    connection = insta485.model.get_db()

    if operation == 'create':
        text = flask.request.form.get('text')
        if len(text) == 0:
            abort(400)
        postid = flask.request.form.get('postid')
        connection.execute(
            "INSERT INTO comments "
            "(owner, postid, text) VALUES "
            "(?, ?, ?)",
            (logname, postid, text)
        )
    else:
        commentid = flask.request.form.get('commentid')
        curr = connection.execute(
            "SELECT * FROM comments "
            "WHERE commentid = ?",
            (commentid,)
        )
        owner = curr.fetchone()["owner"]
        if owner != logname:
            abort(403)

        connection.execute(
            "DELETE FROM comments "
            "WHERE commentid = ?",
            (commentid,)
        )

    connection.commit()
    return redirection()


def redirection():
    """Redirect."""
    target_url = request.args.get('target')
    if target_url:
        return redirect(target_url)
    return redirect(url_for('show_index'))
