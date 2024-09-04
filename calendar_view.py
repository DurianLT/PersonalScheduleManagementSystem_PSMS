import tkinter as tk
import calendar
from datetime import datetime

class CalendarView(tk.Frame):
    def __init__(self, master, on_date_selected):
        super().__init__(master)
        self.master = master
        self.on_date_selected = on_date_selected
        self.current_year = datetime.now().year
        self.current_month = datetime.now().month
        
        self.create_widgets()
        self.show_calendar(self.current_year, self.current_month)
    
    def create_widgets(self):
        # 上方的年份和月份选择区域
        self.header_frame = tk.Frame(self)
        self.header_frame.pack(side="top", fill="x")

        self.prev_month_button = tk.Button(self.header_frame, text="<", command=self.prev_month)
        self.prev_month_button.pack(side="left")

        self.month_label = tk.Label(self.header_frame, text="")
        self.month_label.pack(side="left", expand=True)

        self.next_month_button = tk.Button(self.header_frame, text=">", command=self.next_month)
        self.next_month_button.pack(side="right")
        
        # 显示日期的区域
        self.days_frame = tk.Frame(self)
        self.days_frame.pack(side="top", fill="both", expand=True)
        
    def show_calendar(self, year, month):
        # 清空之前的日历
        for widget in self.days_frame.winfo_children():
            widget.destroy()
        
        # 更新月份标签
        self.month_label.config(text=f"{year}年 {month}月")
        
        # 获取当前月份的天数和第一天是星期几
        cal = calendar.monthcalendar(year, month)
        
        # 显示星期行
        days_of_week = ["日", "一", "二", "三", "四", "五", "六"]
        for day in days_of_week:
            tk.Label(self.days_frame, text=day).grid(row=0, column=days_of_week.index(day))
        
        # 显示日期
        for week in cal:
            for day in week:
                if day == 0:
                    label = tk.Label(self.days_frame, text="")
                else:
                    label = tk.Button(self.days_frame, text=str(day), command=lambda d=day: self.select_date(d))
                label.grid(row=cal.index(week) + 1, column=week.index(day))
    
    def select_date(self, day):
        selected_date = datetime(self.current_year, self.current_month, day)
        self.on_date_selected(selected_date)
    
    def prev_month(self):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.show_calendar(self.current_year, self.current_month)
    
    def next_month(self):
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.show_calendar(self.current_year, self.current_month)
