
from abc import ABC, abstractmethod


class TimeEntryDef(ABC):

    @abstractmethod
    def get_curr_cycle(self):
        pass

    @abstractmethod
    def get_curr_entries(self):
        pass

    @abstractmethod
    def add_entry(self):
        pass

    @abstractmethod
    def update_entry(self, entry_id, updated_entry):
        pass

    @abstractmethod
    def get_headers(self):
        pass
