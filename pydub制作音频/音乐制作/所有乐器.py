"""
输入相位得到相位函数值

相位取值范围：[0,2π]
函数值范围：[-1,+1]
"""
import numpy
π = numpy.pi
def 正弦波(phi):
	return numpy.sin(phi)

def 方波(phi):
	return 2*(phi - π) - 1

def 三角波(phi):
	方波(phi)*phi

def 锯齿波(phi):
	return phi/π - 1

