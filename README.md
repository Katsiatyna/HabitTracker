#  Habit Tracker CLI Application

Welcome to the **Habit Tracker** — a Python-based command-line interface (CLI) application for tracking personal habits, their completions, and analyzing your streaks over time using analytics functions built on a functional programming approach.

This application was developed as part of the IU Portfolio Project for the module **DLBDSOOFPP01 – Object-Oriented and Functional Programming with Python**.

---

##  Features

-  User Registration and Login  
-  Habit Creation, Editing, and Deletion  
-  Completion Tracking with Flexible Date Input  
-  Analytics:
  - Longest streak for each habit
  - Longest streak overall
  - Habits due today
-  Habit filtering by periodicity  
-  Built-in Unit Testing using `pytest`

---

##  Technologies Used

- Python 3.11+
- SQLite (via `sqlite3`)
- `Click` for building CLI commands
- `pytest` for testing
- Functional programming principles
- Modular architecture with separation of concerns

---

##  Project Structure

```text
HabitTracker/
├── src/
│   ├── main.py                   # CLI entry point
│   ├── analytics/                # Functional analytics
│   │   └── analytics.py
│   ├── database/                 # SQLite handler
│   │   └── db_handler.py
│   ├── models/                   # Core classes
│   │   ├── habit.py
│   │   ├── user.py
│   │   └── completion.py
│   └── tests/                    # Unit tests
│       ├── test_analytics.py
│       ├── test_completion.py
│       ├── test_db_handler.py
│       ├── test_user.py
│       └── test_habit.py
```

## Hot ro Run

### 1. Clone the repository

  ```bash
git clone https://github.com/Katsiatyna/HabitTracker.git
cd HabitTracker
  ```

### 2. Lunch Application

  ```bash
python src/main.py
  ```

## Running Test

  ```bash
poetry run pytest
  ```

This will run all tests across:
- Habit, User, and Completion model logic
- Database operations (DatabaseHandler)
- Analytics functions (get_longest_streak, habits_to_complete_today, etc.)

## Technologies Used

- Python 3.10+
- SQLite for data storage
- Click for CLI interactions
- Pytest for unit testing
- Functional Programming with map, filter, reduce, and immutability principles

## Author

Katsiaryna Petrushenia

Created for IU’s module DLBDSOOFPP01 – Object-Oriented and Functional Programming with Python

26.05.2025

