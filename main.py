# main.py
from PySide6.QtWidgets import QApplication, QMainWindow
from views.main_page import MainPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 获取屏幕尺寸
        screen_geometry = QApplication.primaryScreen().geometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        # 设置窗口大小为屏幕的 70% 宽和 70% 高
        self.resize(int(screen_width * 0.7), int(screen_height * 0.7))

        # 设置中央布局
        self.main_page = MainPage()
        self.setCentralWidget(self.main_page)

        # 设置窗口标题
        self.setWindowTitle("To-Do App")

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
