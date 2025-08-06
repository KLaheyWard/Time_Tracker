import customtkinter as ctk

from common.constants.colours import BAD, GREAT, NEUTRAL
from services.time_entry_service import TimeEntryService
from services.time_tracker_service import TimeTrackerService


class TimeTrackerFrame(ctk.CTkFrame):
    """Frame to display extra time or time owed based on current cycle entries."""

    def __init__(self, app):
        super().__init__(app)
        # font
        self.bold = ctk.CTkFont(family="Arial", size=16, weight="bold")
        self.configure(fg_color="transparent")
        # services
        self.entry_service = TimeEntryService()
        self.tracker_service = TimeTrackerService()
        self.pack()

        # Create and place widgets
        self.create_widgets()

    def create_widgets(self):
        """Creates the widgets for the time tracker frame."""
        self.create_labels()
        self.create_bank_display()

    def create_labels(self):
        """Creates the labels for the time tracker frame."""
        time_owed = round(self.tracker_service.get_hours_owed(), 2)
        time_owed_abs = abs(time_owed)

        # the emoji to show
        time_emoji = "🚀" if time_owed < 0 else "🥴" if time_owed > 0 else "🎯"
        # the label text that describes the time owed
        time_owed_label_text = "Owed:" if time_owed > 0 else "Extra:" if time_owed < 0 else "On Target:"

        # Create the labels
        time_owed_label = ctk.CTkLabel(
            self, text=f"{time_owed_label_text} {time_owed_abs:.2f}", font=self.bold, text_color=self.calculate_time_colour(time_owed))
        time_owed_emoji = ctk.CTkLabel(
            self, text=time_emoji, font=("Arial", 20))

        # add to frame
        time_owed_label.pack(side="left", padx=10, pady=10)
        time_owed_emoji.pack(side="left", padx=10, pady=10)

    def create_bank_display(self):
        """Creates a frame to hold the banked time display."""
        # value to display
        banked_time = self.tracker_service.banked_time

        # configure frame and labels
        banked_frame = ctk.CTkFrame(
            self, corner_radius=10, fg_color="#1c1c1c")
        banked_time_label = ctk.CTkLabel(
            banked_frame, text="Banked", font=("Arial", 14))
        banked_time_value = ctk.CTkLabel(
            banked_frame, text=f"{banked_time:.2f}", font=self.bold, text_color=self.calculate_time_colour(banked_time))

        # pack
        banked_time_label.pack(padx=10)
        banked_time_value.pack(padx=10)
        banked_frame.pack(padx=10, pady=20)

    def calculate_time_colour(self, time_owed):
        """Calculates the colour based on the time owed."""
        if time_owed < 0:
            return GREAT
        elif time_owed > 0:
            return BAD
        else:
            return NEUTRAL
