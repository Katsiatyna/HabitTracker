"""
Test: test_habit.py
Author: Katsiaryna Petrushenia

Description: This module contains unit tests for the Habit class, testing initialization and completion methods.
"""

import pytest
from datetime import datetime, timedelta
from src.models.habit import Habit

def test_habit_initialiation():
    """
    Test the initialization of the Habit class
    """
    creation_date = datetime(2023, 8, 30) # Example fixed date for consistency

    # Check attribute values
    habit = Habit("Exercise", "Daily workout", 1, creation_date)
    assert habit.name == "Exercise"
    assert habit.description == "Daily workout"
    assert habit.periodicity == 1
    assert habit.creation_date == creation_date
    assert habit.completions == []

def test_add_completion():
    """
    Test if the add_completion method adds a completion to the completions list.
    """
    creation_date = datetime(2023, 8, 30) # Example fixed date for consistency
    habit = Habit("Exercise", "Daily workout", 1, creation_date)
    habit.add_completion()

    # Check if the completion was added
    assert len(habit.completions) == 1
    # Verify the completion date is a datetime object
    assert isinstance(habit.completions[0], datetime)

def test_calculate_streak_daily():
    """
    Test if the calculate_streak method returns the correct number of consecutive completions.
    """
    creation_date = datetime(2023, 8, 30) # Example fixed date for consistency
    habit = Habit("Exercise", "Daily workout", 1, creation_date)

    # Add completions on consecutive days to maintain streak
    habit.completions = [
        creation_date,
        creation_date + timedelta(days=1),
        creation_date + timedelta(days=2)
    ]

    #Check if the streak calculation is correct
    assert habit.calculate_streak() == 3

def test_calculate_streak_broken():
    """
    Test if the streak resets when the habit is not completed within the periodicity.
    """
    creation_date = datetime(2023, 8, 30) # Example fixed date for consistency
    habit = Habit("Meditation", "Morning routine", 1, creation_date)

    # Add completions on consecutive days to maintain streak
    habit.completions = [
        creation_date,
        creation_date + timedelta(days=1),
        creation_date + timedelta(days=2),
        creation_date + timedelta(days=4) # Gap of 2 days
    ]

    #Check if the streak calculation is correct
    assert habit.calculate_streak() == 1

def test_calculate_streak_flexible():
    """
    Test if the calculate_streak method returns the correct number of consecutive completions.
    """
    creation_date = datetime(2023, 8, 30) # Example fixed date for consistency
    habit = Habit("Running", "Run every 3 days", 3, creation_date)

    # Add completions on consecutive days to maintain streak
    habit.completions = [
        creation_date,
        creation_date + timedelta(days=3),
        creation_date + timedelta(days=6),
    ]

    #Check if the streak calculation is correct
    assert habit.calculate_streak() == 3
