"""REST API for posts."""
import flask
from insta485.api.basic_auth import basic_auth
import insta485


@insta485.app.route("/api/v1/posts/<int:postid_url_slug>/", methods=["GET"])
def get_post(postid_url_slug):
    """Return post on postid."""
    logname, success = basic_auth()
    if not success:
        return logname, 403

    connection = insta485.model.get_db()

    # Get single post
    curr = connection.execute(
        "SELECT * FROM posts "
        "WHERE postid=?",
        (postid_url_slug, )
    )
    post_result = curr.fetchone()
    if not post_result:
        return flask.jsonify({"message": "Not Found",
                              "status_code": 404}), 404

    # Get the post owner profile img
    curr = connection.execute(
        "SELECT * "
        "FROM users "
        "WHERE username = ?",
        (post_result["owner"],)
    )
    owner_img_url = curr.fetchone()["filename"]

    # Get 'likes' object for single post according to spec
    curr = connection.execute(
        "SELECT COUNT(*) AS like_count "
        "FROM likes "
        "WHERE postid = ?",
        (postid_url_slug,)
    )
    like_count = curr.fetchone()["like_count"]

    curr = connection.execute(
        "SELECT COUNT(*) AS liked "
        "FROM likes "
        "WHERE postid = ? AND owner = ?",
        (post_result["postid"], logname)
    )
    logname_liked = curr.fetchone()["liked"]

    if logname_liked:
        logname_liked = True
        curr = connection.execute(
            "SELECT * "
            "FROM likes "
            "WHERE postid = ? AND owner = ?",
            (post_result["postid"], logname)
        )
        likes_url = f"/api/v1/likes/{curr.fetchone()['likeid']}/"
    else:
        logname_liked = False
        likes_url = None
    likes = {
        "lognameLikesThis": logname_liked,
        "numLikes": like_count,
        "url": likes_url
    }

    # Get single post comments
    comments = []
    curr = connection.execute(
        "SELECT * "
        "FROM comments "
        "WHERE postid = ? "
        "ORDER BY commentid ASC",
        (postid_url_slug,)
    )
    result = curr.fetchall()
    for comment in result:
        logname_owns_this = comment["owner"] == logname
        comments.append({
            "commentid": comment["commentid"],
            "lognameOwnsThis": logname_owns_this,
            "owner": comment["owner"],
            "ownerShowUrl": f"/users/{comment['owner']}/",
            "text": comment["text"],
            "url": f"/api/v1/comments/{comment['commentid']}/"
        })

    # Create and return the post object
    return flask.jsonify({
        "comments": comments,
        "comments_url": f"/api/v1/comments/?postid={postid_url_slug}",
        "created": post_result["created"],
        "imgUrl": f"/uploads/{post_result['filename']}",
        "likes": likes,
        "owner": post_result["owner"],
        "ownerImgUrl": f"/uploads/{owner_img_url}",
        "ownerShowUrl": f"/users/{post_result['owner']}/",
        "postShowUrl": f"/posts/{postid_url_slug}/",
        "postid": postid_url_slug,
        "url": flask.request.path
    }), 200
