"""
Test: test_completion.py
Author: Katsiaryna Petrushenia

Description: This module contains unit tests for the Completion class, testing initialization and completion methods.
"""

import pytest
from datetime import datetime
from src.models.completion import Completion

def test_completion_initialiation():
    """
    Test the initialization of the Completion class
    """
    completion = Completion(1, datetime.now())
    assert completion.habit_id == 1
    assert isinstance(completion.completed_date, datetime)

def test_completion_with_custom_date():
    """
    Test the initialization of the Completion class with a custom date
    """
    custom_date = datetime(2023, 8, 30)
    completion = Completion(2, custom_date)
    assert completion.habit_id == 2
    assert completion.completed_date == custom_date

def test_completion_string_representation():
    """
    Test the string representation of the Completion class
    """
    completion = Completion(3, datetime.now())
    assert str(completion).startswith("Completion(habit_id=3, completion_date=")