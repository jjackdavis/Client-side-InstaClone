"""
Insta485 index (main) view.

URLs include:
/
"""
import flask
from flask import url_for, redirect, send_from_directory, abort
import arrow
import insta485


@insta485.app.route('/')
def show_index():
    """Display / route."""
    if 'username' not in flask.session:
        return redirect(url_for('show_login'))
    logname = flask.session['username']

    # Connect to database
    connection = insta485.model.get_db()

    # Query database for posts
    cur = connection.execute(
        "SELECT p.* "
        "FROM posts as p "
        f"WHERE p.owner = '{logname}'"
        "UNION "
        "SELECT po.* "
        "FROM following AS f "
        "JOIN posts AS po ON f.username2 = po.owner "
        f"WHERE f.username1 = '{logname}' "
        "ORDER BY p.postid DESC "
    )
    posts = cur.fetchall()

    post_profile_pics = {}
    post_likes = {}
    post_comments = {}
    post_liked = {}
    for post in posts:
        # Query database for profile pictures
        cur_profile_pic = connection.execute(
            "SELECT filename "
            "FROM users "
            "WHERE username = ?",
            (post["owner"],)
        )
        # Query database for comments
        cur_comments = connection.execute(
            "SELECT c.owner, c.text "
            "FROM comments AS c "
            "WHERE c.postid = ? "
            "ORDER BY c.commentid ASC",
            (post["postid"],)
        )
        # Query database for likes
        cur_likes = connection.execute(
            "SELECT COUNT(*) AS like_count "
            "FROM likes "
            "WHERE postid = ?",
            (post["postid"],)
        )
        # Query database to see if post is liked
        cur_liked = connection.execute(
            "SELECT COUNT(*) AS like_count "
            "FROM likes "
            "WHERE owner = ? AND postid = ?",
            (logname, post["postid"])
        )
        # Comments
        post_comments[post["postid"]] = \
            [dict(row) for row in cur_comments.fetchall()]
        # Likes
        post_likes[post["postid"]] = \
            cur_likes.fetchone()["like_count"]
        # Liked (will either be 1 or 0)
        post_liked[post["postid"]] = \
            cur_liked.fetchone()["like_count"]
        # Profile Pics
        post_profile_pics[post["owner"]] = \
            cur_profile_pic.fetchone()["filename"]

    context = {
        "logname": logname,
        "posts": []
    }
    for post in posts:
        created_timestamp = arrow.get(post["created"])
        post["timestamp"] = created_timestamp.humanize()
        context["posts"].append({
            "postid": post["postid"],
            "owner": post["owner"],
            "img_url": post["filename"],
            "timestamp": post["timestamp"],
            "comments": post_comments[post["postid"]],
            "owner_img_url": post_profile_pics[post["owner"]],
            "likes": post_likes[post["postid"]],
            "liked": post_liked[post["postid"]]
        })

    return flask.render_template("index.html", **context)


@insta485.app.route('/uploads/<img_url>')
def get_image(img_url):
    """Serve images."""
    if 'username' not in flask.session:
        abort(403)

    return send_from_directory(insta485.app.config["UPLOAD_FOLDER"], img_url)
