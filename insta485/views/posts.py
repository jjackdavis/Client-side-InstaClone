"""Show post actions."""
import flask
from flask import url_for, redirect
import arrow
from insta485.views.index import show_index
import insta485


@insta485.app.route('/posts/<postid>/')
def posts(postid):
    """Show a post."""
    if 'username' not in flask.session:
        return redirect(url_for('show_login'))
    logname = flask.session['username']
    # Database connection
    con = insta485.model.get_db()

    curr = con.execute(
        "SELECT * "
        "FROM posts "
        "WHERE postid = ?",
        (postid,)
    )

    post = curr.fetchone()
    filename = post["filename"]
    owner = post["owner"]

    curr = con.execute(
        "SELECT * "
        "FROM users "
        "WHERE username = ?",
        (owner,)
    )
    user = curr.fetchone()
    owner_img_url = user["filename"]

    # Retrieve likes
    curr = con.execute(
        "SELECT COUNT(*) AS like_count "
        "FROM likes "
        "WHERE postid = ?",
        (postid,)
    )

    likes = curr.fetchone()["like_count"]

    curr = con.execute(
        "SELECT * "
        "FROM comments "
        "WHERE postid = ? "
        "ORDER BY commentid ASC",
        (postid,)
    )

    comments = curr.fetchall()

    # Query db to see if post liked or not
    liked = con.execute(
        "SELECT COUNT(*) AS l_count "
        "FROM likes "
        "WHERE postid = ? AND owner = ?",
        (post["postid"], logname)
    )

    # Liked (will either be 1 or 0)
    liked = liked.fetchone()["l_count"]

    context = {
        "logname": logname,
        "img_url": filename,
        "timestamp": arrow.get(post["created"]).humanize(),
        "owner": owner,
        "likes": likes,
        "owner_img_url": owner_img_url,
        "postid": postid,
        "comments": comments,
        "liked": liked
    }

    return flask.render_template("post.html", **context, show_index=show_index)
