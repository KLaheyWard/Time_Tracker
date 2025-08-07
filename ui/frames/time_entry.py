from datetime import datetime

import customtkinter as ctk

from common.models.time_entry_model import TimeEntryModel


class TimeEntryFrame(ctk.CTkFrame):
    """Used to create a frame that holds a single time entry.

    Initialize with either header=True to create a header row with pretty labels or pass in a TimeEntryModel with values set to display the values.
    """

    def __init__(self, parent, app, time_entry=None, width=800, header=False):
        super().__init__(parent, width=width)
        self.parent = parent
        self.app = app
        self.configure(fg_color="transparent")
        self.entry_service = parent.entry_service
        self.id = time_entry.entry_id if time_entry else None
        if (header):
            self._create_labels(TimeEntryModel.get_pretty_headers())
        else:
            self.time_entry = time_entry
            self._generate_values()

        self.pack(expand=True)

    def _create_value(self, value, col, row, width=200):
        "Creates a single value field in the frame."
        val = ctk.CTkEntry(self, height=5, width=width)
        val.insert("end", value)
        val.bind("<FocusOut>", self.save_entry)
        val.pack(expand=True, side="left", padx=5, pady=5)

        return val

    def _generate_values(self):
        "Creates the row of values for the time entry."

        # transform date from yyyy-mm-dd to a datetime
        day_of_week = datetime.strptime(
            self.time_entry.date, "%Y-%m-%d").strftime("%A")
        day_of_week_label = ctk.CTkLabel(
            self, text=day_of_week, fg_color="#1c1c1c", corner_radius=5, width=100)
        day_of_week_label.pack(side="left", padx=4, pady=4)

        self.date_value = self._create_value(self.time_entry.date, 0, 0, 100)
        self.start_time_value = self._create_value(
            self.time_entry.start_time, 1, 0, 70)
        self.end_time_value = self._create_value(
            self.time_entry.end_time, 2, 0, 70)
        self.unpaid_break_value = self._create_value(
            self.time_entry.unpaid_break_duration_min, 3, 0, 50)
        self.note_value = self._create_value(
            self.time_entry.note, 4, 0, 200)

    def _create_labels(self, headers):
        header_widths = [220, 70, 70, 50, 150]
        # Skip the first header
        for i, header in enumerate(headers[2:]):
            label = ctk.CTkLabel(self, fg_color="#1c1c1c", corner_radius=5,
                                 text=header, width=header_widths[i])
            label.pack(side="left", padx=4, pady=4)

    def save_entry(self, event):
        """Saves the current entry values."""
        # TODO: maybe call validator after getting data or in the save ? to think about.

        # TODO: maybe validate the event.widget.get() value

        new_date = self.date_value.get()
        new_start_time = self.start_time_value.get()
        new_end_time = self.end_time_value.get()
        new_unpaid_break_duration_min = int(
            self.unpaid_break_value.get())
        new_note = self.note_value.get()
        updated_time_entry = TimeEntryModel(
            entry_id=self.id,
            cycle_id=self.time_entry.cycle_id,
            date=new_date,
            start_time=new_start_time,
            end_time=new_end_time,
            note=new_note,
            unpaid_break_duration_min=new_unpaid_break_duration_min
        )
        self.entry_service.update_entry(self.id, updated_time_entry)
        print(f"Saved entry: {self.time_entry}")
        self.show_success_message()

    def show_success_message(self):
        # Create the message label
        success_label = ctk.CTkLabel(
            self, text="✅")
        success_label.pack(side="left", padx=5, pady=5)

        # Remove it after 2 seconds (2000 ms)
        self.after(2000, self.app.destroy_widgets)
