import sys
from concurrent.futures import Future
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget
import pandas as pd

from worker import ReturnProcess, ThreadPoolExecutor_global,ProcessPoolExecutor_global
# Hàm xử lý nặng (chạy trong process pool)
class MainWindow(QMainWindow):
    n = 0
    def __init__(self):
        super().__init__()
        "Khởi tạo ProcessPoolExecutor và ThreadPoolExecutor toàn cục"
        ProcessPoolExecutor_global.submit(print, "start process")
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("ProcessPoolExecutor Example")
        self.setGeometry(100, 100, 400, 200)
        self.label = QLabel("Click Start to run task", self)
        self.btn_start = QPushButton("Start Task", self)
        self.btn_start.clicked.connect(self.start_task)
        
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.btn_start)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.n = 0
        
    @classmethod
    def heavy_task(cls):
        df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        cls.n +=1
        # print("check ",cls.n)
        data = df.to_dict()
        df = pd.DataFrame.from_dict(data=data)
        return df 
    
    def start_task(self):
        print("self ",self.n)
        self.label.setText("Processing...")
        self.executor = ReturnProcess(self.heavy_task)
        self.executor.update_signal.connect(self.update_label)
        self.executor.finished_signal.connect(self.task_finished)
        self.executor.start()
        
    def update_label(self, future: Future):
        print(future,type(future))
        self.label.setText(str(future))

    def task_finished(self):
        self.btn_start.setEnabled(True)
        # self.label.setText("Task completed!")

    def closeEvent(self, event):
        self.executor.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())