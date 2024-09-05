import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from database import Database

## DailySchedule类
## 负责创建每日的日程视图，管理任务的显示、保存和加载。
class DailySchedule(tk.Frame):
    # __init__ 方法：
    def __init__(self, master, selected_date, on_back_to_calendar):
        super().__init__(master)
        self.master = master # self.master：传入的Tkinter主窗口对象。
        self.selected_date = selected_date # self.selected_date：用户从日历视图中选择的日期，作为当前日程的日期。
        self.on_back_to_calendar = on_back_to_calendar # self.on_back_to_calendar：回调函数，当用户点击返回按钮时调用，用于切换回日历视图。
        self.db = Database() # self.db：实例化Database类，用于与数据库交互。

        self.create_widgets() # self.create_widgets()：创建UI组件。
        self.load_schedule()  # self.load_schedule()：加载数据库中的日程和备忘录数据。

    # 创建UI组件
    def create_widgets(self):
        # 标题和返回按钮
        # header_frame：顶部框架，包含返回按钮和当前日期标签。
        self.header_frame = tk.Frame(self) 
        self.header_frame.pack(side="top", fill="x")
        
        # back_button：点击后调用self.on_back_to_calendar，返回日历视图。
        self.back_button = tk.Button(self.header_frame, text="返回", command=self.on_back_to_calendar)
        self.back_button.pack(side="left")
        
        # date_label：显示当前选定的日期。
        self.date_label = tk.Label(self.header_frame, text=self.selected_date.strftime("%Y-%m-%d"))
        self.date_label.pack(side="right", expand=True)

        # 日程安排区域
        self.schedule_frame = tk.Frame(self)# schedule_frame：显示每日日程的主框架，包含时间标签和任务输入框。
        self.schedule_frame.pack(side="top", fill="both", expand=True)
        
        self.time_labels = [] # time_label：显示每小时的时间（例如00:00、01:00等）。
        self.schedule_entries = [] # schedule_entry：对应每个小时的任务输入框，用户可以在这里输入任务。

        for hour in range(24):
            time_label = tk.Label(self.schedule_frame, text=f"{hour:02}:00")
            time_label.grid(row=hour, column=0, padx=5, pady=5)

            schedule_entry = tk.Entry(self.schedule_frame, width=50)
            schedule_entry.grid(row=hour, column=1, padx=5, pady=5)
            
            self.time_labels.append(time_label)
            self.schedule_entries.append(schedule_entry)
        
        # 备忘录区域
        self.memo_frame = tk.Frame(self) # memo_frame：底部框架，包含备忘录输入框和保存按钮。
        self.memo_frame.pack(side="bottom", fill="x")

        self.memo_label = tk.Label(self.memo_frame, text="备忘录:") # memo_label：显示“备忘录”标签。
        self.memo_label.pack(side="left", padx=5, pady=5)

        self.memo_text = tk.Text(self.memo_frame, height=5) # memo_text：多行文本框，用户可以在这里输入备忘内容。
        self.memo_text.pack(side="left", fill="x", expand=True, padx=5, pady=5)

        self.save_button = tk.Button(self.memo_frame, text="保存", command=self.save_schedule) # save_button：点击后调用self.save_schedule()，保存当前的日程和备忘录。
        self.save_button.pack(side="right", padx=5, pady=5)

    # save_schedule() 方法：
    def save_schedule(self):
        date_str = self.selected_date.strftime("%Y-%m-%d") # date_str：将selected_date转换为字符串格式的日期（如2024-09-04）。
        # 保存日程：遍历self.schedule_entries中的每个任务输入框，获取用户输入的任务内容。如果内容非空，则调用self.db.save_schedule()将任务保存到数据库中。
        for hour, entry in enumerate(self.schedule_entries):
            task = entry.get()
            if task:
                self.db.save_schedule(date_str, f"{hour:02}:00", task)

        memo = self.memo_text.get("1.0", tk.END).strip()
        if memo:
            self.db.save_memo(date_str, memo) # 保存备忘录：获取备忘录文本框中的内容，如果非空，则调用self.db.save_memo()将其保存到数据库中。

        messagebox.showinfo("保存成功", "日程和备忘录已保存")# 显示消息框：保存成功后，弹出提示框通知用户。

    # load_schedule() 方法：
    def load_schedule(self):
        date_str = self.selected_date.strftime("%Y-%m-%d")
        schedule = self.db.load_schedule(date_str) # 加载日程：调用self.db.load_schedule()从数据库中获取选定日期的日程数据，然后将其填充到对应的时间输入框中。
        memo = self.db.load_memo(date_str) # 加载备忘录：调用self.db.load_memo()从数据库中获取选定日期的备忘录，并将其显示在备忘录文本框中。

        for hour, entry in enumerate(self.schedule_entries):
            entry.delete(0, tk.END)
            entry.insert(0, schedule.get(f"{hour:02}:00", ""))

        self.memo_text.delete("1.0", tk.END)
        self.memo_text.insert(tk.END, memo)

    # __del__() 方法：析构方法，在对象被销毁时调用。这里用于关闭数据库连接，确保资源得到正确释放。
    def __del__(self):
        self.db.close()
