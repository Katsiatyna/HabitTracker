"""
Module: analytics.py
Author: Katsiaryna Petrushenia
Date: 2023-08-30
Description: This module provides analytics functions for the HabitTracker application.
This module follows functional programming paradigm:
1. Immutability: Avoid changing state or mutating data.
2. Pure Functions: Functions  return the same output given the same input, without side effects.
3. Higher-Order Functions: Use functions as arguments or return values.
4. Map, Filter, Reduce: Utilize these functions for data transformations and aggregations.
5. Avoid Loops: Prefer using functional constructs like list comprehensions, map, filter, and reduce.

Functions:
    get_all_habits(db): Retrieves all habits from the database.
    get_habits_by_periodicity(db, periodicity): Retrieves habits with a specific periodicity from the database.
    get_longest_streak(db, user_id): Retrieves the longest streak for a user from the database.
    get_longest_streak_for_habit(db, habit_id): Retrieves the longest streak for a specific habit from the database.
"""

from datetime import datetime
from functools import reduce


def get_all_habits(db, user_id):
    """
    Retrieves all habits from the database.
    """
    return db.get_all_habits(user_id)

def get_habits_by_periodicity(db, user_id, periodicity):
    """
    Retrieves habits with a specific periodicity from the database.
    """
    habits = db.get_all_habits(user_id)
    return list(filter(lambda habit: habit['periodicity'] == periodicity, habits))

def get_longest_streak(db, user_id):
    """
    Retrieves the longest streak of all habits for a user.
    """
    habits = db.get_all_habits(user_id)
    if not habits:
        return None, 0

    # Get the streaks for all habits
    streaks = map(lambda habit: (habit, get_longest_streak_for_habit(db, habit['id'], habit['periodicity'])), habits)
    longest = max(streaks, key=lambda x: x[1], default=(None, 0))

    return longest

def get_longest_streak_for_habit(db, habit_id, periodicity):
    """
    Retrieves the longest streak for a specific habit.
    """
    completions = db.get_completions(habit_id)
    if not completions:
        return 0

    try:
        # Convert dates to datetime objects and sort them
        dates = sorted([
            datetime.fromisoformat(c['completed_date'])
            for c in completions if c['completed_date'] is not None
        ])
    except Exception as e:
        print(f"Error parsing dates: {e}")
        return 0

    if len(dates) == 1:
        return 1

    # Calculate streaks using reduce
    def streak_reducer(acc, date_pair):
        prev_date, streak, max_streak = acc
        curr_date = date_pair

        diff = (curr_date - prev_date).days
        if (periodicity == 1 and diff == 1) or (periodicity > 1 and 1 <= diff <= periodicity):
            return (curr_date, streak + 1, max(max_streak, streak + 1))
        return (curr_date, 1, max(max_streak, streak))

    _, final_streak, max_streak = reduce(streak_reducer, dates[1:], (dates[0], 1, 1))
    return max_streak

def get_habits_to_complete_today(db, user_id):
    """
    Returns a list of habits that should be completed today.
    """
    today = datetime.now().date()
    habits = db.get_all_habits(user_id)

    def is_due_today(habit):
        last_completion = db.get_last_completion(habit['id'])
        if not last_completion:
            return True  # Never completed, so it's due today
        last_date = datetime.fromisoformat(last_completion['completed_date']).date()
        return (today - last_date).days >= habit['periodicity']

    return list(filter(is_due_today, habits))

def list_all_habits(db, user_id):
    """
    Returns a list of all tracked habits for a user.
    """
    return db.get_all_habits(user_id)

def list_habits_with_same_periodicity(db, user_id, periodicity):
    """
    Returns a list of all habits with the same periodicity for a user.
    """
    habits = db.get_all_habits(user_id)
    return list(filter(lambda habit: habit['periodicity'] == periodicity, habits))

def get_all_streaks(db, user_id):
    """
    Returns a list of all habits with their longest streaks.
    """
    habits = db.get_all_habits(user_id)
    if not habits:
        return []

    def calculate_streak(habit):
        completions = db.get_completions(habit['id'])
        if not completions:
            return 0

        dates = sorted(
            [datetime.fromisoformat(c['completed_date']) for c in completions]
        )

        max_streak = current_streak = 1
        for i in range(1, len(dates)):
            diff = (dates[i] - dates[i - 1]).days
            if 1 <= diff <= habit['periodicity']:
                current_streak += 1
            else:
                max_streak = max(max_streak, current_streak)
                current_streak = 1
        return max(max_streak, current_streak)

    return [{"name": h["name"], "streak": calculate_streak(h)} for h in habits]
