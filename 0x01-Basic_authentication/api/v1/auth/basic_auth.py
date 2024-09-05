#!/usr/bin/env python3
"""api/v1/auth/basic_auth.py"""
import base64
from typing import TypeVar, Tuple
from api.v1.auth.auth import Auth

User = TypeVar('User')


class BasicAuth(Auth):
    """
    BasicAuth class that inherits from Auth.
    """

    def extract_base64_authorization_header(
        self, authorization_header: str
    ) -> str:
        """
        Extract the Base64 part of the Authorization header.
        """
        if (
            authorization_header is None
            or not isinstance(authorization_header, str)
        ):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        # Return the part after "Basic "
        return authorization_header.split(" ", 1)[1]

    def decode_base64_authorization_header(
        self, base64_authorization_header: str) -> str:
        """
        Decode the Base64 string to its original value.
        """
        if base64_authorization_header is None or not isinstance(
            base64_authorization_header, str
        ):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            # Decode as UTF-8 and return the string
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
        self, decoded_base64_authorization_header: str
    ) -> Tuple[str, str]:
        """
        Extract user email and password from the Base64 decoded value.
        """
        if (
            decoded_base64_authorization_header is None
            or not isinstance(decoded_base64_authorization_header, str)
        ):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        # Split the string into email and password
        return tuple(decoded_base64_authorization_header.split(":", 1))

    def user_object_from_credentials(
        self, user_email: str, user_pwd: str
    ) -> User:
        """
        Retrieve the User instance based on email and password.
        """
        if not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return None
        try:
            # Assuming User class has a class method `search` for email lookup
            user = User.search(user_email)
            if not user:
                return None
            # Assuming User class has an `is_valid_password` method
            if not user.is_valid_password(user_pwd):
                return None
            return user
        except Exception:
            return None

    def current_user(self, request=None) -> User:
        """
        Retrieve the User instance for the request.
        """
        auth_header = self.authorization_header(request)
        base64_auth_header = self.extract_base64_authorization_header(
            auth_header)
        decoded_auth_header = self.decode_base64_authorization_header(
            base64_auth_header
        )
        email, password = self.extract_user_credentials(decoded_auth_header)
        return self.user_object_from_credentials(email, password)
