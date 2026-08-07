import pydub
import pydub.generators

import re

def 提取参数(imy文件内容):
	节拍速度_匹配 = re.search(r"BEAT:(\d+)", imy文件内容)

	if (节拍速度_匹配):
		bpm = int(节拍速度_匹配.group(1))
	else:
		bpm = 120

	return {
		"bpm": bpm
	}

def 提取曲谱(imy文件内容):
	# 提取旋律字符串（移除换行和空格）
	曲谱_匹配 = re.search(r"MELODY:\s*([\s\S]+?)\s*END:IMELODY", imy文件内容, re.IGNORECASE)
	if (曲谱_匹配):
		return "".join(曲谱_匹配.group(1).split())  # 去掉所有空白字符
	else:
		raise ValueError("未在文本中找到 MELODY 字段")

def imy_to_mp3(输入文件, 输出文件="output.mp3"):
	"""
	将 IMY 格式的文本铃声转换为 MP3 文件
	"""
	# 0. 读取文件
	with open(输入文件, "r", encoding = "utf-8") as f:
		imy文件内容 = f.read()

	# 1. 解析参数
	参数 = 提取参数(imy文件内容)
	bpm  = 参数["bpm"]
	单拍毫秒时长 = 60000 / bpm

	# 2. 提取旋律字符串（移除换行和空格）
	曲谱字符串 = 提取曲谱(imy文件内容)

	# 3. 音符频率映射表（基于 A4=440Hz 的十二平均律）
	#    这里假设数字 '1' 对应中央 C（C4），数字 '2' 对应高八度 C5，以此类推
	base_freq = {
		'c': 261.63,  # C4
		'd': 293.66,  # D4
		'e': 329.63,  # E4
		'f': 349.23,  # F4
		'g': 392.00,  # G4
		'a': 440.00,  # A4
		'b': 493.88   # B4
	}

	# 4. 解析音符序列：正则匹配 字母 + 数字 + 可选延长符('-')
	#    例如 'c1', 'g1-', 'a2'
	pattern = re.compile(r'([a-g])(\d)(-?)')
	notes = pattern.findall(曲谱字符串)

	# 5. 合成音频（逐个音符拼接）
	final_audio = pydub.AudioSegment.silent(duration=0)  # 初始化空音频

	for note_name, octave_str, dot in notes:
		# 计算频率：基础频率 * 2^(八度数-1)，例如 c1=261.6, c2=523.2
		octave = int(octave_str)
		freq = base_freq[note_name.lower()] * (2 ** (octave - 1))

		# 计算持续时间：如果带有 '-'，时值翻倍（附点/延长效果）
		duration_ms = int(单拍毫秒时长 * 2 if dot == '-' else 单拍毫秒时长)

		# 生成纯正弦波单音（音量设为 -10 dBFS 避免爆音）
		sine_wave = pydub.generators.Sine(freq).to_audio_segment(duration=duration_ms).apply_gain(-10)
		
		# 拼接
		final_audio += sine_wave

	# 6. 导出为 MP3
	final_audio.export(输出文件, format="mp3")
	print(f"✅ 转换成功！文件已保存为：{输出文件}")


# ------------------- 使用示例 -------------------
if __name__ == "__main__":
	# 你提供的“小星星”IMY 文本
	imy_to_mp3("小星星.imy", "小星星.mp3")