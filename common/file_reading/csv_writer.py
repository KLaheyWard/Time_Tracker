import csv
import os
from common.models.time_entry_model import TimeEntryModel


class CSVWriter:
    def __init__(self, file_path, headers):
        self.file_path = file_path
        self.headers = headers
        self._initialize_csv()

    def _initialize_csv(self):
        if not os.path.exists(self.file_path) or os.path.getsize(self.file_path) == 0:
            with open(self.file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(self.headers)

    def write_row(self, row):
        if (type(row) != list):
            row = row.to_list()
        with open(self.file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(row)

    def update_row(self, entry_id, new_data):
        rows = []
        with open(self.file_path, mode='r', newline='') as file:
            reader = csv.reader(file)
            headers = next(reader)
            for row in reader:
                if row[0] == entry_id:  # Assuming entry_id is in the first column
                    row = new_data.to_list()  # Replace the row with new data
                rows.append(row)

        with open(self.file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(rows)

    def erase_file_contents(self):
        """Erases the contents of the CSV file."""
        with open(self.file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(self.headers)
