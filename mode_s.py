from ctypes import *
from rtlsdr import *
from libmodes import *
from pprint import pprint
#except ImportError: from .libmodes import libModeS, modesMessage


class ModeSDetector(object):

	ADSB_FREQ = 1090000000
	ADSB_RATE = 2000000
	ADSB_BUF_SIZE = 8*16*16384 # 2MB

	def __init__(self, device_index=0):
		self.rtlsdr = RtlSdr(device_index=device_index)
		self.rtlsdr.set_center_freq(self.ADSB_FREQ)
		self.rtlsdr.set_sample_rate(self.ADSB_RATE)
		self.rtlsdr.set_gain(100)

		libModeS.modesInit()
		libModeS.setPhaseEnhance()
		libModeS.setAggressiveFixCRC()
		for i in xrange(10):
			pprint(libModeS.processData(self.rtlsdr.read_bytes(self.ADSB_BUF_SIZE)))
		#print self.foo.contents

modes = ModeSDetector()



