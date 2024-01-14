import re

def convert_time_string_to_seconds(time_string):
    # Extract days, hours, minutes, and seconds using regular expressions
    days_match = re.search(r'(\d+)d', time_string)
    hours_match = re.search(r'(\d+)h', time_string)
    minutes_match = re.search(r'(\d+)m', time_string)
    seconds_match = re.search(r'(\d+)s', time_string)

    # Assign extracted values or default to 0
    days = int(days_match.group(1)) if days_match else 0
    hours = int(hours_match.group(1)) if hours_match else 0
    minutes = int(minutes_match.group(1)) if minutes_match else 0
    seconds = int(seconds_match.group(1)) if seconds_match else 0

    # Calculate total seconds
    total_seconds = days * 86400 + hours * 3600 + minutes * 60 + seconds

    return total_seconds
