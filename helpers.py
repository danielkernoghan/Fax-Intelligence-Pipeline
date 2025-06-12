import re
from dateutil import parser

def is_numeric_ignore_spaces(s):
    """
    Checks if a string is numeric, ignoring any spaces.

    Parameters:
        s (str): The input string to be checked.

    Returns:
        bool: True if the string is numeric after removing spaces, False otherwise.
    """
    s = s.replace(" ", "")
    return s.isnumeric()

def convert_date(date):
    """
    Converts a date string into a standardized format (MM-DD-YYYY).

    Parameters:
        date (str): The input date string to be converted.

    Returns:
        str: The date in MM-DD-YYYY format.
    """
    try:
        standardized_date = parser.parse(date).strftime('%m-%d-%Y')
    except Exception:
        standardized_date = "UnknownDate"
    return standardized_date
