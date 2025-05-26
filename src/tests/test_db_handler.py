"""
Module: test_db_handler.py
Author: Katsiaryna Petrushenia
Date: 2023-08-30
Description:
This module contains unit tests for the DatabaseHandler class in the Habit Tracker application.
It verifies correct behavior of user, habit, and completion operations using an in-memory SQLite database.

Tested Features:
    - User creation, retrieval, and updating
    - Habit creation, retrieval, updating, and deletion
    - Completion creation, updating, retrieval, and deletion
"""

import pytest
from datetime import datetime
from src.database.db_handler import DatabaseHandler

@pytest.fixture
def db():
    """
    Sets up an in-memory database for testing and ensures it is cleaned up after the test.
    Yields:
        DatabaseHandler: An instance of the database handler connected to :memory:
    """
    db = DatabaseHandler(":memory:")
    yield db
    db.close()

def test_add_and_get_user(db):
    """
    Tests adding a new user and retrieving it by username and ID.
    """
    creation_date = datetime.now().isoformat()
    user_id = db.add_user("testuser", "test@example.com", creation_date)

    # Fetch all users and verify one exists
    users = db.get_all_users()
    assert len(users) == 1
    assert users[0]["username"] == "testuser"

    # Fetch user ID by username
    fetched_id = db.get_user_id("testuser")
    assert fetched_id == user_id

def test_update_user(db):
    """
    Tests updating a user's username and email.
    """
    user_id = db.add_user("olduser", "old@example.com")
    db.update_user(user_id, "newuser", "new@example.com")
    users = db.get_all_users()
    assert users[0]["username"] == "newuser"
    assert users[0]["email"] == "new@example.com"

def test_add_and_get_habit(db):
    """
    Tests adding and retrieving a habit for a user.
    """
    user_id = db.add_user("habituser", "habit@example.com")
    db.add_habit(user_id, "Exercise", "Daily workout", 1)
    habits = db.get_all_habits(user_id)

    assert len(habits) == 1
    assert habits[0]["name"] == "Exercise"
    assert habits[0]["periodicity"] == 1

def test_update_habit(db):
    """
    Tests updating a habit's name, description, and periodicity.
    """
    user_id = db.add_user("habitupd", "edit@example.com")
    db.add_habit(user_id, "OldHabit", "Old Desc", 3)
    db.update_habit(user_id, "OldHabit", "NewHabit", "New Desc", 7)

    habits = db.get_all_habits(user_id)
    assert habits[0]["name"] == "NewHabit"
    assert habits[0]["description"] == "New Desc"
    assert habits[0]["periodicity"] == 7

def test_delete_habit(db):
    """
    Tests deleting a habit by name for a user.
    """
    user_id = db.add_user("delhabit", "delete@example.com")
    db.add_habit(user_id, "ToDelete", "Desc", 2)
    db.delete_habit(user_id, "ToDelete")

    habits = db.get_all_habits(user_id)
    assert len(habits) == 0

def test_add_and_get_completion(db):
    """
    Tests adding a completion and verifying it is retrievable.
    """
    user_id = db.add_user("compuser", "comp@example.com")
    db.add_habit(user_id, "Exercise", "Daily", 1)
    habit = db.get_habit_by_name(user_id, "Exercise")

    db.add_completion(habit["id"], "2023-08-30T10:00:00")
    completions = db.get_completions(habit["id"])
    assert len(completions) == 1
    assert completions[0]["completed_date"] == "2023-08-30T10:00:00"

def test_update_completion_date(db):
    """
    Tests updating the date of a completion entry.
    """
    user_id = db.add_user("updatecomp", "u@example.com")
    db.add_habit(user_id, "TestHabit", "Daily", 1)
    habit = db.get_habit_by_name(user_id, "TestHabit")

    db.add_completion(habit["id"], "2023-08-30T08:00:00")
    completion = db.get_completions(habit["id"])[0]

    db.update_completion_date(completion["id"], "2023-09-01T08:00:00")
    updated = db.get_completions(habit["id"])[0]
    assert updated["completed_date"] == "2023-09-01T08:00:00"

def test_delete_completion(db):
    """
    Tests deleting a specific completion date (by date only, not time).
    """
    user_id = db.add_user("delcomp", "dc@example.com")
    db.add_habit(user_id, "Stretching", "Morning", 1)
    habit = db.get_habit_by_name(user_id, "Stretching")

    db.add_completion(habit["id"], "2023-08-30T07:00:00")
    db.delete_completion(habit["id"], "2023-08-30T09:00:00")  # Same date, different time
    completions = db.get_completions(habit["id"])
    assert len(completions) == 0

def test_get_last_completion(db):
    """
    Tests retrieving the most recent completion of a habit.
    """
    user_id = db.add_user("lastcomp", "last@example.com")
    db.add_habit(user_id, "Jogging", "Evening", 1)
    habit = db.get_habit_by_name(user_id, "Jogging")

    db.add_completion(habit["id"], "2023-08-29T10:00:00")
    db.add_completion(habit["id"], "2023-08-31T10:00:00")
    last = db.get_last_completion(habit["id"])

    assert last["completed_date"] == "2023-08-31T10:00:00"
