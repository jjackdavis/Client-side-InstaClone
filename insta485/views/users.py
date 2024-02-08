"""Profile Page."""
import flask
from flask import url_for, redirect, abort
from insta485.views.post import post
import insta485


@insta485.app.route('/users/<username>/')
def show_user(username):
    """Profile Page."""
    if 'username' not in flask.session:
        return redirect(url_for('show_login'))
    logname = flask.session['username']
    connection = insta485.model.get_db()

    curr = connection.execute(
        "SELECT fullname "
        "FROM users "
        "WHERE username = ? ",
        (username,)
    )
    result = curr.fetchone()
    if result is None:
        abort(404)
    fullname = result["fullname"]

    curr = connection.execute(
        "SELECT p.* "
        "FROM posts as p "
        f"WHERE p.owner = '{username}'"
        "ORDER BY p.created DESC "
    )

    posts = curr.fetchall()

    curr = connection.execute(
        "SELECT COUNT(*) as post_count "
        "FROM posts "
        "WHERE owner = ?",
        (username,)
    )
    totalposts = curr.fetchone()["post_count"]

    curr = connection.execute(
        "SELECT COUNT(*) as following_count "
        "FROM following "
        "WHERE username1 = ?",
        (username,)
    )
    following_count = curr.fetchone()["following_count"]

    curr = connection.execute(
        "SELECT COUNT(*) as follower_count "
        "FROM following "
        "WHERE username2 = ?",
        (username,)
    )
    follower_count = curr.fetchone()["follower_count"]

    curr = connection.execute(
        "SELECT COUNT(*) as follower_count "
        "FROM following "
        "WHERE username2 = ?",
        (username,)
    )
    follower_count = curr.fetchone()["follower_count"]

    curr = connection.execute(
        "SELECT COUNT(*) as log_follows_user "
        "FROM following "
        "WHERE username1 = ? AND username2 = ?",
        (logname, username)
    )

    if curr.fetchone()["log_follows_user"] == 0:
        log_follows_user = False
    else:
        log_follows_user = True

    context = {
        "logname": logname,
        "username": username,
        "fullname": fullname,
        "total_posts": totalposts,
        "following": following_count,
        "followers": follower_count,
        "logname_follows_username": log_follows_user,
        "URL": f"/users/{username}/",
        "posts": []
    }
    for each_post in posts:
        context["posts"].append({
            "postid": each_post["postid"],
            "img_url": each_post["filename"],
        })

    return flask.render_template("user.html", **context, post=post)
