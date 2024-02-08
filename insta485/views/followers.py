"""Followers Page."""
import flask
from flask import url_for, redirect, abort
import insta485


@insta485.app.route('/users/<username>/followers/')
def show_followers(username):
    """Followers Page."""
    if 'username' not in flask.session:
        return redirect(url_for('show_login'))
    connection = validate(username)
    logname = flask.session['username']

    curr = connection.execute(
        "SELECT * "
        "FROM following "
        f"WHERE username2 = '{username}'"
    )
    followers = curr.fetchall()

    follower_img_user = {}
    follower_log_follows = {}

    for follower in followers:
        curr = connection.execute(
            "SELECT COUNT(*) AS log_follows_follower "
            "FROM following "
            "WHERE username1 = ? AND username2 = ?",
            (logname, follower["username1"])
        )
        if curr.fetchone()["log_follows_follower"] == 0:
            follower_log_follows[follower["username1"]] = False
        else:
            follower_log_follows[follower["username1"]] = True

        curr = connection.execute(
            "SELECT filename "
            "FROM users "
            "WHERE username = ?",
            (follower["username1"],)
        )

        follower_img_user[follower["username1"]] = curr.fetchone()["filename"]

    context = {
        "logname": logname,
        "username": username,
        "followers": []
    }

    for follower in followers:
        context["followers"].append({
            "username": follower["username1"],
            "logname_follows_username": (
                follower_log_follows[follower["username1"]]
            ),
            "user_img_url": follower_img_user[follower["username1"]]
        })

    return flask.render_template("followers.html", **context)


def validate(username):
    """Validate."""
    connection = insta485.model.get_db()

    curr = connection.execute(
        "SELECT * "
        "FROM users "
        "WHERE username = ?",
        (username,)
    )
    result = curr.fetchone()
    if result is None:
        abort(404)
    return connection
