from datetime import datetime

from customtkinter import CTkButton, CTkFrame

from common.constants.cycles import NUM_DAYS_IN_CYCLE
from common.constants.work_day import DEFAULT_UNPAID_BREAK_MINUTES, DayTypeHoursEnum
from common.models.time_entry_model import TimeEntryModel
from common.utils.time_calculator import get_estimated_end_time
from services.time_entry_service import TimeEntryService
from services.time_tracker_service import TimeTrackerService
from ui.frames.all_time_entries_in_cycle import AllCycleEntries
from ui.frames.time_entry import TimeEntryFrame
from ui.frames.time_tracker_frame import TimeTrackerFrame
from ui.frames.view_past_cycles import ViewPastCycles


class App(CTkFrame):

    def __init__(self, app):
        self.entry_service = TimeEntryService()
        self.tracker_service = TimeTrackerService()
        self.app = self

        super().__init__(app, fg_color="transparent")
        self.configure(fg_color="transparent", corner_radius=10)
        # Configure 3 columns inside the main_frame
        self.pack(expand=True)

        # Create and place widgets
        self.create_widgets()

    def create_widgets(self):
        widget_frame = CTkFrame(self, corner_radius=10, fg_color="transparent")
        # current cycle time entries
        self.all_entries = AllCycleEntries(
            widget_frame, self.app)
        self.create_action_buttons(widget_frame)
        self.create_time_tracker(widget_frame)
        self.create_history_viewer(widget_frame)

        widget_frame.pack(fill="both",
                          expand=True, padx=10, pady=10)

    def create_add_entry_button(self, frame):
        """Creates a button to add a new time entry."""
        return CTkButton(
            frame, text="Add Regular Day", command=(lambda: self.add_entry(day_type=DayTypeHoursEnum.REGULAR)),)

    def create_add_holiday_button(self, frame):
        """Creates a button to add a new holiday entry."""
        return CTkButton(
            frame, text="Add Holiday", command=(lambda: self.add_entry(day_type=DayTypeHoursEnum.HOLIDAY)), fg_color="#9c0263", hover_color="#6e0045")

    def add_entry(self, day_type=DayTypeHoursEnum.REGULAR):
        """Adds a new time entry."""
        now = datetime.now().astimezone()

        # TODO: remove - this is for testing only
        now = datetime(2025, 8, 5, 7, 30, 0)

        note_value = 'Regular work day' if day_type == DayTypeHoursEnum.REGULAR else 'Holiday'

        time_entry = TimeEntryModel(
            entry_id=None,  # This will be set by the CSVWriter
            cycle_id=self.entry_service.current_cycle_id,
            date=now.strftime("%Y-%m-%d"),
            start_time=now.strftime("%H:%M"),
            end_time=get_estimated_end_time(now.strftime(
                "%H:%M"), DEFAULT_UNPAID_BREAK_MINUTES, day_type=day_type),
            unpaid_break_duration_min=DEFAULT_UNPAID_BREAK_MINUTES,
            note=note_value
        )

        TimeEntryFrame(
            self, self.app, time_entry=time_entry, header=False)
        self.entry_service.add_entry(time_entry)
        self.destroy_widgets()

    def create_start_new_cycle_button(self, frame):
        """Creates a button to start a new cycle."""
        return CTkButton(
            frame, text="Start New Cycle", command=self.start_new_cycle, fg_color="green", hover_color="darkgreen")

    def start_new_cycle(self):
        """Starts a new cycle and refreshes the entries."""
        self.tracker_service.bank_cycle_hours()
        self.entry_service.start_new_cycle()
        self.destroy_widgets()

    def destroy_widgets(self):
        """Destroys all widgets in the frame."""
        for widget in self.winfo_children():
            widget.destroy()
        self.create_widgets()

    def create_action_buttons(self, frame):
        """Creates action buttons for the frame."""
        action_button_frame = CTkFrame(frame, fg_color="transparent")
        action_button_frame_top_row = CTkFrame(
            action_button_frame, fg_color="transparent")

        add_entry_button = self.create_add_entry_button(
            action_button_frame_top_row)
        create_add_holiday_button = self.create_add_holiday_button(
            action_button_frame_top_row)
        start_new_cycle_button = self.create_start_new_cycle_button(
            action_button_frame)

        # Place the buttons in the action button frame
        create_add_holiday_button.pack(
            side="left", padx=5, pady=5)
        add_entry_button.pack(side="left", padx=5, pady=5)
        action_button_frame_top_row.pack(padx=5, pady=5)

        if len(self.entry_service.get_curr_entries()) >= NUM_DAYS_IN_CYCLE:
            start_new_cycle_button.pack(padx=5, pady=5, expand=True)

        # add frame to app
        action_button_frame.pack(padx=10, pady=10)

    def create_time_tracker(self, frame):
        self.time_tracker = TimeTrackerFrame(frame)
        self.time_tracker.pack()

    def create_history_viewer(self, frame):
        history_viewer = ViewPastCycles(frame,
                                        entries=self.entry_service.refresh_entries())
        history_viewer.pack(pady=10, padx=20, fill="x")
