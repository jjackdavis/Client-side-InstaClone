"""Explore Page."""
import flask
from flask import url_for, redirect
from insta485.views.follow import follow
from insta485.views.edit import authorize_user
import insta485


@insta485.app.route('/explore/')
def explore():
    """Explore Page."""
    if 'username' not in flask.session:
        return redirect(url_for('show_login'))

    connection, logname = authorize_user()

    curr = connection.execute(
        "SELECT * "
        "FROM users "
        "WHERE username NOT IN ( "
        "SELECT username2 "
        "FROM following "
        "WHERE username1 = ?)",
        (logname,))
    not_following = curr.fetchall()

    context = {
        "logname": logname,
        "URL": url_for('explore'),
        "not_following": []
    }
    for user in not_following:
        context["not_following"].append({
            "username": user["username"],
            "user_img_url": user["filename"]
        })

    return flask.render_template("explore.html", **context, follow=follow)
