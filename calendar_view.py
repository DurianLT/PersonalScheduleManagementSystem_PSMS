# 导入必要的模块
import tkinter as tk # Python的标准GUI库，用于创建图形用户界面。
import calendar # Python的内置模块，用于处理日历相关的功能，如获取某月的天数和第一天是星期几。
from datetime import datetime # 用于处理日期和时间的模块，这里主要用于获取当前的年份和月份。

## CalendarView类
# # CalendarView类是日历视图的核心，它继承自tk.Frame，这使它成为一个可以放置在Tkinter窗口中的组件
class CalendarView(tk.Frame):
    # __init__ 方法：
    def __init__(self, master, on_date_selected):
        super().__init__(master) 
        self.master = master # self.master：传入的Tkinter主窗口对象，用于将日历视图嵌入其中
        self.on_date_selected = on_date_selected # self.on_date_selected：这是一个回调函数，当用户选择日期时调用，用于切换到每日视图。
        self.current_year = datetime.now().year # self.current_year 和 self.current_month：获取当前的年份和月份，初始时显示当前月的日历。
        self.current_month = datetime.now().month
        
        self.create_widgets() # self.create_widgets()：创建日历视图的UI组件。
        self.show_calendar(self.current_year, self.current_month) # self.show_calendar()：显示当前年份和月份的日历。
    
    # 创建UI组件
    def create_widgets(self):
        # 上方的年份和月份选择区域
        self.header_frame = tk.Frame(self) # header_frame：这是顶部的一个框架，包含了用于选择月份的按钮和当前月份的标签。
        self.header_frame.pack(side="top", fill="x")

        self.prev_month_button = tk.Button(self.header_frame, text="<", command=self.prev_month) # prev_month_button：显示“<”按钮，点击时切换到前一个月。
        self.prev_month_button.pack(side="left")

        self.month_label = tk.Label(self.header_frame, text="") # month_label：显示当前的年份和月份。
        self.month_label.pack(side="left", expand=True)

        self.next_month_button = tk.Button(self.header_frame, text=">", command=self.next_month) # next_month_button：显示“>”按钮，点击时切换到下一个月。
        self.next_month_button.pack(side="right")
        
        # 显示日期的区域
        self.days_frame = tk.Frame(self) # days_frame：这是显示日历日期的区域，包含了所有的日期按钮和星期行。
        self.days_frame.pack(side="top", fill="both", expand=True)
        
    # show_calendar() 方法：
    def show_calendar(self, year, month):
        # 清空之前的日历 清空日历：使用winfo_children()获取days_frame中的所有子组件并销毁，以清空之前的日历内容。
        for widget in self.days_frame.winfo_children():
            widget.destroy()
        
        # 更新月份标签：更新month_label显示当前的年份和月份。
        self.month_label.config(text=f"{year}年 {month}月")
        
        # 获取当前月份的天数和第一天是星期几 使用calendar.monthcalendar(year, month)获取指定月份的天数和第一天是星期几，这个方法返回一个列表，其中每个子列表代表一周。
        cal = calendar.monthcalendar(year, month)
        
        # 显示星期行 在日历的顶部显示星期几（如日、一、二等）。
        days_of_week = ["日", "一", "二", "三", "四", "五", "六"]
        for day in days_of_week:
            tk.Label(self.days_frame, text=day).grid(row=0, column=days_of_week.index(day))
        
        # 显示日期 遍历cal，为每个非0的日期创建一个按钮，点击后调用self.select_date(d)选择日期。
        for week in cal:
            for day in week:
                if day == 0:
                    label = tk.Label(self.days_frame, text="")
                else:
                    label = tk.Button(self.days_frame, text=str(day), command=lambda d=day: self.select_date(d))
                label.grid(row=cal.index(week) + 1, column=week.index(day))
    
    # select_date() 方法：当用户点击一个日期按钮时调用。
    def select_date(self, day):
        selected_date = datetime(self.current_year, self.current_month, day) # selected_date：将当前的年份、月份和选中的日期组合成一个datetime对象。
        self.on_date_selected(selected_date) # 调用回调函数：self.on_date_selected(selected_date)，这个函数是从main.py中的ScheduleApp类传入的，用于切换到每日视图。
    
    # prev_month()：当用户点击“<”按钮时调用。如果当前月份是1月，则切换到上一年的12月，否则仅切换到上一个月。然后调用show_calendar()重新显示日历
    def prev_month(self):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.show_calendar(self.current_year, self.current_month)
    
    # next_month()：当用户点击“>”按钮时调用。如果当前月份是12月，则切换到下一年的1月，否则仅切换到下一个月。然后调用show_calendar()重新显示日历。
    def next_month(self):
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.show_calendar(self.current_year, self.current_month)
