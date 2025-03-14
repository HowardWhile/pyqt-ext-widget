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

        # **按鈕 1：更新父容器標題**
        self.btn_update_title = QPushButton("更新父容器標題")
        self.btn_update_title.clicked.connect(self.update_parent_title)
        layout.addWidget(self.btn_update_title)

        # **按鈕 2：傳遞訊息給其他插件**
        self.btn_send_message = QPushButton("傳遞訊息給其他插件")
        self.btn_send_message.clicked.connect(self.send_message)
        layout.addWidget(self.btn_send_message)

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

    def update_parent_title(self):
        """更新父容器 (MainWindows) 的標題"""
        if self.parent:
            new_title = f"{self.name} - 更新次數: {self.count}"
            self.parent.setWindowTitle(new_title)
            print(f"父容器標題已更新為: {new_title}")

    def send_message(self):
        """傳遞訊息給其他插件"""
        message = f"{self.name} 傳送了一條訊息！"
        self.message_signal.emit(message)
        print(f"發送訊息: {message}")
