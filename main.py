import customtkinter as ctk
from ui.app import App

# Set appearance mode and default color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Create the main window
app = ctk.CTk()
app.title("Compressed Tracker")

main_app = App(app)


# Run the application
app.mainloop()
