"""Docstring."""
import flask
from insta485.api.basic_auth import basic_auth
import insta485


@insta485.app.route('/api/v1/posts/')
def newest_posts():
    """Return most recent posts."""
    logname, success = basic_auth()
    if not success:
        return logname, 403

    # Connect to database
    connection = insta485.model.get_db()
    # Default vals specified here (postid is j most recent)
    page = flask.request.args.get('page', default=0, type=int)
    size = flask.request.args.get('size', default=10, type=int)
    postid_lte = flask.request.args.get('postid_lte', default=None, type=int)

    if size <= 0 or page < 0:
        return flask.jsonify({"message": "Bad Request",
                              "status_code": 400}), 400

    if not postid_lte:
        cur = connection.execute(
            "SELECT * "
            "FROM posts WHERE owner = ? "
            "UNION "
            "SELECT p.* "
            "FROM posts p "
            "JOIN following f ON p.owner = f.username2 "
            "WHERE f.username1 = ? "
            "ORDER BY postid DESC "
            "LIMIT 1",
            (logname, logname)
        )
        result = cur.fetchone()

        if result:
            postid_lte = result['postid']

    # Query database for posts
    cur = connection.execute(
        "SELECT p.* "
        "FROM posts p "
        "WHERE p.owner = ? AND p.postid <= ? "
        "UNION "
        "SELECT p.* "
        "FROM posts p "
        "JOIN following f ON p.owner = f.username2 "
        "WHERE f.username1 = ? AND p.postid <= ? "
        "ORDER BY p.postid DESC "
        "LIMIT ? OFFSET ? * ?",
        (logname, postid_lte, logname, postid_lte, size, size, page)
    )
    posts = cur.fetchall()

    if len(posts) < size:
        next_page = ""
    else:
        page += 1
        next_page = (
            f"/api/v1/posts/?size={size}"
            f"&page={page}&postid_lte={postid_lte}"
        )

    if flask.request.query_string.decode() == "":
        url = flask.request.path
    else:
        url = flask.request.path + "?" + flask.request.query_string.decode()

    context = {
        "next": next_page,
        "results": [],
        "url": url
    }
    for post in posts:
        context["results"].append({
            "postid": post["postid"],
            "url": f"/api/v1/posts/{post['postid']}/"
        })

    return flask.jsonify(**context), 200
