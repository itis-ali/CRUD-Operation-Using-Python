import customtkinter as ctk
import calendar
from tkinter import Toplevel
from datetime import datetime

class CustomDatePicker:
    def __init__(self, parent, entryWidget):
        """
        Initialize the Custom Date Picker.
        :param parent: The parent window where the date picker will open.
        :param entryWidget: The entry widget (e.g., CTkEntry) where the selected date will be displayed.
        """
        self.parent = parent
        self.entryWidget = entryWidget
        self.currentDate = datetime.now()
        self.selectedYear = self.currentDate.year
        self.selectedMonth = self.currentDate.month

    def openDatePicker(self):
        """Opens the date picker window."""
        self.topWindow = Toplevel(self.parent)
        self.topWindow.geometry("560x500")
        self.topWindow.title("Pick a Date")
        self.topWindow.resizable(False, False)
        self.topWindow.configure(bg="#333333")

        # Navigation Frame for Year and Month
        navFrame = ctk.CTkFrame(self.topWindow)
        navFrame.pack(fill="x", pady=10)

        # Year Selector
        years = [str(year) for year in range(1900, 2101)]  # Range of years
        self.yearVar = ctk.StringVar(value=str(self.selectedYear))
        yearMenu = ctk.CTkOptionMenu(navFrame, values=years, variable=self.yearVar, command=self.updateCalendar,
                                     corner_radius=50, fg_color='#00ffc3',button_hover_color='#00ffc3',
                                     button_color='#007860',text_color='#000000')
        yearMenu.pack(side="left", padx=10)

        # Month Selector
        months = list(calendar.month_name)[1:]  # Get month names
        self.monthVar = ctk.StringVar(value=calendar.month_name[self.selectedMonth])
        monthMenu = ctk.CTkOptionMenu(navFrame, values=months, variable=self.monthVar, command=self.updateCalendar,
                                      corner_radius=50, fg_color='#00ffc3',button_hover_color='#00ffc3',
                                      button_color='#007860',text_color='#000000')
        monthMenu.pack(side="left", padx=10)

        # Calendar Frame
        self.calendarFrame = ctk.CTkFrame(self.topWindow)
        self.calendarFrame.pack(fill="both", expand=True, padx=10, pady=10)

        self.loadCalendar(self.selectedYear, self.selectedMonth)

    def updateCalendar(self, _=None):
        """Update the calendar when the year or month changes."""
        year = int(self.yearVar.get())
        month = list(calendar.month_name).index(self.monthVar.get())
        self.selectedYear = year
        self.selectedMonth = month
        self.loadCalendar(year, month)

    def loadCalendar(self, year, month):
        """Load the calendar for the given year and month."""
        # Clear previous calendar
        for widget in self.calendarFrame.winfo_children():
            widget.destroy()

        # Display the days of the week
        days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for col, day in enumerate(days_of_week):
            dayLabel = ctk.CTkLabel(self.calendarFrame, text=day, width=50, height=30)
            dayLabel.grid(row=0, column=col, padx=5, pady=5)

        # Display the days of the month
        days = calendar.monthcalendar(year, month)
        for row, week in enumerate(days, start=1):
            for col, day in enumerate(week):
                if day != 0:  # Skip blank days
                    dayButton = ctk.CTkButton(
                        self.calendarFrame,
                        text=str(day),
                        command=lambda d=day: self.setDate(year, month, d),
                        width=50,
                        height=30,
                        corner_radius=50,
                        text_color='#000000',
                        hover_color='#007860',
                        border_width=1,
                        fg_color='#00ffc3'
                    )
                    dayButton.grid(row=row, column=col, padx=5, pady=5)

    def setDate(self, year, month, day):
        """Set the selected date in the entry widget."""
        self.entryWidget.set(f"{year}-{month:02d}-{day:02d}")
        self.topWindow.destroy()
