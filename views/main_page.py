from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSplitter, QInputDialog
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QListWidgetItem, QSplitter, QLabel, QFrame
from PySide6.QtCore import Qt

class MainPage(QWidget):
    def __init__(self):
        super().__init__()

        # 创建主布局 - 水平分割
        main_layout = QHBoxLayout(self)

        # 设置整个布局的外边距（左，上，右，下）
        main_layout.setContentsMargins(10, 20, 10, 10)  # 调整上边距为20

        # 使用 QSplitter 来实现可调整大小的左右布局
        splitter = QSplitter(Qt.Horizontal)

        # 左边栏
        self.sidebar = LeftSidebar()
        splitter.addWidget(self.sidebar)

        # 中间内容区
        self.main_content = MainContent()
        splitter.addWidget(self.main_content)

        # 右边栏（可折叠）
        self.right_sidebar = RightSidebar()
        splitter.addWidget(self.right_sidebar)

        # 设置左右栏的宽度比
        splitter.setStretchFactor(0, 1)  # 左边栏相对较小
        splitter.setStretchFactor(1, 8)  # 中间内容显示区较大
        splitter.setStretchFactor(2, 1)  # 右边栏初始大小

        main_layout.addWidget(splitter)
        self.setLayout(main_layout)

class LeftSidebar(QWidget):
    def __init__(self):
        super().__init__()
        left_layout = QVBoxLayout()

        # 功能列表
        self.function_list = QListWidget()
        task_item = QListWidgetItem("任务栏")
        self.function_list.addItem(task_item)
        left_layout.addWidget(self.function_list)

        # 设置按钮
        self.settings_button = QPushButton("设置")
        self.settings_button.clicked.connect(self.open_settings)
        left_layout.addWidget(self.settings_button)

        # 设置布局
        self.setLayout(left_layout)

    def open_settings(self):
        new_function_name, ok = QInputDialog.getText(self, '添加功能', '输入功能名称:')
        if ok and new_function_name:
            new_item = QListWidgetItem(new_function_name)
            self.function_list.addItem(new_item)
            # 保存到数据库或JSON
            self.save_function_order()

    def save_function_order(self):
        # 保存功能列表顺序的逻辑
        pass

class MainContent(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # 示例中间内容
        label = QLabel("Main Content Area")
        label.setFrameStyle(QFrame.StyledPanel)
        layout.addWidget(label)

        self.setLayout(layout)

class RightSidebar(QWidget):
    def __init__(self):
        super().__init__()
        right_layout = QVBoxLayout()

        # 示例右侧内容
        right_label = QLabel("Right Sidebar (Collapsible)")
        right_layout.addWidget(right_label)

        self.setLayout(right_layout)

