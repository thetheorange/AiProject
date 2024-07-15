import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl


class AudioPlayer(QWidget):
    def __init__(self, path: str):
        super().__init__()

        # 初始化播放器
        self.player = QMediaPlayer(None)
        # 设置音频文件
        print(path)
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(path)))
        self.init_ui()

        # 设置音量
        self.player.setVolume(50)
        # self.play_audio_begin()
        self.on_state_changes(self.player.state())

    def init_ui(self):
        # 创建播放按钮
        self.play_button = QPushButton('播放')
        # 连接按钮的clicked信号到播放音频的槽
        self.play_button.clicked.connect(self.play_audio_begin)

        # 创建布局并添加按钮
        layout = QVBoxLayout()
        layout.addWidget(self.play_button)
        self.setLayout(layout)

        # 设置窗口大小
        self.setGeometry(100, 100, 200, 100)

    def on_state_changes(self, state):
        if state == QMediaPlayer.PlayingState:
            print("正在播放")
        elif state == QMediaPlayer.PausedState:
            print("已暂停")
        elif state == QMediaPlayer.StoppedState:
            print("已停止")

    def play_audio_begin(self):
        self.on_state_changes(self.player.state())
        # 播放音频
        if not self.player.state() == QMediaPlayer.PlayingState:
            self.player.play()
        self.on_state_changes(self.player.state())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = AudioPlayer('../Temp/1.wav')
    player.show()  # 显示窗口
    sys.exit(app.exec_())
