import tkinter as tk
from calendar_view import CalendarView
from daily_schedule import DailySchedule

class ScheduleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("日程管理系统")
        self.root.geometry("800x600")
        
        self.calendar_view = CalendarView(self.root, self.show_daily_schedule)
        self.calendar_view.pack(fill="both", expand=True)
        
    def show_daily_schedule(self, date):
        self.calendar_view.pack_forget()
        self.daily_schedule = DailySchedule(self.root, date, self.show_calendar)
        self.daily_schedule.pack(fill="both", expand=True)
        
    def show_calendar(self):
        self.daily_schedule.pack_forget()
        self.calendar_view.pack(fill="both", expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = ScheduleApp(root)
    root.mainloop()
