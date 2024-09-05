#!/usr/bin/env python3
""" Authentication module
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Auth class for managing API authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Determines if authentication is required for a given path"""
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True

        # Ensure path ends with a slash
        if path[-1] != '/':
            path += '/'

        # Return False if the path is in excluded_paths
        for excluded_path in excluded_paths:
            if excluded_path[-1] != '/':
                excluded_path += '/'
            if path == excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """Returns the Authorization header from a Flask request object"""

        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns the current user (to be implemented later)"""
        return None
