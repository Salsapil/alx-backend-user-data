#!/usr/bin/env python3
"""Hash password"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """
    Hash the input password using bcrypt, returning the salted hash as bytes.
    """
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    return hashed_password
