import numpy
import pydub
import pathlib

from . import 常数

采样率 = 44100
音符持续时间 = 0.5
音符间中顿时间 = 0.1

def 曲谱转化为震动(曲谱, 乐器):
	音符个数 = len(曲谱)
	t = numpy.arange(0, 音符个数 * (音符持续时间 + 音符间中顿时间), 1 / 采样率)
	y = numpy.zeros_like(t)
	for i in range(音符个数):
		起始时间 = i * (音符持续时间 + 音符间中顿时间)
		终止时间 = 起始时间 + 音符持续时间
		频率 = 常数.音高频率表[曲谱[i]]
		待修改下标 = (t >= 起始时间) * (t < 终止时间)
		相位 = 2 * 2 * numpy.pi * 频率 * (t[待修改下标] - 起始时间)
		相位 = 相位 % (2*numpy.pi)
		y[待修改下标] = 乐器(相位)
	return t,y

def 震动转化为音频(震动):
	t = 震动[0]
	y = 震动[1]
	极大值_y = numpy.max(y)
	极小值_y = numpy.min(y)
	
	中间值 = (极大值_y + 极小值_y) / 2
	差值   = 极大值_y - 极小值_y
	
	y_归一化 = numpy.int16(65535 * (y - 中间值) / 差值)
	音频 = pydub.AudioSegment(y_归一化.tobytes(), frame_rate=采样率, sample_width=2, channels=1)
	return 音频

def 音频写入文件(音频, 文件路径: pathlib.Path):
	match(文件路径.suffix):
		case ".wav":
			音频.export(文件路径, format="wav")
		case ".mp3":
			音频.export(文件路径, format="mp3")
		case 无效格式:
			raise ValueError("暂不支持“{}”格式生成".format(无效格式))
