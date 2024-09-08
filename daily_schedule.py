import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from database import Database
from plyer import notification

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

        # self.time_labels = [] # time_label：显示每小时的时间（例如00:00、01:00等）。
        # self.schedule_entries = [] # schedule_entry：对应每个小时的任务输入框，用户可以在这里输入任务。

        # for hour in range(24):
        #     time_label = tk.Label(self.schedule_frame, text=f"{hour:02}:00")
        #     time_label.grid(row=hour, column=0, padx=5, pady=5)

        #     schedule_entry = tk.Entry(self.schedule_frame, width=50)
        #     schedule_entry.grid(row=hour, column=1, padx=5, pady=5)
                    
        #     self.time_labels.append(time_label)
        #     self.schedule_entries.append(schedule_entry)

        self.schedule_list = tk.Listbox(self.schedule_frame)  # 使用Listbox显示日程
        self.schedule_list.pack(side="left", fill="both", expand=True)

        self.sidebar_frame = tk.Frame(self)
        self.sidebar_frame.pack(side="right", fill="y")
    
        self.add_button = tk.Button(self.sidebar_frame, text="增加", command=self.add_schedule)
        self.add_button.pack(side="top", padx=5, pady=5)

        self.delete_button = tk.Button(self.sidebar_frame, text="删除", command=self.enable_delete_mode)
        self.delete_button.pack(side="top", padx=5, pady=5)

        # # 备忘录区域
        # self.memo_frame = tk.Frame(self) # memo_frame：底部框架，包含备忘录输入框和保存按钮。
        # self.memo_frame.pack(side="bottom", fill="x")

        # self.memo_label = tk.Label(self.memo_frame, text="备忘录:") # memo_label：显示“备忘录”标签。
        # self.memo_label.pack(side="left", padx=5, pady=5)

        # self.memo_text = tk.Text(self.memo_frame, height=5) # memo_text：多行文本框，用户可以在这里输入备忘内容。
        # self.memo_text.pack(side="left", fill="x", expand=True, padx=5, pady=5)

        # self.save_button = tk.Button(self.memo_frame, text="保存", command=self.save_schedule) # save_button：点击后调用self.save_schedule()，保存当前的日程和备忘录。
        # self.save_button.pack(side="right", padx=5, pady=5)

    # load_schedule() 方法：
    # def load_schedule(self):
    #     date_str = self.selected_date.strftime("%Y-%m-%d")
    #     schedule = self.db.load_schedule(date_str) # 加载日程：调用self.db.load_schedule()从数据库中获取选定日期的日程数据，然后将其填充到对应的时间输入框中。
    #     memo = self.db.load_memo(date_str) # 加载备忘录：调用self.db.load_memo()从数据库中获取选定日期的备忘录，并将其显示在备忘录文本框中。

    #     for hour, entry in enumerate(self.schedule_entries):
    #         entry.delete(0, tk.END)
    #         entry.insert(0, schedule.get(f"{hour:02}:00", ""))

    #     self.memo_text.delete("1.0", tk.END)
    #     self.memo_text.insert(tk.END, memo)

    def check_notifications(self):
        current_time = datetime.now().strftime("%H:%M")
        date_str = self.selected_date.strftime("%Y-%m-%d")
        schedule = self.db.load_schedule(date_str)

        for start_hour, start_minute, end_hour, end_minute, task_name, _ in schedule:
            start_time = f"{start_hour:02}:{start_minute:02}"
            end_time = f"{end_hour:02}:{end_minute:02}"

            if start_time == current_time:
                notification.notify(
                    title="任务提醒",
                    message=f"任务 '{task_name}' 已经开始！",
                    timeout=10  # 通知显示的时间
                )

            if end_time == current_time:
                notification.notify(
                    title="任务提醒",
                    message=f"任务 '{task_name}' 已经结束！",
                    timeout=10
                )

    def load_schedule(self):
        date_str = self.selected_date.strftime("%Y-%m-%d")
        schedule = self.db.load_schedule(date_str)

        self.schedule_list.delete(0, tk.END)
        for start_hour, start_minute, end_hour, end_minute, task_name, _ in schedule:
            start_time = f"{start_hour:02}:{start_minute:02}"
            end_time = f"{end_hour:02}:{end_minute:02}"
            self.schedule_list.insert(tk.END, f"{start_time}-{end_time} - {task_name}")

        self.check_notifications()  # 加载日程后检查通知
    
    def add_schedule(self):
        add_window = tk.Toplevel(self)
        add_window.title("增加日程")

        tk.Label(add_window, text="日程名称:").grid(row=0, column=0, padx=5, pady=5)
        task_name_entry = tk.Entry(add_window)
        task_name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(add_window, text="开始时间 (HH:MM):").grid(row=1, column=0, padx=5, pady=5)
        start_time_entry = tk.Entry(add_window)
        start_time_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(add_window, text="结束时间 (HH:MM):").grid(row=2, column=0, padx=5, pady=5)
        end_time_entry = tk.Entry(add_window)
        end_time_entry.grid(row=2, column=1, padx=5, pady=5)

        def save_new_schedule():
            task_name = task_name_entry.get()
            start_time = start_time_entry.get().split(':')
            end_time = end_time_entry.get().split(':')

            if task_name and len(start_time) == 2 and len(end_time) == 2:
                start_hour, start_minute = int(start_time[0]), int(start_time[1])
                end_hour, end_minute = int(end_time[0]), int(end_time[1])

                self.db.save_schedule(
                    self.selected_date.strftime("%Y-%m-%d"),
                    start_hour, start_minute, 
                    end_hour, end_minute, 
                    task_name
                )
                self.load_schedule()
                add_window.destroy()

        save_button = tk.Button(add_window, text="保存", command=save_new_schedule)
        save_button.grid(row=3, columnspan=2, pady=5)


    def enable_delete_mode(self):
        self.schedule_list.delete(0, tk.END)
        date_str = self.selected_date.strftime("%Y-%m-%d")
        self.delete_mode = True

        schedule = self.db.load_schedule(date_str)

        for start_hour, start_minute, end_hour, end_minute, task_name, _ in schedule:
            start_time = f"{start_hour:02}:{start_minute:02}"
            end_time = f"{end_hour:02}:{end_minute:02}"
            task_str = f"{start_time}-{end_time} - {task_name} [x]"
            self.schedule_list.insert(tk.END, task_str)
    
        self.schedule_list.bind('<ButtonRelease-1>', self.delete_task)

    def delete_task(self, event):
        selected = self.schedule_list.get(tk.ACTIVE)
        if self.delete_mode and "[x]" in selected:
            result = messagebox.askyesno("删除确认", "你确定要删除这个日程吗？")
            if result:
                time_range = selected.split(' - ')[0]  # 解析时间段
                start_time = time_range.split('-')[0]
                start_hour, start_minute = map(int, start_time.split(':'))

                self.db.delete_schedule(
                    self.selected_date.strftime("%Y-%m-%d"), 
                    start_hour, start_minute
                )
                self.delete_mode = False
                self.load_schedule()

    def __del__(self):
        self.db.close()
