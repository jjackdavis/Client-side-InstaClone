"""Show Follow Page."""
import flask
from flask import redirect, url_for
from insta485.views.follow import follow
from insta485.views.followers import validate
import insta485


@insta485.app.route('/users/<username>/following/')
def show_following(username):
    """Show Follow Page."""
    if 'username' not in flask.session:
        return redirect(url_for('show_login'))
    connection = validate(username)
    logname = flask.session['username']

    cur = connection.execute(
        "SELECT * "
        "FROM following "
        "WHERE username1 = ? ",
        (username,)
    )

    following = cur.fetchall()

    following_img_user = {}
    following_log_follows = {}

    for person in following:
        cur = connection.execute(
            "SELECT COUNT(*) AS log_follows_follower "
            "FROM following "
            "WHERE username1 = ? "
            "AND username2 = ?",
            (logname, person["username2"])
        )
        if cur.fetchone()["log_follows_follower"] == 0:
            following_log_follows[person["username2"]] = False
        else:
            following_log_follows[person["username2"]] = True

        cur = connection.execute(
            "SELECT filename "
            "FROM users "
            "WHERE username = ?",
            (person["username2"],)
        )

        following_img_user[person["username2"]] = cur.fetchone()["filename"]

    context = {
        "logname": logname,
        "username": username,
        "following": []
    }

    for person in following:
        context["following"].append({
            "username": person["username2"],
            "logname_follows_username": (
                following_log_follows[person["username2"]]
            ),
            "user_img_url": following_img_user[person["username2"]]
        })

    return flask.render_template("following.html", **context, follow=follow)
