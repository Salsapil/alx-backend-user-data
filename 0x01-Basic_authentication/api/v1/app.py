#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None

# Load the appropriate authentication type based on the environment variable
auth_type = os.getenv('AUTH_TYPE')
if auth_type == "basic_auth":
    auth = BasicAuth()
else:
    auth = Auth()


@app.route('/api/v1/status/', methods=['GET'])
def status():
    """simple status"""
    return jsonify({"status": "OK"}), 200


@app.before_request
def before_request_func():
    """Filters requests before they reach the route"""
    # If no auth class is defined, do nothing
    if auth is None:
        return

    # List of paths that don't require authentication
    excluded_paths = [
        '/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/'
        ]

    # Check if the request path requires authentication
    if not auth.require_auth(request.path, excluded_paths):
        return

    # Check if the Authorization header is present
    if auth.authorization_header(request) is None:
        abort(401)  # Unauthorized error

    # Check if the current user is valid
    if auth.current_user(request) is None:
        abort(403)  # Forbidden error


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized_error(error) -> str:
    """ Error handler for 401 status code """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden_error(error) -> str:
    """ Error handler for 403 status code """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
