import serial
import serial.tools.list_ports

class SerialPort:
    def __init__(self, port, baud_rate=9600):
        """Khởi tạo SerialPort với tốc độ baud mặc định."""
        self.port = port
        self.baud_rate = baud_rate
        self.serial_connection = None

    def setPort(self,port):
        self.port=port

    def list_serial_ports(self):
        """Liệt kê tất cả các cổng serial hiện có."""
        ports = serial.tools.list_ports.comports()
        available_ports = [port.device for port in ports]
        return available_ports

    def connect(self):
        """Kết nối tới một cổng serial."""
        try:
            self.serial_connection = serial.Serial(self.port, self.baud_rate, timeout=1)
            print(f"Kết nối thành công tới {self.port} với baud rate {self.baud_rate}.")
        except serial.SerialException as e:
            print(f"Lỗi: Không thể kết nối tới {self.port}. Chi tiết: {e}")
            self.serial_connection = None

    def send_data(self, data):
        """Gửi dữ liệu qua cổng serial."""
        if not self.serial_connection or not self.serial_connection.is_open:
            print("Lỗi: Chưa kết nối tới cổng serial.")
            return

        try:
            # Gửi dữ liệu
            self.serial_connection.write(data.encode('utf-8'))
            print(f"Dữ liệu đã gửi: {data}")
        except serial.SerialException as e:
            print(f"Lỗi khi gửi dữ liệu: {e}")

    def read_data(self):
        """Đọc và hiển thị dữ liệu từ cổng serial."""
        if not self.serial_connection or not self.serial_connection.is_open:
            print("Lỗi: Chưa kết nối tới cổng serial.")
            return

        try:
            print("Đang đọc dữ liệu từ cổng serial. Nhấn Ctrl+C để dừng.")
            while True:
                # Đọc dữ liệu từ cổng serial
                data = self.serial_connection.readline().decode('utf-8').strip()
                if data:
                    print(f"Dữ liệu nhận được: {data}")
        except KeyboardInterrupt:
            print("\nDừng đọc dữ liệu.")
        except serial.SerialException as e:
            print(f"Lỗi khi đọc dữ liệu: {e}")

    def disconnect(self):
        """Ngắt kết nối khỏi cổng serial."""
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
            print("Đã ngắt kết nối khỏi cổng serial.")
        else:
            print("Lỗi: Không có kết nối để ngắt.")