"""
Sample application for testing StackTrace AI debugging system.
Contains multiple functions with intentional bugs.
"""

import json


def validate_token(token, secret):
    """
    Validate API token.
    """
    if token != secret:
        raise ValueError("Invalid token")
    return True


def divide_numbers(a, b):
    """
    Divide two numbers.
    """
    return a / b


def parse_user_data(data):
    """
    Parse user JSON data.
    """
    user = json.loads(data)
    return user["name"]


def get_user_email(user):
    """
    Return email from user object.
    """
    return user.email


def process_items(items):
    """
    Process list items.
    """
    for i in range(len(items) + 1):
        print(items[i])


def connect_database(url):
    """
    Dummy database connection.
    """
    if not url:
        raise ConnectionError("Database URL missing")

    print("Connected to database")


def calculate_average(numbers):
    """
    Calculate average of numbers.
    """
    total = sum(numbers)
    return total / len(numbers)


def main():

    # TypeError test
    validate_token("abc123")

    # ZeroDivisionError test
    divide_numbers(10, 0)

    # JSON / KeyError test
    parse_user_data('{"age":25}')

    # AttributeError test
    user = {"email": "test@test.com"}
    get_user_email(user)

    # IndexError test
    process_items([1, 2, 3])

    # ConnectionError test
    connect_database("")

    # ZeroDivisionError test
    calculate_average([])


if __name__ == "__main__":
    main()