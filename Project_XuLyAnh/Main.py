# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer
import cv2

class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('MainWindow.ui', self)  

        # Khởi tạo camera
        self.capture = cv2.VideoCapture(0)  # 0 là ID camera mặc định
        if not self.capture.isOpened():
            print("Không thể mở camera!")
            exit()
        
        # Tạo timer để đọc khung hình
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Cập nhật mỗi 30ms

        # Gán QLabel hiển thị video
        self.videoLabel = self.findChild(QtWidgets.QLabel, "videoLabel")

    def update_frame(self):
        ret, frame = self.capture.read()
        if ret:
            # Chuyển đổi khung hình từ BGR sang RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Chuyển đổi khung hình thành QImage
            height, width, channel = rgb_frame.shape
            step = channel * width
            qImg = QImage(rgb_frame.data, width, height, step, QImage.Format_RGB888)
            
            # Hiển thị hình ảnh trong QLabel
            self.videoLabel.setPixmap(QPixmap.fromImage(qImg))
            self.videoLabel.setScaledContents(True)  # Đảm bảo video vừa khít trong QLabel

    def closeEvent(self, event):
        # Dừng camera khi đóng cửa sổ
        self.timer.stop()
        self.capture.release()
        cv2.destroyAllWindows()
        event.accept()

import logoTruong_rc
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = Ui_MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())
