"""
输入相位得到相位函数值

相位取值范围：[0,2π]
函数值范围：[-1,+1]
"""
import numpy
π = numpy.pi
def 正弦波(amp, phi):
	return amp*numpy.sin(phi)

def 方波(amp, phi):
	return amp*(2*(phi-π)-1)

def 三角波(amp, phi):
	amp*方波(phi)*phi

def 锯齿波(amp,phi):
	return amp*(phi/π - 1)

def 