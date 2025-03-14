from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QTimer
import os


class extWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.name = os.path.basename(__file__)
        layout = QVBoxLayout(self)
        label = QLabel(f"我是 {self.name} 產生的 extWidget")
        layout.addWidget(label)

        label = QLabel(f"")
        self.dtxt = label
        layout.addWidget(label)

        # 設定 QTimer，每秒觸發一次 update_label
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_label)
        self.timer.start(1000)  # 設定為 1000 毫秒（1 秒）
        self.count = 0  # 計數器

    def update_label(self):
        """更新標籤內容，每秒觸發一次"""
        self.count += 1
        msg = f"{self.name} 更新次數: {self.count}"
        print(msg)
        self.dtxt.setText(msg)
