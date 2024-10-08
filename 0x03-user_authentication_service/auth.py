#!/usr/bin/env python3
"""Hash password"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from bcrypt import checkpw
import uuid


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def get_reset_password_token(self, email: str) -> str:
        """
        Generate a reset password token for the user.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError(f"User with email {email} does not exist")

        reset_token = _generate_uuid()

        self._db.update_user(user.id, reset_token=reset_token)

        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Update the password for the user identified by the reset_token.
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError("Invalid reset token")

        hashed_password = _hash_password(password)

        self._db.update_user(user.id, hashed_password=hashed_password,
                             reset_token=None)

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user with the given email and password.
        Raises ValueError if the user already exists.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Check if the provided email and password are valid.
        Returns True if valid, False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
            return checkpw(password.encode('utf-8'), user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """
        Create a new session for the user with the provided email.
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        Find the user corresponding to the given session ID.
        Returns the User object or None if no user is found.
        """
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """
        Destroy the session for the user with the given user_id.
        Sets the user's session_id to None.
        """
        self._db.update_user(user_id, session_id=None)


def _generate_uuid() -> str:
    """
    Generate a new UUID and return its string representation.
    """
    return str(uuid.uuid4())


def _hash_password(password: str) -> bytes:
    """
    Hash the input password using bcrypt, returning the salted hash as bytes.
    """
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    return hashed_password
