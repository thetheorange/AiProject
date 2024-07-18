import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl

class AudioPlayer(QWidget):
    def __init__(self, path: str):
        super().__init__()
        self.path=path
        # 初始化播放器
        self.player = QMediaPlayer(None)
        # 设置音频文件
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(path)))
        # self.init_ui()
        # 设置音量
        self.player.setVolume(50)
        # 初始化时播放音频（如果你不想在初始化时播放，可以注释掉这一行）
        self.on_state_changes(self.player.state())
        self.play_audio_begin()
        self.on_state_changes(self.player.state())

    def init_ui(self):
        # 创建播放和停止按钮
        self.play_button = QPushButton('播放')
        self.stop_button = QPushButton('停止')
        # 连接按钮的clicked信号到对应的槽
        self.play_button.clicked.connect(self.play_audio_begin)
        self.stop_button.clicked.connect(self.stop_audio)

        # 创建布局并添加按钮
        layout = QVBoxLayout()
        layout.addWidget(self.play_button)
        layout.addWidget(self.stop_button)
        self.setLayout(layout)

        # 设置窗口大小
        self.setGeometry(100, 100, 200, 150)  # 增加高度以适应停止按钮

    def on_state_changes(self, state):
        if state == QMediaPlayer.PlayingState:
            print("正在播放")
        elif state == QMediaPlayer.PausedState:
            print("已暂停")
        elif state == QMediaPlayer.StoppedState:
            print("已停止")

    def play_audio_begin(self):
        if not self.player.state() == QMediaPlayer.PlayingState:
            self.player.play()

    def stop_audio(self):
        self.player.stop()
        # 更新状态（可选，因为stop()后状态会自动更新）
        # self.on_state_changes(self.player.state())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = AudioPlayer('../../Temp/1.wav')
    player.show()  # 显示窗口
    sys.exit(app.exec_())