from PySide6.QtCore import QThread, Signal, Qt, QTimer
from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QPushButton, QHBoxLayout

class WidgetLoader(QThread):
    """Thread xử lý dữ liệu cho từng widget"""
    result_signal = Signal(int, str)  # Gửi dữ liệu về main thread (index, data)

    def __init__(self, index):
        super().__init__()
        self.index = index  # Mỗi thread xử lý một widget riêng

    def run(self):
        import time
        # time.sleep(2)  # Giả lập thời gian load dữ liệu
        data = f"Widget {self.index} Loaded"
        self.result_signal.emit(self.index, data)

class Page(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Optimized Page Rendering")
        self.setGeometry(100, 100, 500, 300)

        self.layout = QVBoxLayout(self)

        # Nút load trang
        self.button = QPushButton("Load Page")
        self.button.clicked.connect(self.load_page)
        self.layout.addWidget(self.button)

        # Placeholder widgets
        self.widgets = []
        for i in range(10):  # Giả sử trang có 10 widgets
            placeholder = QLabel(f"Loading Widget {i}...")  # Hiển thị placeholder trước
            placeholder.setStyleSheet("font-size: 14px; color: gray;")
            self.widgets.append(placeholder)
            self.layout.addWidget(placeholder)

    def load_page(self):
        self.button.setEnabled(False)  # Disable nút trong khi đang tải

        self.threads = []
        for i in range(10):  # Tạo 10 thread để load dữ liệu cho 10 widget
            thread = WidgetLoader(i)
            thread.result_signal.connect(self.update_widget)
            self.threads.append(thread)

        # Khởi động từng thread với delay nhỏ để UI không bị đơ
        for i, thread in enumerate(self.threads):
            QTimer.singleShot(i * 100, thread.start)  # Delay 100ms mỗi widget để load dần

    def update_widget(self, index, data):
        """Cập nhật widget khi dữ liệu đã sẵn sàng"""
       
        
        self.widgets[index].setText(data)
        self.widgets[index].setStyleSheet("font-size: 16px; color: green; font-weight: bold;")

        # Kiểm tra nếu tất cả widget đã load xong thì enable lại nút
        if all("Loaded" in w.text() for w in self.widgets):
            self.button.setEnabled(True)

if __name__ == "__main__":
    app = QApplication([])
    window = Page()
    window.show()
    app.exec()
