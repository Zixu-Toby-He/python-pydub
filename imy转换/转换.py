import pathlib

import pyimy

当前路径 = pathlib.Path(__file__).parent
(当前路径 / "output").mkdir(parents = True, exist_ok = True)


if __name__ == "__main__":
	转换器 = pyimy.imy阅读器(当前路径 / "input" / "小星星.imy")
	print("节拍速度：{} 拍 / min".format(转换器.节拍速度))
	print("单拍时长：{} s".format(转换器.单拍毫秒时长 / 1000))
	print("曲谱：{}".format(tuple("".join(i) for i in 转换器.曲谱)))
	转换器.输出(当前路径 / "output" / "小星星.wav", 演奏乐器 = "锯齿波")
