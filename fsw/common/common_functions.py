import math

def is_number(string:str) -> bool:
    try:
        float(string)
        return True
    except ValueError:
        return False


def compare_number_strings(str1:str, str2:str) -> bool:
    try:
        num1 = float(str1)
        num2 = float(str2)
        
        return math.isclose(num1,num2)
    except ValueError:
        # conversion failed
        return False