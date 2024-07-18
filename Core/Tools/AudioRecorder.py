"""
录音机
依赖包：PyAudio-0.2.14
参考：
https://zhuanlan.zhihu.com/p/92205480
https://www.cnblogs.com/dreamboy2000/p/15337029.html
@Author Misaka-xxw
Time 2024/5/18
ps:
1. pydub不合适。使用numpy就可以了。
2. 后面临时文件的存放仍然需要统一标准。
3. 还有临时文件的清除未写
"""

import time
import threading
import pyaudio
import wave
import numpy as np

CHUNK = 1024  # 每个缓冲区的帧数
FORMAT = pyaudio.paInt16  # 采样位数
CHANNELS = 1  # 单声道
RATE = 16000  # 采样频率


class AudioRecorder(object):
    def __init__(self):
        """
        录音机
        """
        #print("init")
        super().__init__()
        self.pyaudio_instance = pyaudio.PyAudio()
        self.stream = None
        self.recording: bool = False
        self.prefix_path: str = '..\Temp'  # 文件父文件夹目录。example:r'D:\GitHub\AiProject\Tests'
        self.path: str = ""  # 文件目录

    def start_recording(self):
        print("start_recording")
        self.path = self.prefix_path + '\\' + time.strftime('%Y%m%d%H%M%S', time.localtime()) + ".wav"
        try:
            if not self.recording:
                self.recording = True
                self.stream = self.pyaudio_instance.open(format=FORMAT,
                                                         channels=CHANNELS,
                                                         rate=RATE,
                                                         input=True,
                                                         frames_per_buffer=CHUNK)
                wf = wave.open(self.path, 'wb')
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(self.pyaudio_instance.get_sample_size(FORMAT))
                wf.setframerate(RATE)

                def record_loop():
                    """
                    录音循环（应在一个单独的线程中运行）
                    """
                    while self.recording:
                        data = self.stream.read(CHUNK)
                        if data:
                            wf.writeframes(data)

                    wf.close()
                    self.stream.stop_stream()
                    self.stream.close()
                    self.pyaudio_instance.terminate()

                t = threading.Thread(target=record_loop, daemon=True)
                t.start()

        except Exception as e:
            print(str(e))

    def stop_recording(self):
        if self.recording:
            self.path = self.wav2pcm(self.path)
            print(self.path)
            self.recording = False
            print("stop")



    @staticmethod
    def wav2pcm(wavfile: str, data_type=np.int16) -> str:
        """
        wav文件转成pcm文件
        :param wavfile:wav文件路径
        :param data_type:数据类型，默认为int16
        :return: pcm文件名
        """
        pcm_file = wavfile[:-3] + "pcm"
        with open(wavfile, "rb") as f:
            f.seek(0)
            f.read(44)
            data = np.fromfile(f, dtype=data_type)
            data.tofile(pcm_file)
        return pcm_file
