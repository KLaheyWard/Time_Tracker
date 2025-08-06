import customtkinter as ctk


class DisplayCycleFrame(ctk.CTkFrame):
    def __init__(self, parent, cycle_id=1, entries=[]):
        super().__init__(parent)
        self.configure(fg_color="transparent")
        self.cycle_id = cycle_id
        self.entries = entries
        self.create_widgets()

    def create_widgets(self):
        # Create a label to display the title
        title_label = ctk.CTkLabel(
            self, text=f"Cycle {self.cycle_id}", font=("Arial", 18))
        title_label.pack(padx=5, pady=5)

        # display each entry in the cycle
        for i, entry in enumerate(self.entries):
            entry_label = ctk.CTkLabel(
                self, text=f"Entry {i + 1}: {entry.date} {entry.start_time} - {entry.end_time}, Note: {entry.note}")
            entry_label.pack()
