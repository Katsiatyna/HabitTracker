"""
Module: completion.py
Author: Katsiaryna Petrushenia
Date: 2023-08-30
Description: This module provides a completion class to represent a completion of a habit.

Classes:
    Completion: A class for representing a completion of a habit.
"""

from datetime import datetime

class Completion:
    """
    Represents a completion of a habit.

    Attributes:
        habit_id (int): The ID of the habit that was completed.
        completed_date (datetime): The date and time of the completion.
    """

    def __init__(self, habit_id: int, completed_date: datetime):
        """
        Initializes a new instance of the Completion class.

        Args:
            habit_id (int): The ID of the habit that was completed.
            completed_date (datetime): The date and time of the completion.
        """
        self.habit_id = habit_id
        self.completed_date = completed_date or datetime.now()

    def __str__(self) -> str:
        """
        Returns a string representation of the Completion object.
        """
        return f"Completion(habit_id={self.habit_id}, completion_date={self.completed_date})"