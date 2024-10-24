# common_functions.py

import math

def is_number(string:str) -> bool:
    """Checks if string passed could be a number

    Args:
        string (str): imput string

    Returns:
        bool: returns true if string represents a number
    """
    try:
        float(string)
        return True
    except ValueError:
        return False


def compare_number_strings(str1:str, str2:str) -> bool:
    """ Compares two strings that contain numbers, returns true if the match

    Args:
        str1 (str): string 1
        str2 (str): string 2

    Returns:
        bool: Comparison result
    """
    try:
        num1 = float(str1)
        num2 = float(str2)
        
        return math.isclose(num1,num2)
    except ValueError:
        return False

