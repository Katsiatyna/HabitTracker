"""
Module: test_analytics.py
Author: Katsiaryna Petrushenia
Date: 2023-08-30
Description:
This module contains unit tests for the analytics functions in the HabitTracker application.
The tests verify that the analytics functions correctly retrieve, filter, and calculate
habits and their streaks from the database.

Tested Functions:
    get_all_habits(db): Retrieves all habits from the database.
    get_habits_by_periodicity(db, periodicity): Retrieves habits with a specific periodicity from the database.
    get_longest_streak(db, user_id): Retrieves the longest streak for a user from the database.
    get_longest_streak_for_habit(db, habit_id): Retrieves the longest streak for a specific habit from the database.
"""

import pytest
from datetime import datetime, timedelta
from src.analytics.analytics import (
    get_all_habits,
    get_habits_by_periodicity,
    get_longest_streak,
    get_longest_streak_for_habit, get_habits_to_complete_today
)
from src.database.db_handler import DatabaseHandler

@pytest.fixture
def db():
    """
    Sets up an in-memory DB for testing and adds sample data.

    This fixture provides a fresh DB instance for each test. The DB contains:
        - 1 user (KatsiarynaPetrushenia)
        - 3 habits with different periodicities (1, 5, 7)
        - Completions linked to specific habits

    Yields:
        DatabaseHandler: An instance of the DatabaseHandler class.
    """
    db_handler = DatabaseHandler(":memory:")
    db_handler.add_user("KatsiarynaPetrushenia", "admin@example.com", "2023-08-30T14:23:55")

    # Add habits with periodicities 1, 5, and 7
    db_handler.add_habit(1, "Exercise", "Do 30 minutes of exercise every day", 1, "2023-08-30T14:23:55")
    db_handler.add_habit(1, "Reading", "Read for 30 minutes every week", 7, "2023-08-30T14:23:55")
    db_handler.add_habit(1, "Meditation", "Meditate every 5 days", 5, "2023-08-30T14:23:55")

    # Add completions for habits
    db_handler.add_completion(1, "2023-08-30T15:00:00")
    db_handler.add_completion(1, "2023-08-31T15:00:00")  # Exercise - daily streak of 2
    db_handler.add_completion(3, "2023-09-04T15:00:00")  # Meditation - one completion
    db_handler.add_completion(2, "2023-08-30T15:00:00")  # Reading - one completion

    yield db_handler
    db_handler.close()

def test_get_all_habits(db):
    """
    Test to verify that all habits are retrieved correctly.
    """
    habits = get_all_habits(db, 1)
    assert len(habits) == 3
    habit_names = {habit['name'] for habit in habits}
    assert habit_names == {"Exercise", "Reading", "Meditation"}

def test_get_habits_by_periodicity(db):
    """
    Test to verify that habits are correctly filtered by periodicity.
    """
    daily_habits = get_habits_by_periodicity(db, 1, 1)  # Daily
    weekly_habits = get_habits_by_periodicity(db, 1, 7)  # Weekly
    flexible_habits = get_habits_by_periodicity(db, 1, 5)  # Every 5 days

    assert len(daily_habits) == 1
    assert daily_habits[0]['name'] == "Exercise"
    assert len(weekly_habits) == 1
    assert weekly_habits[0]['name'] == "Reading"
    assert len(flexible_habits) == 1
    assert flexible_habits[0]['name'] == "Meditation"

def test_get_longest_streak(db):
    """
    Test to find the habit with the longest streak among all user habits.
    """
    # Add additional completions to simulate edge cases
    db.add_completion(1, "2023-09-01T15:00:00")  # Exercise - daily streak of 3
    db.add_completion(2, "2023-09-06T15:00:00")  # Reading - 7-day gap continuation
    db.add_completion(3, "2023-09-09T15:00:00")  # Meditation - 5-day gap

    habit, streak = get_longest_streak(db, 1)
    assert habit is not None, "Longest habit not found"
    assert habit['name'] == "Exercise", f"Expected 'Exercise', but got {habit['name']}"
    assert streak == 3, f"Expected 3, but got {streak}"

def test_get_longest_streak_for_habit(db):
    """
    Test to find the longest streak for a specific habit.
    """
    db.add_completion(1, "2023-09-01T15:00:00")  # Exercise - daily streak of 3
    db.add_completion(2, "2023-09-06T15:00:00")  # Reading - 7-day gap continuation
    db.add_completion(3, "2023-09-09T15:00:00")  # Meditation - 5-day gap

    streak_exercise = get_longest_streak_for_habit(db, 1, 1)  # Daily
    streak_reading = get_longest_streak_for_habit(db, 2, 7)   # Weekly
    streak_meditation = get_longest_streak_for_habit(db, 3, 5) # Every 5 days

    assert streak_exercise == 3, f"Expected 3 for Exercise, got {streak_exercise}"
    assert streak_reading == 2, f"Expected 2 for Reading, got {streak_reading}"
    assert streak_meditation == 2, f"Expected 2 for Meditation, got {streak_meditation}"

def test_get_habits_to_complete_today(db):
    """
    Test to verify which habits are due for completion today.
    """
    # Set last completion far in the past for test purposes
    db.add_completion(1, (datetime.now() - timedelta(days=3)).isoformat())
    db.add_completion(2, (datetime.now() - timedelta(days=10)).isoformat())
    db.add_completion(3, (datetime.now() - timedelta(days=6)).isoformat())

    due_habits = get_habits_to_complete_today(db, 1)
    due_names = {h['name'] for h in due_habits}

    assert "Exercise" in due_names
    assert "Reading" in due_names
    assert "Meditation" in due_names