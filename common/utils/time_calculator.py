from datetime import datetime, timedelta

from common.constants.work_day import DayTypeHoursEnum


def get_time_worked_in_entry(start_time, end_time, unpaid_break_duration_min=0):
    """
    Calculate the total time worked in a time entry.

    Args:
        start_time (str): Start time in "HH:MM" format.
        end_time (str): End time in "HH:MM" format.
        unpaid_break_duration_min (int, optional): Unpaid break duration in minutes. Defaults to 0.

    Returns:
        int: Total time worked in minutes.
    """
    # TODO: validate inputs
    start = datetime.strptime(start_time, "%H:%M")
    end = datetime.strptime(end_time, "%H:%M")

    diff = end - start
    total_minutes = diff.total_seconds() / 60
    total_minutes = total_minutes - int(unpaid_break_duration_min)

    return max(total_minutes, 0)  # Ensure non-negative time worked


def get_time_worked_in_entries(entries):
    """
    Calculate the total time worked across multiple entries.

    Args:
        entries (list): List of time entries, each with 'start_time', 'end_time', and 'unpaid_break_duration_min'.

    Returns:
        int: Total time worked in minutes across all entries.
    """
    total_time = 0
    for entry in entries:
        total_time += get_time_worked_in_entry(
            entry.start_time, entry.end_time, entry.unpaid_break_duration_min)
    return total_time


def get_estimated_end_time(start_time, unpaid_break_duration_min, day_type=DayTypeHoursEnum.REGULAR):
    """
    Calculate the estimated end time based on start time, how long a day in a cycle should be, and length of unpaid break.

    Args:
        start_time (str): Start time in "HH:MM" format.
        duration_minutes (int): Duration in minutes.

    Returns:
        str: Estimated end time in "HH:MM" format.
    """
    # TODO: validate inputs
    start = datetime.strptime(start_time, "%H:%M")

    shift_length_minutes = day_type.value * 60
    end = start + timedelta(minutes=shift_length_minutes +
                            unpaid_break_duration_min)
    return end.strftime("%H:%M")

    # TODO: use this FN
    def validate_time_format(time_str):
        """Validates that a time string is in the correct "HH:MM" format."""
        try:
            datetime.strptime(time_str, "%H:%M")
            return True
        except ValueError:
            return False
