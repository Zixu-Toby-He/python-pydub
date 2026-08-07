import re
import pathlib
import pydub
import pydub.generators

当前路径 = pathlib.Path(__file__).parent

def 提取信息(imy文件内容):
	# 读取节拍速度
	节拍速度_匹配 = re.search(r"BEAT:(\d+)", imy文件内容)
	if (节拍速度_匹配):
		bpm = int(节拍速度_匹配.group(1))
	else:
		bpm = 120

	# 提取旋律字符串（移除换行和空格）
	曲谱_匹配 = re.search(r"MELODY:\s*([\s\S]+?)\s*END:IMELODY", imy文件内容, re.IGNORECASE)
	if (曲谱_匹配):
		曲谱 =  "".join(曲谱_匹配.group(1).split())  # 去掉所有空白字符
	else:
		曲谱 = ""

	return {
		"bpm":    bpm,
		"melody": 曲谱
	}

def 音符信息拆解(曲谱字符串, 单拍时长, 单拍占空比:float = 0.95):
	音高频率表 = {
		"c": 261.63,  # C4
		"d": 293.66,  # D4
		"e": 329.63,  # E4
		"f": 349.23,  # F4
		"g": 392.00,  # G4
		"a": 440.00,  # A4
		"b": 493.88   # B4
	}
	音符匹配器 = re.compile(r"([a-g])(\d)(-?)")
	音符信息   = 音符匹配器.findall(曲谱字符串)

	音频信息 = []
	间隔时长 = int(单拍时长 * (1 - 单拍占空比))
	for 音符, 八度, 延长 in 音符信息:
		频率 = 音高频率表[音符.lower()] * (2 ** (int(八度) - 1))
		if (延长 == '-'):
			音符时长 = 2 * 单拍时长 - 间隔时长
		else:
			音符时长 = 单拍时长 - 间隔时长

		# 响 + 静默
		音频信息.append((频率, 音符时长 - 间隔时长))
		音频信息.append((0,    间隔时长))
	return tuple(音频信息[:-1])

def imy_to_mp3(输入文件:pathlib.Path, 输出文件:pathlib.Path):
	"""
	将 IMY 格式的文本铃声转换为 MP3 文件
	"""
	# 0. 读取文件
	with 输入文件.open("r", encoding = "utf-8") as f:
		imy文件内容 = f.read()

	# 1. 解析参数
	曲谱信息 = 提取信息(imy文件内容)

	bpm        = 曲谱信息["bpm"]
	曲谱字符串 = 曲谱信息["melody"]

	单拍毫秒时长 = 60000 / bpm

	# 3. 音符信息拆解
	音频信息 = 音符信息拆解(曲谱字符串, 单拍毫秒时长)

	# 5. 合成音频（逐个音符拼接）
	音频生成器 = pydub.AudioSegment.silent(duration=0)  # 初始化空音频

	for 频率, 时长 in 音频信息:
		# 生成纯正弦波单音（音量设为 -10 dBFS 避免爆音）
		正弦波 = pydub.generators.Sine(频率).to_audio_segment(duration=时长).apply_gain(-10)
		# 拼接
		音频生成器 += 正弦波

	# 6. 导出为 MP3
	音频生成器.export(输出文件, format="mp3")
	print(f"✅ 转换成功！文件已保存为：{输出文件}")

# ------------------- 使用示例 -------------------
if __name__ == "__main__":
	# 你提供的“小星星”IMY 文本
	imy_to_mp3(
		当前路径 / "小星星.imy",
		当前路径 / "小星星.mp3"
	)