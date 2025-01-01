# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer
import cv2
from SerialPort import SerialPort 
from ultralytics import YOLO
# vinomodel = YOLO('yolov8n_openvino_model')
vinomodel=YOLO('best.pt')

selectedPort=""
selectedMode=""

class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self, serialport, modeList):
        super().__init__()
        loadUi('MainWindow.ui', self)

        # Initialize SerialPort and Mode List
        self.serialport = serialport
        self.modeList = modeList
        if(len(self.serialport.list_serial_ports())!=0):
            selectedPort=self.serialport.list_serial_ports()[0]
        selectedMode=modeList[0]

        # Initialize camera (but don't open yet)
        self.capture = None

        # Create a timer to read frames
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)

        # Find widgets from the UI
        self.videoLabel = self.findChild(QtWidgets.QLabel, "videoLabel")
        self.openCamera = self.findChild(QtWidgets.QPushButton, "openCamera")
        self.closeCamera = self.findChild(QtWidgets.QPushButton, "closeCamera")
        self.serialPort = self.findChild(QtWidgets.QComboBox, "serialPort")
        self.modeSelect = self.findChild(QtWidgets.QComboBox, "modeSelect")
        self.startSystem=self.findChild(QtWidgets.QPushButton,"startSystem")
        self.stopSystem=self.findChild(QtWidgets.QPushButton,"stopSystem")

        # Update serial ports in the QComboBox
        self.update_serial_ports()

        # Update modes in the modeSelect ComboBox
        self.update_mode_select()

        # Connect buttons to functions
        self.startSystem.clicked.connect(lambda: self.start_System(selectedPort))
        self.stopSystem.clicked.connect(self.stop_System)
        self.openCamera.clicked.connect(self.start_camera)
        self.closeCamera.clicked.connect(self.stop_camera)

        self.serialPort.currentIndexChanged.connect(self.handle_serial_port_selection)
        self.modeSelect.currentIndexChanged.connect(self.handle_mode_selection)

    def start_System(self,selectedPort):
        self.serialport.setPort(selectedPort)
        self.serialport.connect()
        self.serialport.send_data("ON")
    
    def stop_System(self):
        self.serialport.disconnect()
    
    def update_serial_ports(self):
        ports = self.serialport.list_serial_ports()
        self.serialPort.clear()  
        self.serialPort.addItems(ports) 

    def handle_serial_port_selection(self):
        selectedPort = self.serialPort.currentText()  
        print(f"Selected serial port: {selectedPort}")

    def update_mode_select(self):
        self.modeSelect.clear()  
        self.modeSelect.addItems(self.modeList)  

    def handle_mode_selection(self):
        selectedMode = self.modeSelect.currentText()  
        print(f"Selected mode: {selectedMode}")

    def start_camera(self):
        """Open the camera when the button is clicked."""
        if self.capture is None or not self.capture.isOpened():
            # Open the camera
            self.capture = cv2.VideoCapture(0)
            if self.capture.isOpened():
                print("Camera opened successfully!")
                self.timer.start(0)  # Update frames every 30ms
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
                results = vinomodel(frame)
                annotated_frame = results[0].plot()  # Annotate frame with detections
                rgb_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
                
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
    modeList=["ĐIỆN TRỞ","TỤ ĐIỆN"]
    serialPort = SerialPort("COM5", 115200)
    MainWindow = Ui_MainWindow(serialPort,modeList)
    MainWindow.show()
    sys.exit(app.exec_())
