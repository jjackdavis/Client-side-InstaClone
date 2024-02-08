"""Delete Page."""
import flask
from insta485.api.basic_auth import basic_auth
import insta485


@insta485.app.route("/api/v1/likes/<int:likeid_slug>/",
                    methods=["DELETE"])
def delete_like(likeid_slug):
    """Delete Page."""
    logname, success = basic_auth()
    if not success:
        return logname, 403

    likeid = likeid_slug

    connection = insta485.model.get_db()
    # Get like
    curr = connection.execute(
        "SELECT * "
        "FROM likes WHERE "
        "likeid = ?",
        (likeid,)
    )

    result = curr.fetchone()
    if not result:
        return flask.jsonify({"message": "Like not found",
                              "status_code": 404}), 404
    if result["owner"] != logname:
        return flask.jsonify({"message": "Permission denied",
                              "status_code": 403}), 403

    connection.execute(
        "DELETE FROM likes "
        "WHERE owner = ? "
        "AND likeid = ?",
        (logname, likeid)
    )

    return '', 204
