"""
A small set of utilities for entering simple inputs and validating them.
"""


def input_int(prompt: str) -> int:
    """
    Prompt the user for a valid integer on the console.
    :param prompt: Text string to display so that the user knows what they are entering.
    :return: The entered integer.  This routine wil not stop until it gets one.
    """
    valid: bool = False
    value: int = 0
    while not valid:
        try:
            value = int(input(prompt))
            valid = True
        except ValueError:
            print('Not a valid integer.  Try again')
    return value


def input_int_range(prompt: str, minimum: int, maximum: int) -> int:
    """
    Prompt the user for a valid integer within a set range on the console.
    :param prompt: Text string to display so that the user knows what they are entering.
    :param minimum: Lowest allowable value.
    :param maximum: Greatest allowable value.  Be sure this is > minimum.
    :return: The entered integer value.
    """
    valid: bool = False
    value: int = 0
    while not valid:
        value = input_int(prompt)
        if value < minimum:
            print(f'Value cannot be less than: {minimum}')
        elif value > maximum:
            print(f'Value cannot be greater than {maximum}')
        else:
            valid = True
    return value


def input_float(prompt: str) -> float:
    """
    Prompt the user for a valid float value on the console.
    :param prompt: Text string to display so that the user knows what they are entering.
    :return: The entered float value.  This routine wil not stop until it gets one.
    """
    valid: bool = False
    value: float = 0
    while not valid:
        try:
            value = float(input(prompt))
            valid = True
        except ValueError:
            print('Not a valid floating point value.  Try again')
    return value


def input_float_range(prompt: str, minimum: float, maximum: float) -> float:
    """
    Prompt the user for a valid float value within a set range on the console.
    :param prompt: Text string to display so that the user knows what they are entering.
    :param minimum: Lowest allowable value.
    :param maximum: Greatest allowable value.  Be sure this is > minimum.
    :return: The entered float value.
    """
    valid: bool = False
    value: float = 0
    while not valid:
        value = input_float(prompt)
        if value < minimum:
            print(f'Value cannot be less than: {minimum}')
        elif value > maximum:
            print(f'Value cannot be greater than {maximum}')
        else:
            valid = True
    return value
