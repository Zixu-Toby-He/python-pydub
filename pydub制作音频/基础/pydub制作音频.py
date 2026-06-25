import numpy
import pydub
import pydub.playback

# 生成示例数据
采样率 = 44100  # 示例采样率：44.1 kHz
采样率 = 96000  # 示例采样率：44.1 kHz
# 采样率选项信息源自chatgpt
# 　　电话质量：8    kHz，通常用于电话系统和语音通信。
# 　　标准质量：16   kHz，用于语音识别和一般音频录制。
# 　　光碟音质：44.1 kHz，用于音乐CD。
# 　　专业音频：48   kHz，用于音乐制作和数字音频工作站。
# 　高保真音频：96   kHz，用于专业音乐制作和高分辨率音频录制。
# 超高保真音频：192  kHz，用于专业音乐制作和高端音频设备。

t = numpy.arange(0,10,1/采样率)  # 10秒的时间坐标
y = numpy.sin(2*numpy.pi*440*t)    # 440 Hz的正弦波
y[t>5] = numpy.sin(2*numpy.pi*220*t[t>5])
# y = t*采样率/200 - numpy.int16(t*采样率/200)

# 将numpy数组转换为pydub的音频段
# 32767 = 2^15-1，此处为归一化系数
# 音频文件中振幅为 int16 数字
极大值_y = numpy.max(numpy.abs(y))
y_归一化 = numpy.int16(32767*y/极大值_y)

音频 = pydub.AudioSegment(y_归一化.tobytes(), frame_rate=采样率, sample_width=2, channels=1)

# 指定一个可写入的文件路径
音频文件路径 = "音频文件.wav"
音频.export(音频文件路径, format="wav")

# 播放（不成功）
# pydub.playback.play(音频)