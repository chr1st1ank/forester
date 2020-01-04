from datetime import datetime


def format_number(number) -> str:
    """Format a number with thousand separators and return a string"""
    try:
        return "{:,}".format(number)
    except ValueError:
        return str(number)


def format_timestamp(timestamp) -> str:
    """Format a unix timestamp in ISO date format"""
    return datetime.fromtimestamp(timestamp).isoformat(sep=' ', timespec='seconds')
