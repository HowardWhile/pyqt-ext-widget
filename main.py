import os
import sys
import importlib.util
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QGroupBox,
    QPushButton,
    QComboBox,
    QHBoxLayout,
    QStackedWidget,
)


class MainWindows(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("動態 Widget 加載器")
        self.setGeometry(100, 100, 500, 500)

        # 主視窗 Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # 建立上方選單與按鈕區域
        top_layout = QHBoxLayout()
        self.widget_selector = QComboBox()
        self.load_button = QPushButton("重新載入")
        self.test_button = QPushButton("測試按鈕")

        top_layout.addWidget(self.widget_selector)
        top_layout.addWidget(self.load_button)
        top_layout.addWidget(self.test_button)

        # 建立 GroupBox
        self.group_box = QGroupBox("Widget 容器")
        group_layout = QVBoxLayout()

        # self.widget_container = QWidget()
        # group_layout.addWidget(self.widget_container)
        # self.group_box.setLayout(group_layout)

        # 使用 QStackedWidget 儲存所有 widgets
        self.widget_container = QStackedWidget()
        group_layout.addWidget(self.widget_container)
        self.group_box.setLayout(group_layout)

        # 加入 Layout
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.group_box)

        # 事件綁定
        self.load_button.clicked.connect(self.load_widgets)
        self.widget_selector.currentIndexChanged.connect(self.switch_widget)

        # 變數儲存動態加載的 widgets
        self.loaded_widgets = {}

        # 初次載入 widgets
        self.load_widgets()

    def load_widgets(self):
        """載入 ./widgets 目錄下的所有 Python 檔案"""
        widget_dir = "./widgets"
        self.loaded_widgets.clear()
        self.widget_selector.clear()

        if not os.path.exists(widget_dir):
            os.makedirs(widget_dir)  # 如果資料夾不存在則建立
            return

        for file in os.listdir(widget_dir):
            if file.endswith(".py") and not file.startswith("_"):
                module_name = file[:-3]
                module_path = os.path.join(widget_dir, file)

                spec = importlib.util.spec_from_file_location(module_name, module_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                if hasattr(module, "extWidget"):
                    widget_instance = module.extWidget()  # 建立 Widget 實例
                    self.loaded_widgets[module_name] = (
                        module.extWidget
                    )  # 插件都要有名為extWidget的class
                    self.widget_container.addWidget(
                        widget_instance
                    )  # 加入 QStackedWidget
                    self.widget_selector.addItem(module_name)

    def switch_widget(self):
        """切換顯示的 Widget"""
        selected_widget_name = self.widget_selector.currentText()

        if selected_widget_name in self.loaded_widgets:
            """切換顯示的 Widget，但所有 Widget 都會持續運行"""
            selected_index = self.widget_selector.currentIndex()
            if selected_index >= 0:
                self.widget_container.setCurrentIndex(selected_index)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindows()
    window.show()
    sys.exit(app.exec())
