"""Doc string."""
import flask
from insta485.api.basic_auth import basic_auth
import insta485


@insta485.app.route('/api/v1/comments/<commentid>/', methods=['DELETE'])
def delete_comment(commentid):
    """Doc string."""
    logname, success = basic_auth()
    if not success:
        return logname, 403
    connection1 = insta485.model.get_db()

    curr = connection1.execute(
        "SELECT * FROM comments "
        "WHERE commentid = ?",
        (commentid,)
    )
    result = curr.fetchone()
    if not result:
        return flask.jsonify({"message": "Commentid not found",
                              "status_code": 404}), 404
    if result["owner"] != logname:
        return flask.jsonify({"message": "Permission denied",
                              "status_code": 403}), 403

    connection1.execute(
        "DELETE FROM comments "
        "WHERE commentid = ?",
        (commentid,)
    )

    connection1.commit()
    return '', 204
