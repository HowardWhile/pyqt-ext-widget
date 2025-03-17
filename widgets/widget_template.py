from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QTimer
from PySide6.QtCore import Signal
import os


class extWidget(QWidget):
    message_signal = Signal(str)  # 用於傳遞訊息給其他插件
    
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent

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

    def __del__(self):
        """解構函式"""
        print(f"{self.name} 正在被銷毀")
        if self.timer.isActive():
            self.timer.stop()
            print(f"{self.name} 的計時器已停止")
