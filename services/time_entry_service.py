
from common.models.curr_cycle_model import CurrCycleModel
from common.models.time_entry_model import TimeEntryModel
from common.models.bank_model import BankModel
from common.file_reading.csv_reader import CSVReader
from common.file_reading.csv_writer import CSVWriter
from common.interfaces.time_entry_def import TimeEntryDef


class TimeEntryService():
    def __init__(self):
        # current cycle
        self.curr_cycle_reader = CSVReader(
            "./data/current_cycle.csv", obj_type=CurrCycleModel)
        self.current_cycle_id = self.curr_cycle_reader.read_csv()[0].cycle_id
        self.curr_cycle_writer = CSVWriter(
            "./data/current_cycle.csv", CurrCycleModel.get_headers())
        print(f'Current cycle ID: {self.current_cycle_id}')

        # current entries
        self.entries_reader = CSVReader(
            "./data/time.csv", obj_type=TimeEntryModel)
        self.entries_writer = CSVWriter(
            "./data/time.csv", TimeEntryModel.get_headers())
        self.entries = self.entries_reader.read_csv(
        ) if self.entries_reader.read_csv() else []

    def get_curr_cycle(self):
        return self.current_cycle

    def get_curr_entries(self):
        e = self.entries
        curr_cycle = self.current_cycle_id
        return [entry for entry in self.entries if int(entry.cycle_id) == int(self.current_cycle_id)]

    def add_entry(self, entry):
        # new entry with time that is 8h 20min
        if entry.entry_id is None:
            # Assign a new ID if it is not set
            entry.entry_id = len(self.entries) + 1
        self.entries_writer.write_row(entry)
        self.refresh_entries()

    def update_entry(self, id, updated_entry):
        print(f'UPDATING:: ID: {id}, Updated Entry: {updated_entry}')
        self.entries_writer.update_row(id, updated_entry)

    def get_headers(self):
        return TimeEntryModel.get_headers()

    def refresh_entries(self):
        """Refreshes the entries from the CSV file."""
        self.entries = self.entries_reader.read_csv()
        print(f'Refreshed entries: {self.entries}')
        return self.entries

    def start_new_cycle(self):
        """Starts a new cycle by creating a new current cycle."""
        new_cycle = CurrCycleModel(cycle_id=(int(self.current_cycle_id) + 1))
        self.curr_cycle_writer.erase_file_contents()
        self.curr_cycle_writer.write_row(new_cycle)
        self.current_cycle_id = new_cycle.cycle_id
        print(f'Started new cycle with ID: {self.current_cycle_id}')

    def refresh_cycle(self):
        """Refreshes the entries from the CSV file."""
        self.current_cycle_id = self.curr_cycle_reader.read_csv()[0].cycle_id
        print(f'Refreshed entries: {self.entries}')
