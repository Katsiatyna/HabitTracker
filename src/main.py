"""
Author: Katsiaryna Petrushenia
Date: 2023-08-30
Description:
This module serves as the main entry point for the Habit Tracker CLI application.
It enables users to manage their habits, mark completions, and perform analytics using a functional programming paradigm.
The application supports user registration, login, habit management (add, edit, delete), completion management (add, edit, delete), and analytics functionalities.
The analytics module is implemented using functional programming techniques to analyze habit data efficiently.

"""

import click
from src.database.db_handler import DatabaseHandler
from datetime import datetime, timedelta
from src.analytics.analytics import get_longest_streak, get_longest_streak_for_habit
from src.analytics.analytics import get_all_streaks
from src.analytics.analytics import get_habits_to_complete_today

# Initialize the database handler to manage data storage and retrieval
db = DatabaseHandler()

# Global variables to store the current logged-in user's ID and username
current_user_id = None
current_username = None

def create_predefined_habits(user_id):
    """
    Creates 5 predefined habits for a new user.
    Includes at least one daily and one weekly habit.
    Adds example completion data for a period of 4 weeks (28 days),
    with completions spaced according to each habit's periodicity.
    """
    predefined_habits = [
        {"name": "Exercise", "description": "30 minutes of physical exercise", "periodicity": 1},
        {"name": "Reading", "description": "Read 20 pages of a book", "periodicity": 2},
        {"name": "Meditation", "description": "10 minutes of meditation", "periodicity": 3},
        {"name": "Weekly Cleaning", "description": "Clean the house thoroughly", "periodicity": 7},
        {"name": "Grocery Shopping", "description": "Buy weekly groceries", "periodicity": 7}
    ]

    current_date = datetime.now()

    for habit in predefined_habits:
        creation_date = current_date.isoformat()
        db.add_habit(user_id, habit["name"], habit["description"], habit["periodicity"], creation_date)
        click.echo(f"Predefined habit '{habit['name']}' added for the new user.")

        # Retrieve the new habit ID by name
        habits = db.get_all_habits(user_id)
        habit_id = next((h['id'] for h in habits if h['name'] == habit['name']), None)

        # Generate completions every 'periodicity' days over 4 weeks
        completion_date = current_date
        end_date = current_date - timedelta(weeks=4)

        while completion_date >= end_date:
            db.add_completion(habit_id, completion_date.isoformat())
            click.echo(f"Completion for '{habit['name']}' added on {completion_date.strftime('%d-%m-%Y %H:%M:%S')}.")
            completion_date -= timedelta(days=habit["periodicity"])

    click.echo("Predefined habits and example data added successfully.")

def login_or_register():
    """
    Function to handle user login or registration.
    """
    global current_user_id, current_username
    click.echo("\nWelcome to Habit Tracker!")

    while True:
        # Prompt the user to check if they already have an account
        choice = click.prompt("Do you have an account? (Y/N)").strip().lower()

        if choice == "y":
            # Prompt for username and check existence in the database
            username = click.prompt("Enter username")
            users = db.get_all_users()

            # Loop through users to find a matching username
            for user in users:
                if user['username'] == username:
                    current_user_id = user['id']
                    current_username = user['username']
                    click.echo(f"Welcome back, {username}!")
                    menu()  # Show the menu immediately after login
                    return
            else:
                click.echo("User not found. Please register.")

        elif choice == "n":
            # Ask if the user wants to create a new account
            create_account = click.confirm("Would you like to create a new account?")
            if create_account:
                while True:
                    # Prompt for username and email, then check for duplicates
                    username = click.prompt("Enter username")
                    email = click.prompt("Enter email")
                    users = db.get_all_users()

                    # Check if username or email already exists
                    username_exists = any(user['username'] == username for user in users)
                    email_exists = any(user['email'] == email for user in users)

                    if username_exists or email_exists:
                        click.echo("Username or email already exists. Please try again.")
                    else:
                        # No duplicates found, create the new user
                        db.add_user(username, email, datetime.now().isoformat())
                        click.echo(f"User {username} created successfully!")
                        current_user_id = db.get_user_id(username)
                        current_username = username
                        click.echo(f"Welcome, {username}!")

                        # Automatically create predefined habits for the new user
                        create_predefined_habits(current_user_id)

                        menu()  # Show the menu immediately after registration
                        return
            else:
                # Offer the option to exit the program if user doesn't want to create an account
                exit_choice = click.confirm("Would you like to exit the program?")
                if exit_choice:
                    click.echo("Goodbye!")
                    exit()
                else:
                    continue  # Loop back and ask again

        else:
            # Invalid input handler
            click.echo("Invalid input. Please enter 'Y' or 'N'.")

def menu():
    """
    Displays the main menu for the application
    """
    while True:
        click.echo("\nMain menu for Habit Tracker. Please select an option:")
        click.echo("1. Exit")
        click.echo("2. List habits")
        click.echo("3. List completions")
        click.echo("4. List habits by periodicity")
        click.echo("5. Longest streak for all habits")
        click.echo("6. Longest streak for a specific habit")
        click.echo("7. Show all habits that have to be done today")
        click.echo("8. Add habit")
        click.echo("9. Edit habit")
        click.echo("10. Delete habit")
        click.echo("11. Complete habit")
        click.echo("12. Edit completion")
        click.echo("13. Delete completion")
        click.echo("14. Edit user")
        click.echo("15. Logout")

        choice = click.prompt("Enter your choice", type=int)

        if choice == 1:
            click.echo("Goodbye!")
            exit()
        elif choice == 2:
            list_habits()
        elif choice == 3:
            list_completions()
        elif choice == 4:
            list_habits_by_periodicity()
        elif choice == 5:
            longest_streak_all()
        elif choice == 6:
            longest_streak_for_habit()
        elif choice == 7:
            habits_to_complete_today()
        elif choice == 8:
            add_habit()
        elif choice == 9:
            edit_habit()
        elif choice == 10:
            delete_habit()
        elif choice == 11:
            complete_habit()
        elif choice == 12:
            edit_completion()
        elif choice == 13:
            delete_completion()
        elif choice == 14:
            edit_user()
        elif choice == 15:
            logout()
            return
        else:
            click.echo("Invalid choice. Please try again.")

@click.group()
def cli():
    """
    Entry point for the Habit Tracker CLI.
    Groups all commands under a single CLI interface
    """
    pass

@cli.command()
def add_habit():
    """
    Adds a new habit to the database.
    Prompts the user for habit details.
    """
    global current_user_id

    while True:
        # Promt for habit details
        name = click.prompt("Enter habit name")
        description = click.prompt("Enter habit description")
        periodicity = click.prompt("Enter habit periodicity (number of days)", type=int)
        creation_date = datetime.now().isoformat()

        # Fetch existing habits for the user
        habits = db.get_all_habits(current_user_id)

        # Check if a habit with the same name already exists
        if any(habit['name'] == name for habit in habits):
            click.echo("A habit with this name already exists. Please try again.")
        else:
            # Add the new habit to the database
            db.add_habit(current_user_id, name, description, periodicity, creation_date)
            click.echo(f"Habit {name} added successfully!")
            menu()
            break

@cli.command()
def complete_habit():
    """
    Marks a specified habit as completed.
    Uses the habit ID to update the completion status in the database.
    """
    global current_user_id

    # Prompt the user to enter the habit name
    habit_name = click.prompt("Enter the habit name")
    habits = db.get_all_habits(current_user_id)

    # Find the habit with the specified name
    for habit in habits:
        if habit['name'] == habit_name:
            # Prompt for completion date
            while True:
                completion_input = click.prompt("Enter the completion date (YYYY-MM-DD) or type 'today'")
                if completion_input.lower() == 'today':
                    completion_date = datetime.now().isoformat()
                    break
                try:
                    completion_date = datetime.strptime(completion_input, "%Y-%m-%d").isoformat()
                    break
                except ValueError:
                    click.echo("Invalid date format. Please enter a valid date (YYYY-MM-DD).")
                    continue

            # Add completion (this now happens **after** breaking the loop)
            db.add_completion(habit['id'], completion_date)
            click.echo(f"Habit '{habit_name}' completed on {datetime.fromisoformat(completion_date).strftime('%d-%m-%Y')}.")
            menu()
            return

    # Habit not found
    click.echo(f"Habit '{habit_name}' not found.")
    menu()


@cli.command()
def longest_streak_all():
    """
    Displays the longest streaks for all habits of the logged-in user.
    """
    global current_user_id
    streaks = get_all_streaks(db, current_user_id)
    if not streaks:
        click.echo("No habits found.")
    else:
        for entry in streaks:
            click.echo(f"Habit: {entry['name']}, Longest Streak: {entry['streak']} completions in a row")
    menu()

@cli.command()
def longest_streak_for_habit():
    """
    Displays the longest streak for a specific habit.
    """
    global current_user_id
    habit_name = click.prompt("Enter habit name")
    habit = db.get_habit_by_name(current_user_id, habit_name)
    if habit:
        streak = get_longest_streak_for_habit(db, habit['id'], habit['periodicity'])
        click.echo(f"Longest streak for '{habit['name']}': {streak} completions in a row")
    else:
        click.echo(f"Habit '{habit_name}' not found.")
    menu()

@cli.command()
def list_habits_by_periodicity():
    """
    Lists all habits of the logged-in user by periodicity.
    """
    periodicity = click.prompt("Enter periodicity (number of days)", type=int)
    habits = db.get_habits_by_periodicity(current_user_id, periodicity)
    for habit in habits:
        click.echo(f"Name: {habit['name']}, Description: {habit['description']}, Periodicity: {habit['periodicity']}")
    menu()

@cli.command()
def edit_user():
    """
    Edit the logged-in user's username or email.
    """
    global current_user_id
    new_username = click.prompt("Enter new username")
    new_email = click.prompt("Enter new email")
    db.update_user(current_user_id, new_username, new_email)
    click.echo("User updated successfully!")
    menu()

@cli.command()
def edit_habit():
    """
    Edit a habit of the logged-in user.
    """
    habit_name = click.prompt("Enter the habit name to edit")
    new_name = click.prompt("New habit name")
    new_description = click.prompt("New habit description")
    new_periodicity = click.prompt("New periodicity (number of days)", type=int)
    db.update_habit(current_user_id, habit_name, new_name, new_description, new_periodicity)
    click.echo(f"Habit '{habit_name}' updated.")
    menu()

@cli.command()
def edit_completion():
    """
    Edits a specific completion date for a habit.
    """
    global current_user_id
    habit_name = click.prompt("Enter the habit name")
    habit = db.get_habit_by_name(current_user_id, habit_name)

    if not habit:
        click.echo(f"Habit '{habit_name}' not found.")
        return menu()

    completions = db.get_completions(habit['id'])
    if not completions:
        click.echo(f"No completions found for '{habit_name}'.")
        return menu()

    # Sort by date descending
    completions_sorted = sorted(completions, key=lambda c: c['completed_date'], reverse=True)

    click.echo(f"\nCompletions for '{habit_name}':")
    for comp in completions_sorted:
        formatted = datetime.fromisoformat(comp['completed_date']).strftime('%d-%m-%Y')
        click.echo(f"- ID: {comp['id']} | Date: {formatted}")

    # Ask which completion to edit (by ID)
    comp_id = click.prompt("Enter the ID of the completion you want to edit", type=int)
    target_completion = next((c for c in completions if c['id'] == comp_id), None)

    if not target_completion:
        click.echo("Completion ID not found.")
        return menu()

    # Ask for the new date
    new_date_str = click.prompt("Enter the new completion date (YYYY-MM-DD)")
    try:
        new_date = datetime.strptime(new_date_str, "%Y-%m-%d").isoformat()
        db.update_completion_date(comp_id, new_date)
        click.echo(f"Completion updated to {new_date_str}.")
    except ValueError:
        click.echo("Invalid date format.")

    menu()


@cli.command()
def delete_habit():
    """
    Delete a habit of the logged-in user.
    """
    habit_name = click.prompt("Enter the habit name to delete")
    db.delete_habit(current_user_id, habit_name)
    click.echo(f"Habit '{habit_name}' deleted.")
    menu()

@cli.command(name="habits-to-complete-today")
def habits_to_complete_today():
    """
    Lists habits that are due today but haven't been completed yet.
    """
    global current_user_id
    habits = get_habits_to_complete_today(db, current_user_id)

    if not habits:
        click.echo("No habits due today. Well done!")
    else:
        click.echo("Habits you should complete today:")
        for habit in habits:
            click.echo(f"- {habit['name']} (Every {habit['periodicity']} day(s))")
    menu()


@cli.command()
def delete_completion():
    """
    Delete a specific completion date for a habit.
    """
    global current_user_id
    habit_name = click.prompt("Enter habit name")
    habits = db.get_all_habits(current_user_id)
    habit = next((h for h in habits if h['name'] == habit_name), None)

    if not habit:
        click.echo(f"Habit '{habit_name}' not found.")
        return

    completions = db.get_completions(habit['id'])
    if not completions:
        click.echo(f"No completions found for '{habit_name}'.")
        return

    click.echo(f"Completions for '{habit_name}':")
    for c in completions:
        formatted_date = datetime.fromisoformat(c['completed_date']).strftime('%d-%m-%Y')
        click.echo(f"- {formatted_date}")

    input_date = click.prompt("Enter the date to delete (DD-MM-YYYY)")
    try:
        iso_date = datetime.strptime(input_date, "%d-%m-%Y").isoformat()
        db.delete_completion(habit['id'], iso_date)
        click.echo(f"Completion on {input_date} deleted successfully.")
    except ValueError:
        click.echo("Invalid date format.")
    menu()

@cli.command()
def list_habits():
    """
    List all habits associated with the current logged-in user.
    Displays habit ID, name, description, periodicity, and creation date.
    """
    global current_user_id
    habits = db.get_all_habits(current_user_id)  # Fetch habits for the given user ID
    if not habits:
        click.echo("No habits found.")
        return

    for habit in habits:
        click.echo(f"ID: {habit['id']}, Name: {habit['name']}, Description: {habit['description']}, Periodicity: {habit['periodicity']}, Creation Date: {habit['creation_date']}")
    menu()

@cli.command()
def list_completions():
    """
    Lists all completions for all habits of the current user.
    """
    global current_user_id
    habits = db.get_all_habits(current_user_id)

    if not habits:
        click.echo("No habits found.")
        return

    for habit in habits:
        completions = db.get_completions(habit['id'])
        if completions:
            click.echo(f"\nCompletions for habit: {habit['name']}")
            for comp in completions:
                date_str = comp['completed_date']
                formatted_date = datetime.fromisoformat(date_str).strftime('%d-%m-%Y')
                click.echo(f"- Completion ID: {comp['id']}, Date: {formatted_date}")
        else:
            click.echo(f"\nNo completions for habit: {habit['name']}")

    menu()

@cli.command()
def logout():
    """
    Command to log out of the application.
    """
    global current_user_id, current_username
    current_user_id = None
    current_username = None
    click.echo("Logged out successfully.")
    login_or_register()

@cli.command()
def close_db():
    """
    Command to close the database connection.
    """
    db.close()
    click.echo("Database connection closed.")

# Entry point for the Habit Tracker CLI
if __name__ == "__main__":
    login_or_register()  # Start the login process immediately