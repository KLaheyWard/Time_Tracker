import customtkinter as ctk
from customtkinter import CTkFrame

from services.time_entry_service import TimeEntryService
from ui.frames.time_entry import TimeEntryFrame


class AllCycleEntries(CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, corner_radius=10)
        self.configure(fg_color="transparent")
        self.parent = parent
        self.app = app
        self.entry_service = TimeEntryService()
        self.current_entries = self.entry_service.get_curr_entries()
        self.cycle_id = self.entry_service.current_cycle_id

        # Create and place widgets
        self.create_widgets()

        self.pack()

    def create_labels(self):
        self.header = TimeEntryFrame(self, self.app, header=True)

    def create_widgets(self):
        self.create_labels()
        entries_to_display = [TimeEntryFrame(
            self, self.app, entry) for entry in self.current_entries]

        if len(entries_to_display) <= 0:
            # create and display a label saying no entries have been added yet
            no_entries_label = ctk.CTkLabel(
                self, text="No entries have been added yet.")
            no_entries_label.pack(expand=True, padx=10, pady=10)
