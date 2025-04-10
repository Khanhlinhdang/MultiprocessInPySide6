# Multiprocess and MultiThread In Python/PySide6

The way to use multiprocess in pyside6 project

- Worker sử dụng QThead xử lý tiến trình nặng, hoặc tác vụ nền chạy ngầm nhẹ.
- Worker sử dụng QRunable và quản lý bởi QThreadPool , xử lý các tiến trình nhẹ
- Worker sử dụng Coroutine cho các hàm I/O
- Worker sử dụng `ThreadPoolExecutor quản lý các tiến trình nhẹ, vì nếu chạy nhiều task nó vẫn ảnh hưởng đến main_thread gây lag/chậm bởi cơ chế GIL của python`
- Worker sử dụng `ProcessPoolExecutor `quản lý các tiến trình nặng về tính toán, không gây ảnh hưởng đến main_thread tuy nhiên nếu đắt max_worker lớn thì ảnh hưởng đến CPU``
- Chú ý hàm

  `from worker.return_worker import HeavyProcess`

  `from worker.return_worker import ReturnProcess`

  dùng thể xử lý kết quả trả về của hàm `self.fn = fn` bằng hàm `self.callback = callback`

Dự án sử dụng:

ATK: [AutoTradingKit(ATK)](https://www.facebook.com/groups/748831980507126)

Github: [ATK](https://github.com/Khanhlinhdang/AutoTradingKit)
