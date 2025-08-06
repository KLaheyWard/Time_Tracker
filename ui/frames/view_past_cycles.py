import customtkinter as ctk

from services.time_entry_service import TimeEntryService
from ui.frames.display_cycle_frame import DisplayCycleFrame


class ViewPastCycles(ctk.CTkFrame):
    def __init__(self, parent, entries=None):
        super().__init__(parent, corner_radius=10)
        self.configure(fg_color="transparent")
        self.parent = parent
        self.entry_service = TimeEntryService()
        self.entries = entries
        self.current_cycle_id = int(self.entry_service.current_cycle_id)

        self.displayed_cycle = self.current_cycle_id - \
            1 if self.current_cycle_id > 1 else 1

        self.create_widgets()

    def create_widgets(self):
        if (self.current_cycle_id > 1):
            self.create_show_button()
        else:
            # no entries yet
            no_entries_label = ctk.CTkLabel(
                self, text="No past cycles to display.")
            no_entries_label.pack(padx=10, pady=10)

    def create_show_button(self):
        """Creates a button to show past cycles."""
        self.show_button = ctk.CTkButton(
            self, text="Show Past Cycles", command=(lambda: self.open_popup(self.displayed_cycle)))
        self.show_button.pack(side="top", padx=10, pady=10)

    def show_cycle(self, frame, cycle_id):
        """Displays the previous cycle and buttons to navigate between cycles."""
        # cycle to show
        cycle_id = int(cycle_id)

        # entries in the cycle to show
        entries_to_show = [
            entry for entry in self.entries if int(entry.cycle_id) == cycle_id]

        # navigation buttons for popup
        button_frame = self.create_button_frame(frame)

        # decide which nav buttons to disable
        disable_prev_cycle_button = cycle_id <= 1
        disable_next_cycle_button = self.displayed_cycle >= self.current_cycle_id - 1

        # cycle info
        displayed = self.displayed_cycle
        curr = self.current_cycle_id

        # create buttons and add to button frame, then display
        self.create_nav_buttons(
            button_frame, disable_prev_cycle_button, disable_next_cycle_button)
        button_frame.grid()

        # create a DisplayCycleFrame and display it in popup contents
        cycle_frame = DisplayCycleFrame(
            frame, cycle_id=cycle_id, entries=entries_to_show)
        cycle_frame.grid()

    def create_nav_buttons(self, frame, prev_disabled, next_disabled):
        """Creates navigation buttons for the cycle."""
        # configure the buttons
        self.prev_cycle_button = ctk.CTkButton(
            frame, text="Previous", width=70, command=(lambda: self.change_cycles(frame, self.displayed_cycle - 1)))
        self.next_cycle_button = ctk.CTkButton(
            frame, text="Next", width=70, command=(lambda: self.change_cycles(frame, self.displayed_cycle + 1)))
        self.close_button = ctk.CTkButton(
            frame, text="Close", width=70, fg_color="red", hover_color="darkred", command=self.popup.destroy)

        # disable buttons (if necessary)
        if prev_disabled:
            self.disable_button(self.prev_cycle_button)
        if next_disabled:
            self.disable_button(self.next_cycle_button)

        # display the buttons
        self.prev_cycle_button.grid(row=0, column=0, sticky="nsew", padx=10)
        self.close_button.grid(row=0, column=1, sticky="nsew", padx=10)
        self.next_cycle_button.grid(row=0, column=2, sticky="nsew", padx=10)

    def change_cycles(self, frame, cycle_id):
        """Changes the displayed cycle."""
        self.displayed_cycle = cycle_id
        self.popup_contents.destroy()
        self.create_popup_contents(cycle_id)

    def open_popup(self, cycle_id):
        self.popup = ctk.CTkToplevel(self.parent)
        self.popup.title("Past Cycles")
        self.create_popup_contents(cycle_id or self.displayed_cycle)

    def create_popup_contents(self, cycle_id):
        """Creates the contents of the popup."""
        self.popup_contents = ctk.CTkFrame(self.popup, fg_color="transparent")
        self.popup_contents.grid(padx=10, pady=10, sticky="nsew")
        self.show_cycle(self.popup_contents, cycle_id)

    def disable_button(self, button):
        """Disables a button functionally and visually."""
        button.configure(state="disabled")
        button.configure(fg_color="Gray", hover_color="Gray")

    def create_button_frame(self, frame):
        """Creates and configures a frame for the buttons."""
        button_frame = ctk.CTkFrame(
            frame, height=30, width=400, fg_color="transparent")
        for i in range(3):
            button_frame.grid_columnconfigure(i, weight=1)
        button_frame.grid_propagate(False)
        return button_frame
