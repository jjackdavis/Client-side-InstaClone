"""Doc string."""
import flask
from insta485.api.basic_auth import basic_auth
import insta485


@insta485.app.route('/api/v1/comments/', methods=['POST'])
def add_comment():
    """Doc string."""
    logname, success = basic_auth()
    if not success:
        return logname, 403
    connection3 = insta485.model.get_db()

    postid2 = flask.request.args.get('postid', default=0, type=int)
    curr = connection3.execute(
        "SELECT * FROM posts "
        "WHERE postid = ?",
        (postid2,)
    )
    result = curr.fetchone()
    if not result:
        return flask.jsonify({"message": "Post not found",
                              "status_code": 404}), 404

    text = flask.request.json.get('text')
    connection3.execute(
        "INSERT INTO comments "
        "(owner, postid, text) VALUES "
        "(?, ?, ?)",
        (logname, postid2, text)
    )
    curr = connection3.execute(
        "SELECT last_insert_rowid()"
        "FROM comments"
    )
    lastid = curr.fetchone()["last_insert_rowid()"]

    curr = connection3.execute(
        "SELECT * "
        "FROM comments "
        "WHERE commentid = ?",
        (lastid,)
    )

    return flask.jsonify(curr.fetchone()), 201
