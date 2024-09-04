import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from database import Database

class DailySchedule(tk.Frame):
    def __init__(self, master, selected_date, on_back_to_calendar):
        super().__init__(master)
        self.master = master
        self.selected_date = selected_date
        self.on_back_to_calendar = on_back_to_calendar
        self.db = Database()

        self.create_widgets()
        self.load_schedule()  # 加载日程和备忘录

    def create_widgets(self):
        # 标题和返回按钮
        self.header_frame = tk.Frame(self)
        self.header_frame.pack(side="top", fill="x")
        
        self.back_button = tk.Button(self.header_frame, text="返回", command=self.on_back_to_calendar)
        self.back_button.pack(side="left")
        
        self.date_label = tk.Label(self.header_frame, text=self.selected_date.strftime("%Y-%m-%d"))
        self.date_label.pack(side="right", expand=True)

        # 日程安排区域
        self.schedule_frame = tk.Frame(self)
        self.schedule_frame.pack(side="top", fill="both", expand=True)
        
        self.time_labels = []
        self.schedule_entries = []

        for hour in range(24):
            time_label = tk.Label(self.schedule_frame, text=f"{hour:02}:00")
            time_label.grid(row=hour, column=0, padx=5, pady=5)

            schedule_entry = tk.Entry(self.schedule_frame, width=50)
            schedule_entry.grid(row=hour, column=1, padx=5, pady=5)
            
            self.time_labels.append(time_label)
            self.schedule_entries.append(schedule_entry)
        
        # 备忘录区域
        self.memo_frame = tk.Frame(self)
        self.memo_frame.pack(side="bottom", fill="x")

        self.memo_label = tk.Label(self.memo_frame, text="备忘录:")
        self.memo_label.pack(side="left", padx=5, pady=5)

        self.memo_text = tk.Text(self.memo_frame, height=5)
        self.memo_text.pack(side="left", fill="x", expand=True, padx=5, pady=5)

        self.save_button = tk.Button(self.memo_frame, text="保存", command=self.save_schedule)
        self.save_button.pack(side="right", padx=5, pady=5)

    def save_schedule(self):
        date_str = self.selected_date.strftime("%Y-%m-%d")
        for hour, entry in enumerate(self.schedule_entries):
            task = entry.get()
            if task:
                self.db.save_schedule(date_str, f"{hour:02}:00", task)

        memo = self.memo_text.get("1.0", tk.END).strip()
        if memo:
            self.db.save_memo(date_str, memo)

        messagebox.showinfo("保存成功", "日程和备忘录已保存")

    def load_schedule(self):
        date_str = self.selected_date.strftime("%Y-%m-%d")
        schedule = self.db.load_schedule(date_str)
        memo = self.db.load_memo(date_str)

        for hour, entry in enumerate(self.schedule_entries):
            entry.delete(0, tk.END)
            entry.insert(0, schedule.get(f"{hour:02}:00", ""))

        self.memo_text.delete("1.0", tk.END)
        self.memo_text.insert(tk.END, memo)

    def __del__(self):
        self.db.close()
