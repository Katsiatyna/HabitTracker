"""
Module: db_handler.py
Author: Katsiaryna Petrushenia
Date: 2023-08-30
Description: SQLite backend for managing habit, completion, and user data.

Classes:
    DatabaseHandler: Manages CRUD operations for users, habits, and completions.
"""
import os
import sqlite3
from datetime import datetime
from contextlib import closing

class DatabaseHandler:
    """
    Manages the SQLite database for storing users, habits, and completions.
    """

    def __init__(self, db_name='habit_tracker.db'):
        """
        Initializes a new instance of the DatabaseHandler class.
        Ensures the database is always created in the project root directory.
        """
        try:
            # Set the database path relative to the current working directory
            self.db_name = db_name
            self.connection = sqlite3.connect(self.db_name, timeout=10)
            self.create_tables()
            print(f"Database connected at: {self.db_name}")
        except sqlite3.OperationalError as e:
            print(f"Error: Could not connect to the database. {e}")
            exit(1)


    def create_tables(self):
        """
        Creates the tables in the database if they do not exist.
        """
        with closing(self.connection.cursor()) as cursor:
            # Users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    email TEXT NOT NULL,
                    creation_date TEXT NOT NULL
                );
            """)

            # Habits table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS habits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    name TEXT NOT NULL,
                    description TEXT,
                    periodicity INTEGER NOT NULL,
                    creation_date TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
                );
            """)

            # Completions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS completions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    habit_id INTEGER,
                    completed_date TEXT NOT NULL,
                    FOREIGN KEY (habit_id) REFERENCES habits (id) ON DELETE CASCADE
                );
            """)
            self.connection.commit()

    def add_user(self, username, email, creation_date=None):
        """
        Adds a new user to the database and returns the newly created user ID.
        """
        creation_date = creation_date or datetime.now().isoformat()
        with closing(self.connection.cursor()) as cursor:
            cursor.execute("""
                INSERT INTO users (username, email, creation_date)
                VALUES (?, ?, ?);
            """, (username, email, creation_date))
            self.connection.commit()
            return cursor.lastrowid  # Return the ID of the newly inserted user

    def update_user(self, user_id, new_username, new_email):
        """
        Updates the username and email of a user by their ID.
        """
        with closing(self.connection.cursor()) as cursor:
            cursor.execute("""
                UPDATE users
                SET username = ?, email = ?
                WHERE id = ?;
            """, (new_username, new_email, user_id))
            self.connection.commit()


    def add_habit(self, user_id, name, description, periodicity, creation_date=None):
        """
        Adds a new habit to the database.
        """
        creation_date = creation_date or datetime.now().isoformat()
        with closing(self.connection.cursor()) as cursor:
            cursor.execute("""
                INSERT INTO habits (user_id, name, description, periodicity, creation_date)
                VALUES (?, ?, ?, ?, ?);
            """, (user_id, name, description, periodicity, creation_date))
            self.connection.commit()

    def add_completion(self, habit_id, completed_date=None):
        """
        Adds a new completion to the database.
        """
        completed_date = completed_date or datetime.now().isoformat()
        with closing(self.connection.cursor()) as cursor:
            cursor.execute("""
                INSERT INTO completions (habit_id, completed_date)
                VALUES (?, ?);
            """, (habit_id, completed_date))
            self.connection.commit()

    def update_completion_date(self, completion_id, new_date):
        """
        Updates the completion date for a specific completion entry.
        """
        with closing(self.connection.cursor()) as cursor:
            cursor.execute("""
                UPDATE completions
                SET completed_date = ?
                WHERE id = ?;
            """, (new_date, completion_id))
            self.connection.commit()

    def delete_completion(self, habit_id, completed_date):
        """
        Deletes a specific completion by date (regardless of time).
        """
        with closing(self.connection.cursor()) as cursor:
            cursor.execute("""
                DELETE FROM completions
                WHERE habit_id = ?
                AND DATE(completed_date) = DATE(?);
            """, (habit_id, completed_date))
            self.connection.commit()

    def get_all_users(self):
        """
        Retrieves all users from the database.
        Returns:
            list of dict: A list where each user is represented as a dictionary.
        """
        with closing(self.connection.cursor()) as cursor:
            cursor.execute("SELECT * FROM users;")
            users = cursor.fetchall()
            # Get column names from cursor description and zip with each row
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, user)) for user in users]

    def get_all_habits(self, user_id):
        """
        Retrieves all habits for a user from the database.
        Returns:
            list of dict: A list where each habit is represented as a dictionary.
        """
        with closing(self.connection.cursor()) as cursor:
            cursor.execute("SELECT * FROM habits WHERE user_id = ?;", (user_id,))
            habits = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, habit)) for habit in habits]

    def get_completions(self, habit_id):
        """
        Retrieves all completions for a given habit.
        Returns:
            list of dict: A list where each completion is represented as a dictionary.
        """
        with closing(self.connection.cursor()) as cursor:
            cursor.execute("SELECT * FROM completions WHERE habit_id = ?;", (habit_id,))
            completions = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, completion)) for completion in completions]

    def update_habit(self, user_id, old_name, new_name, new_description, new_periodicity):
        """
        Updates the name, description, and periodicity of a habit for a given user.
        """
        with closing(self.connection.cursor()) as cursor:
            cursor.execute("""
                UPDATE habits
                SET name = ?, description = ?, periodicity = ?
                WHERE user_id = ? AND name = ?;
            """, (new_name, new_description, new_periodicity, user_id, old_name))
            self.connection.commit()

    def delete_habit(self, user_id, habit_name):
        """
        Deletes a specific habit for the given user based on the habit name.
        """
        with closing(self.connection.cursor()) as cursor:
            cursor.execute("""
                DELETE FROM habits WHERE user_id = ? AND name = ?;
            """, (user_id, habit_name))
            self.connection.commit()


    def delete_user(self, user_id):
        """
        Deletes a user from the database.
        """
        with closing(self.connection.cursor()) as cursor:
            cursor.execute("DELETE FROM users WHERE id = ?;", (user_id,))
            self.connection.commit()

    def get_user_id(self, username):
        """
        Retrieves the user ID based on the username.
        Args:
            username (str): The username of the user.
        Returns:
            int or None: The user ID if found, otherwise None.
        """
        with closing(self.connection.cursor()) as cursor:
            cursor.execute("SELECT id FROM users WHERE username = ?;", (username,))
            result = cursor.fetchone()
            if result:
                return result[0]  # Return the user ID
            return None

    def get_habit_by_name(self, user_id, habit_name):
        """
        Retrieves a single habit for a user by name.
        Returns:
            dict or None: The habit as a dictionary, or None if not found.
        """
        with closing(self.connection.cursor()) as cursor:
            cursor.execute("SELECT * FROM habits WHERE user_id = ? AND name = ?;", (user_id, habit_name))
            row = cursor.fetchone()
            if row:
                column_names = [desc[0] for desc in cursor.description]
                return dict(zip(column_names, row))
            return None

    def get_habits_by_periodicity(self, user_id, periodicity):
        """
        Retrieves all habits with a specific periodicity for the given user.
        Args:
            user_id (int): The user's ID.
            periodicity (int): The periodicity in days.
        Returns:
            list of dict: Habits that match the periodicity.
        """
        with closing(self.connection.cursor()) as cursor:
            cursor.execute("""
                SELECT * FROM habits 
                WHERE user_id = ? AND periodicity = ?;
            """, (user_id, periodicity))
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row)) for row in rows]

    def get_last_completion(self, habit_id):
        """
        Retrieves the most recent completion for a habit.
        Returns:
            dict or None: The latest completion as a dictionary, or None if not found.
        """
        with closing(self.connection.cursor()) as cursor:
            cursor.execute("""
                SELECT * FROM completions
                WHERE habit_id = ?
                ORDER BY completed_date DESC
                LIMIT 1;
            """, (habit_id,))
            row = cursor.fetchone()
            if row:
                column_names = [desc[0] for desc in cursor.description]
                return dict(zip(column_names, row))
            return None


    def close(self):
        """
        Closes the database connection.
        """
        self.connection.close()
