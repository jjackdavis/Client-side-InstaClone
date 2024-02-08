"""Add Page."""
import flask
from insta485.api.basic_auth import basic_auth
import insta485


@insta485.app.route("/api/v1/likes/", methods=["POST"])
def add_like():
    """Add like."""
    logname3, success1 = basic_auth()
    if not success1:
        return logname3, 403
    connection1 = insta485.model.get_db()
    postid1 = flask.request.args.get('postid', default=0, type=int)

    curr = connection1.execute(
        "SELECT * FROM posts "
        "WHERE postid = ?",
        (postid1,)
    )
    result = curr.fetchone()

    if not result:
        return flask.jsonify({"message": "Post not found",
                              "status_code": 404}), 404

    curr = connection1.execute(
        "SELECT * FROM likes "
        "WHERE owner = ? "
        "AND postid = ?",
        (logname3, postid1)
    )
    already_liked = curr.fetchone()

    if already_liked:
        likeid = already_liked['likeid']
        return flask.jsonify({"likeid": likeid,
                              "url": f'/api/v1/likes/{likeid}/'}), 200
    # Actually like the post
    connection1.execute(
        "INSERT INTO likes "
        "(owner, postid) VALUES "
        "(?, ?)",
        (logname3, postid1)
    )

    curr = connection1.execute(
        "SELECT * FROM likes "
        "WHERE owner = ? "
        "AND postid = ?",
        (logname3, postid1)
    )
    like = curr.fetchone()
    likeid = like['likeid']
    return flask.jsonify({"likeid": likeid,
                          "url": f'/api/v1/likes/{likeid}/'}), 201
