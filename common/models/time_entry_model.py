from common.constants.work_day import DEFAULT_UNPAID_BREAK_MINUTES


class TimeEntryModel:
    """ Used to represent a single time entry.
    """

    def __init__(self, entry_id, cycle_id, date, start_time, end_time, note, unpaid_break_duration_min=DEFAULT_UNPAID_BREAK_MINUTES):
        self.entry_id = entry_id
        self.cycle_id = cycle_id
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.note = note
        self.unpaid_break_duration_min = unpaid_break_duration_min

    def to_list(self):
        """ Converts the TimeEntryModel instance to a list for CSV writing. """
        return [
            self.entry_id,
            self.cycle_id,
            self.date,
            self.start_time,
            self.end_time,
            self.unpaid_break_duration_min,
            self.note
        ]

    @staticmethod
    def get_headers():
        return ["entry_id", "cycle_id", "date", "start_time", "end_time", "unpaid_break_duration_min", "note"]

    @staticmethod
    def get_pretty_headers():
        return ["Entry ID", "Cycle ID", "Date", "Start Time", "End Time", "Unpaid (min)", "Note"]

    def __repr__(self):
        return f'TimeEntryModel(entry_id={self.entry_id}, cycle_id={self.cycle_id}, date={self.date}, start_time={self.start_time}, end_time={self.end_time}, unpaid_break_duration_min={self.unpaid_break_duration_min}, note="{self.note}")'
