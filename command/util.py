from datetime import datetime


def format_number(number) -> str:
    """Format a number with thousand separators and return a string"""
    try:
        return "{:,}".format(number)
    except ValueError:
        return str(number)


def format_timestamp(timestamp) -> str:
    """Format a unix timestamp in ISO date format"""
    try:
        return datetime.fromtimestamp(timestamp).isoformat(sep=' ', timespec='seconds')
    except TypeError:
        return str(timestamp)


def cut_to_length(text: str, length: int):
    if len(text) > length:
        return f"{text[:length-3]}..."
    return text
