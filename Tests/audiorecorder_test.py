"""
录音机的qt测试
@Author Misaka-xxw
Time 2024/5/25
"""
import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from Core.Tools.AudioRecorder import AudioRecorder


class AudioTestWindow(QWidget):
    def __init__(self):
        """
        录音机测试简易qt界面
        """
        super().__init__()
        self.recorder = AudioRecorder()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.recorder.prefix_path = r"..\Temp"
        btn = QPushButton("Start Recording")
        btn.clicked.connect(self.on_start_recording)
        stop_btn = QPushButton("Stop Recording")
        stop_btn.clicked.connect(self.on_stop_recording)
        layout.addWidget(btn)
        layout.addWidget(stop_btn)
        self.setLayout(layout)

    @pyqtSlot()
    def on_start_recording(self):
        print("push start")
        self.recorder.start_recording()

    @pyqtSlot()
    def on_stop_recording(self):
        self.recorder.stop_recording()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    AudioTestWindow = AudioTestWindow()
    AudioTestWindow.show()
    sys.exit(app.exec_())
