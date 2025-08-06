
from common.models.curr_cycle_model import CurrCycleModel
from common.models.time_entry_model import TimeEntryModel
from common.models.bank_model import BankModel
from common.file_reading.csv_reader import CSVReader
from common.file_reading.csv_writer import CSVWriter
from common.interfaces.time_entry_def import TimeEntryDef
from common.utils.time_calculator import get_time_worked_in_entries
from common.constants.cycles import NUM_HOURS_IN_CYCLE, NUM_DAYS_IN_CYCLE


class TimeTrackerService():
    def __init__(self):
        # current cycle
        self.curr_cycle_reader = CSVReader(
            "./data/current_cycle.csv", obj_type=CurrCycleModel)

        # current entries
        self.entries_reader = CSVReader(
            "./data/time.csv", obj_type=TimeEntryModel)

        # banked time
        self.bank_reader = CSVReader(
            "./data/bank.csv", obj_type=BankModel)
        self.bank_writer = CSVWriter(
            "./data/bank.csv", BankModel.get_headers())

        # get data
        self.refresh()

    def get_curr_cycle_time_worked(self):
        # convert from min to hours
        return get_time_worked_in_entries(self.current_entries) / 60

    def get_expected_hours_worked(self):
        """Returns the expected hours worked based on the number of entries in the current cycle."""
        num_entries_in_cycle = len(self.current_entries)
        hours_expected_so_far = NUM_HOURS_IN_CYCLE / \
            NUM_DAYS_IN_CYCLE * num_entries_in_cycle

        return hours_expected_so_far

    def get_hours_owed(self, for_whole_cycle=False):
        """Returns the hours owed based on the current cycle time worked and expected hours worked."""
        time_worked = self.get_curr_cycle_time_worked(
        )
        if for_whole_cycle:
            expected_worked = NUM_HOURS_IN_CYCLE + self.banked_time
        else:
            expected_worked = self.get_expected_hours_worked() + self.banked_time

        return expected_worked - time_worked

    def bank_cycle_hours(self):
        """Saves the extra or owed hours to the bank for the current cycle."""
        self.refresh()
        time_worked = self.get_hours_owed(for_whole_cycle=True)
        new_bank = BankModel(cycle_id=self.current_cycle_id,
                             balance=time_worked)
        self.bank_writer.write_row(new_bank)

    def refresh(self):
        """Fetches the latest data from the CSV files."""
        self.current_cycle_id = self.curr_cycle_reader.read_csv()[0].cycle_id
        self.entries = self.entries_reader.read_csv(
        ) if self.entries_reader.read_csv() else []
        self.current_entries = [
            entry for entry in self.entries if entry.cycle_id == self.current_cycle_id]
        self.all_banks = self.bank_reader.read_csv(
        ) if self.bank_reader.read_csv() else []
        # find the bank with with current cycle ID - 1 (cycle before the current one)
        self.bank_from_last_cycle = 0 if len(self.all_banks) == 0 else next(
            (bank for bank in self.all_banks if float(bank.cycle_id) == float(self.current_cycle_id) - 1), None)

        self.banked_time = float(
            self.bank_from_last_cycle.balance if self.bank_from_last_cycle else 0)
