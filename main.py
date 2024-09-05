# 导入必要的模块
import tkinter as tk # tkinter：Python的标准GUI库，用于创建图形用户界面。
from calendar_view import CalendarView # CalendarView：自定义模块，管理日历视图，允许用户选择一个具体日期。
from daily_schedule import DailySchedule # DailySchedule：自定义模块，管理每日的详细日程和备忘录。

## 定义ScheduleApp类
# # ScheduleApp类是整个应用程序的核心，负责管理视图之间的切换和应用程序的初始化。
class ScheduleApp:
    # __init__ 方法：
    def __init__(self, root):
        self.root = root # self.root：传入的Tk根窗口对象，用于创建和管理整个应用的主窗口。
        self.root.title("日程管理系统") # self.root.title("日程管理系统")：设置窗口标题为“日程管理系统”。
        self.root.geometry("800x600") # self.root.geometry("800x600")：设置窗口大小为800x600像素。
        
        self.calendar_view = CalendarView(self.root, self.show_daily_schedule) # self.calendar_view：实例化CalendarView对象，传入根窗口self.root和一个回调函数self.show_daily_schedule。这个回调函数用于当用户选择日期时切换到每日视图。
        self.calendar_view.pack(fill="both", expand=True) # self.calendar_view.pack(fill="both", expand=True)：将日历视图布局到窗口中，并设置它在窗口大小变化时自动扩展。
    
    # show_daily_schedule 方法：当用户在日历视图中选择一个日期时，调用此方法。
    def show_daily_schedule(self, date):
        self.calendar_view.pack_forget() # self.calendar_view.pack_forget()：隐藏日历视图。
        self.daily_schedule = DailySchedule(self.root, date, self.show_calendar) # self.daily_schedule：实例化DailySchedule对象，传入根窗口self.root、选择的日期date、以及一个回调函数self.show_calendar。这个回调函数用于当用户在每日视图中点击返回按钮时，切换回日历视图。
        self.daily_schedule.pack(fill="both", expand=True) # self.daily_schedule.pack(fill="both", expand=True)：将每日视图布局到窗口中，并设置它在窗口大小变化时自动扩展。
    
    # show_calendar 方法：当用户从每日视图返回到日历视图时，调用此方法。
    def show_calendar(self):
        self.daily_schedule.pack_forget() # self.daily_schedule.pack_forget()：隐藏每日视图。
        self.calendar_view.pack(fill="both", expand=True) # self.calendar_view.pack(fill="both", expand=True)：重新显示日历视图。

# 启动应用程序
if __name__ == "__main__": # if __name__ == "__main__":：确保脚本是作为主程序运行，而不是被导入为模块。
    root = tk.Tk() # root = tk.Tk()：创建根窗口对象root。
    app = ScheduleApp(root) # app = ScheduleApp(root)：实例化ScheduleApp类，启动应用程序。
    root.mainloop() # root.mainloop()：进入Tkinter的事件循环，保持应用程序运行并响应用户输入。
