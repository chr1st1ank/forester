

def format_number(number) -> str:
    """Format a number with thousand separators and return a string"""
    try:
        return "{:,}".format(number)
    except ValueError:
        return str(number)
