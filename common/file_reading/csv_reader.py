import csv


class CSVReader:
    def __init__(self, file_path, obj_type):
        self.file_path = file_path
        self.obj_type = obj_type

    def read_csv(self):
        with open(self.file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            return [self._create_object(row) for row in reader]

    def _create_object(self, row):
        return self.obj_type(**row)
