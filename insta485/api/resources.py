"""REST API for API resource URLs."""

import flask
import insta485


@insta485.app.route('/api/v1/')
def get_resources():
    """Return API resource URLS."""
    context = {
        "comments": "/api/v1/comments/",
        "likes": "/api/v1/likes/",
        "posts": "/api/v1/posts/",
        "url": flask.request.path,
    }
    return flask.jsonify(**context), 200
