"""Post Actions."""
import os
import flask
from flask import url_for, request, redirect, abort
from insta485.views.accounts import hash_img
import insta485


@insta485.app.route('/posts/', methods=['POST'])
def post():
    """Post Actions."""
    operation = flask.request.form.get('operation')
    logname = flask.session['username']
    # Connect to database
    connection = insta485.model.get_db()

    # To create a post
    if operation == 'create':

        # Unpack flask object
        fileobj = flask.request.files["file"]
        # Make sure file isn't empty
        if not fileobj:
            abort(400)

        uuid_basename = hash_img(fileobj)

        # Insert post into DB
        connection.execute(
            "INSERT INTO posts "
            "(filename, owner) VALUES "
            "(?, ?)",
            (uuid_basename, logname)
        )

        connection.commit()

    # To remove a post -- remove post, comments, likes
    if operation == 'delete':
        postid = flask.request.form.get('postid')

        curr = connection.execute(
            "SELECT * FROM posts "
            "WHERE postid = ?",
            (postid,)
        )
        result = curr.fetchone()
        owner = result["owner"]
        if owner != logname:
            abort(403)

        uuid_basename = result["filename"]
        file_path = insta485.app.config["UPLOAD_FOLDER"]/uuid_basename
        os.remove(file_path)

        # Remove actual post
        connection.execute(
            "DELETE FROM posts "
            "WHERE postid = ? ",
            (postid,)
        )

        connection.commit()

    target_url = request.args.get('target')
    if target_url:
        return redirect(target_url)
    return redirect(url_for('show_user', username=logname))
