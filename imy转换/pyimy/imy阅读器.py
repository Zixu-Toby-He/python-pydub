import re
import pathlib
import pydub
import pydub.generators

from . import 常数


class imy阅读器:
	def __init__(self, 文件路径:pathlib.Path):
		with 文件路径.open("r", encoding = "utf-8") as f:
			self.文件内容 = f.read()

	@property
	def 节拍速度(self):
		节拍速度_匹配 = re.search(r"BEAT:(\d+)", self.文件内容)
		if (节拍速度_匹配):
			return int(节拍速度_匹配.group(1))
		else:
			return 120

	@节拍速度.setter
	def 节拍速度(self, 节拍速度):
		print("暂时无法设置节拍速度")

	@property
	def 单拍毫秒时长(self):
		return 60000 / self.节拍速度

	@property
	def 曲谱(self):
		曲谱_匹配 = re.search(
			r"MELODY:\s*([\s\S]+?)\s*END:IMELODY",
			self.文件内容,
			re.IGNORECASE
		)
		if (曲谱_匹配):
			曲谱字符串 =  "".join(曲谱_匹配.group(1).split())  # 去掉所有空白字符
			音符匹配器 = re.compile(r"([a-g])(\d)(-?)")
			音符信息   = 音符匹配器.findall(曲谱字符串)
			return tuple(音符信息)
		else:
			return tuple()

	def 生成演奏信息(self, 单拍占空比:float = 0.95):
		音符信息   = self.曲谱
		单拍时长   = self.单拍毫秒时长

		音频信息 = []
		间隔时长 = int(单拍时长 * (1 - 单拍占空比))
		for 音符, 八度, 延长 in 音符信息:
			频率 = 常数.音高频率表[音符.lower()] * (2 ** (int(八度) - 1))
			if (延长 == '-'):
				音符时长 = 2 * 单拍时长 - 间隔时长
			else:
				音符时长 = 单拍时长 - 间隔时长

			# 响 + 静默
			音频信息.append((频率, 音符时长 - 间隔时长))
			音频信息.append((0,    间隔时长))
		return tuple(音频信息[:-1])

	def 输出(self, 文件路径:pathlib.Path, 单拍占空比:float = 0.95, 演奏乐器:str = "正弦波"):
		音频生成器 = pydub.AudioSegment.silent(duration=0)  # 初始化空音频
		演奏信息 = self.生成演奏信息(单拍占空比 = 单拍占空比)
		match(文件路径.suffix):
			case ".mp3":
				格式 = "mp3"
			case ".wav":
				格式 = "wav"
			case 无效格式:
				raise ValueError("暂不支持“{}”格式生成".format(无效格式))
		match(演奏乐器):
			case "正弦波":
				for 频率, 时长 in 演奏信息:
					# 生成纯正弦波单音（音量设为 -10 dBFS 避免爆音）
					正弦波 = pydub.generators.Sine(频率).to_audio_segment(duration = 时长).apply_gain(-10)
					# 拼接
					音频生成器 += 正弦波
			case "方波":
				for 频率, 时长 in 演奏信息:
					# 生成方波（音量设为 -10 dBFS 避免爆音）
					if (频率 == 0):
						方波 = pydub.generators.Sine(频率).to_audio_segment(duration = 时长).apply_gain(-10)
					else:
						方波 = pydub.generators.Square(频率).to_audio_segment(duration = 时长).apply_gain(-10)
					# 拼接
					音频生成器 += 方波
			case "三角波":
				for 频率, 时长 in 演奏信息:
					# 生成三角波（音量设为 -10 dBFS 避免爆音）
					if (频率 == 0):
						三角波 = pydub.generators.Sine(频率).to_audio_segment(duration = 时长).apply_gain(-10)
					else:
						三角波 = pydub.generators.Triangle(频率).to_audio_segment(duration = 时长).apply_gain(-10)
					# 拼接
					音频生成器 += 三角波
			case "锯齿波":
				for 频率, 时长 in 演奏信息:
					# 生成锯齿波（音量设为 -10 dBFS 避免爆音，安排 5 % 的下降周期防止突变）
					if (频率 == 0):
						锯齿波 = pydub.generators.Sine(频率).to_audio_segment(duration = 时长).apply_gain(-10)
					else:
						锯齿波 = pydub.generators.Sawtooth(频率, duty_cycle=0.95).to_audio_segment(duration = 时长).apply_gain(-10)
					# 拼接
					音频生成器 += 锯齿波
			case 无效乐器:
				raise ValueError("暂不支持“{}”乐器".format(无效乐器))
		音频生成器.export(文件路径, format = 格式)
		print("✅ 转换成功！文件已保存为：{}".format(文件路径))

