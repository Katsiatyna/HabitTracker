"""
Module: user.py
Author: Katsiaryna Petrushenia
Date: 2023-08-30
Description: This module provides a user class to represent a user.

Classes:
    User: A class for representing a user.
"""

from datetime import datetime

class User:
    """
    Represents a user in the habit tracking application.

    Attributes:
        username (str): The name of the user.
        email (str): The email address of the user.
        creation_date (datetime): The date when the user was created.
    """

    def __init__(self, username, email, creation_date):
        """
        Initializes a new instance of the User class.

        Args:
            username (str): The name of the user.
            email (str): The email address of the user.
            creation_date (datetime): The date when the user was created.
        """
        self.username = username
        self.email = email
        self.creation_date = datetime.now()

    def __str__(self) -> str:
        """
        Returns a string representation of the User object.
        """
        return f"User(username={self.username}, email={self.email}, creation_date={self.creation_date})"
