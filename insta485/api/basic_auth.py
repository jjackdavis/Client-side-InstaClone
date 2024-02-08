"""Doc string."""
import hashlib
import flask
import insta485


def basic_auth():
    """Get basic authorization."""
    if flask.request.authorization:
        username2 = flask.request.authorization['username']
        password2 = flask.request.authorization['password']

        connection = insta485.model.get_db()

        curr = connection.execute(
            "SELECT * FROM users "
            "WHERE username = ?",
            (username2,)
        )

        result1 = curr.fetchone()
        if result1 is None:
            return flask.jsonify({"message": "Forbidden",
                                  "status_code": 403}), False
        result1 = result1["password"]

        # Split the password_db_string using "$" as the delimiter
        parts = result1.split("$")

        # Extract the salt and hash
        salt = parts[1]

        # Create hashed password
        algorithm = 'sha512'
        hash_obj = hashlib.new(algorithm)
        password_salted = salt + password2
        hash_obj.update(password_salted.encode('utf-8'))
        password_hash = hash_obj.hexdigest()
        password_db_string = "$".join([algorithm, salt, password_hash])

        if password_db_string != result1:
            return flask.jsonify({"message": "Forbidden",
                                  "status_code": 403}), False
        return username2, True
    if 'username' not in flask.session:
        return flask.jsonify({"message": "Forbidden",
                              "status_code": 403}), False
    return flask.session['username'], True
