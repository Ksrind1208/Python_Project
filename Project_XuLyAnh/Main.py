# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer
import cv2
from SerialPort import SerialPort 

class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self, serialport):
        super().__init__()
        loadUi('MainWindow.ui', self)  

        # Initialize SerialPort
        self.serialport = serialport
        print(self.serialport.list_serial_ports())

        # Initialize camera (but don't open yet)
        self.capture = None

        # Create a timer to read frames
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)

        # Find widgets from the UI
        self.videoLabel = self.findChild(QtWidgets.QLabel, "videoLabel")
        self.openCamera = self.findChild(QtWidgets.QPushButton, "openCamera")
        self.closeCamera = self.findChild(QtWidgets.QPushButton, "closeCamera")

        # Connect buttons to functions
        self.openCamera.clicked.connect(self.start_camera)
        self.closeCamera.clicked.connect(self.stop_camera)

    def start_camera(self):
        """Open the camera when the button is clicked."""
        if self.capture is None or not self.capture.isOpened():
            # Open the camera
            self.capture = cv2.VideoCapture("http:192.168.1.238:8080/video")
            if self.capture.isOpened():
                print("Camera opened successfully!")
                self.timer.start(30)  # Update frames every 30ms
            else:
                print("Failed to open the camera.")
        else:
            print("Camera is already open.")

    def stop_camera(self):
        """Close the camera when the button is clicked."""
        if self.capture is not None and self.capture.isOpened():
            self.timer.stop()
            self.capture.release()
            self.videoLabel.clear()  # Clear the QLabel
            print("Camera stopped successfully!")
        else:
            print("Camera is not open.")

    def update_frame(self):
        """Read and display the frame from the camera."""
        if self.capture is not None:
            ret, frame = self.capture.read()
            if ret:
                # Convert the frame from BGR to RGB
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Convert the frame to QImage
                height, width, channel = rgb_frame.shape
                step = channel * width
                qImg = QImage(rgb_frame.data, width, height, step, QImage.Format_RGB888)
                
                # Display the image in the QLabel
                self.videoLabel.setPixmap(QPixmap.fromImage(qImg))
                self.videoLabel.setScaledContents(True)

    def closeEvent(self, event):
        """Clean up when the window is closed."""
        self.stop_camera()
        cv2.destroyAllWindows()
        event.accept()

import logoTruong_rc
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    serialport = SerialPort("COM3", 9600)
    MainWindow = Ui_MainWindow(serialport)
    MainWindow.show()
    sys.exit(app.exec_())
