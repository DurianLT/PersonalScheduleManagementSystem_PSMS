# 导入必要的模块
import tkinter as tk # tkinter：Python的标准GUI库，用于创建图形用户界面。
from PIL import Image, ImageTk
from calendar_view import CalendarView # CalendarView：自定义模块，管理日历视图，允许用户选择一个具体日期。
from daily_schedule import DailySchedule # DailySchedule：自定义模块，管理每日的详细日程和备忘录。

## 定义ScheduleApp类
# # ScheduleApp类是整个应用程序的核心，负责管理视图之间的切换和应用程序的初始化。
class ScheduleApp:
    # __init__ 方法：
    def __init__(self, root):
        self.root = root # self.root：传入的Tk根窗口对象，用于创建和管理整个应用的主窗口。
        self.root.title("日程管理系统") # self.root.title("日程管理系统")：设置窗口标题为“日程管理系统”。

         # Remove the default title bar
        self.root.overrideredirect(True)

        # 设置窗口大小
        window_width = 800
        window_height = 600
        
        # 获取屏幕宽高
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # 计算窗口位于屏幕中央的坐标
        position_x = (screen_width // 2) - (window_width // 2)
        position_y = (screen_height // 2) - (window_height // 2)
        
        # 设置窗口的位置和大小
        self.root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

        # Create a frame to hold the custom title bar and the calendar
        self.main_frame = tk.Frame(self.root)
        self.main_frame.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)

        # 自定义上边栏
        self.create_title_bar()

        # 加载并设置背景图片
        self.set_background_image("background.jpg")

        # Add the calendar view
        self.calendar_view = CalendarView(self.main_frame, self.show_daily_schedule) # self.calendar_view：实例化CalendarView对象，传入根窗口self.root和一个回调函数self.show_daily_schedule。这个回调函数用于当用户选择日期时切换到每日视图。
        self.calendar_view.pack(fill="both", expand=True) # self.calendar_view.pack(fill="both", expand=True)：将日历视图布局到窗口中，并设置它在窗口大小变化时自动扩展。

    
    def create_title_bar(self):
        # 创建一个自定义标题栏，并放置在最顶层
        self.title_bar = tk.Frame(self.root, bg="gray", relief="raised", bd=2)
        self.title_bar.place(relwidth=1, relheight=0.1)
        
        # 使窗口可以通过拖拽上边栏移动
        self.title_bar.bind("<ButtonPress-1>", self.start_move)
        self.title_bar.bind("<B1-Motion>", self.on_move)

        # 设置按钮
        self.settings_button = tk.Button(self.title_bar, text="⚙️", command=self.open_settings)
        self.settings_button.pack(side="left", padx=5)

        # 窗口标题
        self.title_label = tk.Label(self.title_bar, text="日程管理系统", bg="gray", fg="white")
        self.title_label.pack(side="left", padx=5)
        
        # 最小化按钮
        self.minimize_button = tk.Button(self.title_bar, text="_", command=self.minimize_window)
        self.minimize_button.pack(side="right", padx=5)
        
        # 关闭按钮
        self.close_button = tk.Button(self.title_bar, text="X", command=self.root.quit)
        self.close_button.pack(side="right", padx=5)
    
    def set_background_image(self, image_path):
        # 设置背景图片，确保其他控件放置在背景图片上方
        self.bg_image = Image.open(image_path)
        self.bg_image = self.bg_image.resize((800, 600), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        
        # 将背景图片放置在最底层
        self.background_label = tk.Label(self.root, image=self.bg_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # 确保背景图片在最底层，其他控件不被覆盖
        self.background_label.lower()

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def on_move(self, event):
        x = event.x_root - self.x
        y = event.y_root - self.y
        self.root.geometry(f"+{x}+{y}")
    
    def minimize_window(self):
        self.root.iconify()

    def open_settings(self):
        # 暂时不实现设置功能
        pass
    
    # show_daily_schedule 方法：当用户在日历视图中选择一个日期时，调用此方法。
    def show_daily_schedule(self, date):
        self.calendar_view.pack_forget() # self.calendar_view.pack_forget()：隐藏日历视图。
        self.daily_schedule = DailySchedule(self.main_frame, date, self.show_calendar) # self.daily_schedule：实例化DailySchedule对象，传入根窗口self.root、选择的日期date、以及一个回调函数self.show_calendar。这个回调函数用于当用户在每日视图中点击返回按钮时，切换回日历视图。
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
