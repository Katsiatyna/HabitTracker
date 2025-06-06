"""
Test: test_user.py
Author: Katsiaryna Petrushenia

Description: This module contains unit tests for the User class, testing initialization and completion methods.
"""

import pytest
from datetime import datetime
from src.models.user import User

def test_user_initialiation():
    """
    Test the initialization of the User class
    """
    user = User("KatsiarynaPetrushenia", "admin@example.com", datetime.now())
    assert user.username == "KatsiarynaPetrushenia"
    assert user.email == "admin@example.com"
    assert isinstance(user.creation_date, datetime)

def test_user_string_representation():
    """
    Test the string representation of the User class
    """
    user = User("KatsiarynaPetrushenia", "admin@example.com", datetime.now())
    assert str(user).startswith("User(username=KatsiarynaPetrushenia, email=admin@example.com, creation_date=")

