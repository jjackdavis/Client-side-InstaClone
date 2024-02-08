"""Doc string."""
import pathlib
import hashlib
import os
import uuid
import flask
from flask import url_for, request, redirect, abort
import insta485


@insta485.app.route('/accounts/', methods=['POST'])
def account_crud():
    """Account crud."""
    operation = flask.request.form.get('operation')

    connection = insta485.model.get_db()

    if operation == 'login':
        login(connection)

    elif operation == 'create':
        create(connection)

    elif operation == 'delete':
        delete(connection)

    elif operation == 'edit_account':
        edit_account(connection)

    elif operation == 'update_password':
        update_password(connection)

    connection.commit()

    target_url = request.args.get('target')
    if target_url:
        return redirect(target_url)
    return redirect(url_for('show_index'))


def login(connection):
    """Connect."""
    username = flask.request.form.get('username')
    password = flask.request.form.get('password')

    if len(username) == 0 or len(password) == 0:
        abort(400)

    curr = connection.execute(
        "SELECT * FROM users "
        "WHERE username = ?",
        (username,)
    )

    result = curr.fetchone()
    if result is None:
        abort(403)
    result = result["password"]

    # Split the password_db_string using "$" as the delimiter
    parts = result.split("$")

    # Extract the salt and hash
    salt = parts[1]

    # Create hashed password
    algorithm = 'sha512'
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join([algorithm, salt, password_hash])

    if password_db_string != result:
        abort(403)

    flask.session['username'] = username


def create(connection):
    """Create."""
    username = flask.request.form.get('username')
    password = flask.request.form.get('password')

    # If user already exists in database
    curr = connection.execute(
        "SELECT * FROM users "
        "WHERE username = ?",
        (username,)
    )

    result = curr.fetchone()
    if result:
        abort(409)

    fullname = flask.request.form.get("fullname")
    email = flask.request.form.get("email")
    fileobj = flask.request.files["file"]
    if (not fileobj or len(fullname) == 0 or len(email) == 0
            or len(username) == 0 or len(password) == 0):
        abort(400)

    uuid_basename = hash_img(fileobj)

    password_db_string = make_password(password)
    connection.execute(
        "INSERT INTO users "
        "(username, fullname, email, filename, password) "
        "VALUES (?, ?, ?, ?, ?)",
        (username, fullname, email, uuid_basename, password_db_string)
    )
    connection.commit()

    flask.session['username'] = username


def hash_img(fileobj):
    """Hash."""
    filename = fileobj.filename

    stem = uuid.uuid4().hex
    suffix = pathlib.Path(filename).suffix.lower()
    uuid_basename = f"{stem}{suffix}"

    # Save to disk
    path = insta485.app.config["UPLOAD_FOLDER"]/uuid_basename
    fileobj.save(path)

    return uuid_basename


def delete(connection):
    """To delete."""
    if 'username' not in flask.session:
        abort(403)

    logname = flask.session['username']
    flask.session.clear()

    # Delete images uploaded by user
    curr = connection.execute(
        "SELECT * FROM posts "
        "WHERE owner = ? ",
        (logname,)
    )

    images = curr.fetchall()
    for image in images:
        path = insta485.app.config["UPLOAD_FOLDER"]/image["filename"]
        os.remove(path)

    curr = connection.execute(
        "SELECT * FROM users "
        "WHERE username = ?",
        (logname,)
    )
    uuid_basename = curr.fetchone()["filename"]

    file_path = insta485.app.config["UPLOAD_FOLDER"]/uuid_basename
    os.remove(file_path)

    connection.execute(
        "DELETE FROM users "
        "WHERE username = ? ",
        (logname,)
    )


def edit_account(connection):
    """Edit account."""
    if 'username' not in flask.session:
        abort(403)

    logname = flask.session['username']

    fullname = flask.request.form.get('fullname')
    email = flask.request.form.get('email')
    fileobj = flask.request.files["file"]

    if len(fullname) == 0 or len(email) == 0:
        abort(400)

    if not fileobj:
        connection.execute(
            "UPDATE users "
            "SET fullname = ? , email = ? "
            "WHERE username = ? ",
            (fullname, email, logname)
        )
    else:
        # Delete user avatar
        curr = connection.execute(
            "SELECT * FROM users "
            "WHERE username = ?",
            (logname,)
        )
        uuid_basename = curr.fetchone()["filename"]

        file_path = insta485.app.config["UPLOAD_FOLDER"]/uuid_basename
        os.remove(file_path)

        filename = fileobj.filename

        stem = uuid.uuid4().hex
        suffix = pathlib.Path(filename).suffix.lower()
        uuid_basename = f"{stem}{suffix}"

        # Save to disk
        path = insta485.app.config["UPLOAD_FOLDER"]/uuid_basename
        fileobj.save(path)

        # Update
        connection.execute(
            "UPDATE users "
            "SET fullname = ? , email = ?, filename = ? "
            "WHERE username = ? ",
            (fullname, email, uuid_basename, logname)
        )


def update_password(connection):
    """Update."""
    if 'username' not in flask.session:
        abort(403)
    logname = flask.session["username"]

    password = flask.request.form.get("password")
    new_password1 = flask.request.form.get("new_password1")
    new_password2 = flask.request.form.get("new_password2")

    if (len(password) == 0 or len(new_password1) == 0
            or len(new_password2) == 0):
        abort(400)

    curr = connection.execute(
        "SELECT * FROM users "
        "WHERE username = ?",
        (logname,)
    )

    result = curr.fetchone()["password"]

    # Split the password_db_string using "$" as the delimiter
    parts = result.split("$")

    # Extract the salt and hash
    salt = parts[1]

    # Create hashed password
    algorithm = 'sha512'
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join([algorithm, salt, password_hash])

    if password_db_string != result:
        abort(403)

    if new_password1 != new_password2:
        abort(401)

    # Create hashed password
    algorithm = 'sha512'
    salt = uuid.uuid4().hex
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + new_password1
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join([algorithm, salt, password_hash])

    connection.execute(
        "UPDATE users "
        "SET password = ? "
        "WHERE password = ?",
        (password_db_string, result)
    )


def make_password(password):
    """Make password."""
    algorithm = 'sha512'
    salt = uuid.uuid4().hex
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join([algorithm, salt, password_hash])
    return password_db_string
