"""
Module: habit.py
Author: Katsiaryna Petrushenia
Date: 2023-08-30
Description: This module defines the Habit class,
which represents a trackable habit with flexible periodicity and methods to record completions and alculate streaks.

Classes:
    Habit: Represents a trackable habit with periodicity and methods to record completions and calculate streaks.
"""

from datetime import datetime

class Habit:
    """
    Represents a habit that the user wants to track

    Attributes:
        name (str): The name of the habit.
        description (str): A description of the habit.
        periodicity (int): The periodicity of the habit in days (e.g., 1 for 'daily', 7 for 'weekly', 5, 21 etc.).
        creation_date (datetime): The date when the habit was created.
        completions (list): A list of datetime objects representing the completion dates of the habit.
    """

    def __init__(self, name, description, periodicity, creation_date):
        """
        Initializes a new instance of the Habit class.

        Args:
            name (str): The name of the habit.
            description (str): A description of the habit.
            periodicity (int): The periodicity of the habit in days (e.g., 1 for 'daily', 7 for 'weekly', 5, 21 etc.).

        Example:
            >>> habit = Habit("Exercise", "Daily workout", 1, datetime.now())
        """
        self.name = name
        self.description = description
        self.periodicity = periodicity
        self.creation_date = creation_date
        self.completions = []

    def add_completion(self) -> None:
        """
        Records a completion for the habit.

        Appends the current timestamp to the completions list.
        """
        self.completions.append(datetime.now())

    def calculate_streak(self) -> int:
        """
        Calculates the current streak for the habit.

        Returns:
            int: The number of consecutive periods the habit was completed without a break.
        """
        if not self.completions:
            return 0

        # Sort completions in ascending order
        self.completions.sort()

        streak = 1
        for i in range(1, len(self.completions)):
            # Calculate the difference between consecutive completions
            diff = (self.completions[i] - self.completions[i-1]).days

            #  Check if the difference matches the periodicity
            if diff <= self.periodicity:
                streak += 1
            else:
                streak = 1

        return streak


    def __str__(self) -> str:
        """
        Returns a string representation of the Habit object.

        Returns:
            str: A string containing the name, description, periodicity, and creation date of the habit.
        """
        return f"Habit(name={self.name}, periodicity={self.periodicity} days)"
