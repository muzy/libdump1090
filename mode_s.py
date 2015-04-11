from ctypes import *
from rtlsdr import *
from libmodes import *
from pprint import pprint
#from bitstring import *
#except ImportError: from .libmodes import libModeS, modesMessage

class ModeSDetectorMessage():
	"""
	Class member variables
	"""
	msg 	= None
	msgbits = None
	msgtype = None
	crcok 	= None
	crc 	= None
	correctedbits 	= None
	corrected 		= None
	addr 			= None
	phase_corrected = None
	timestampMsg	= None
	remote 			= None
	signalLevel 	= None
	ca 		= None
	iid 	= None
	metype 	= None
	mesub 	= None
	heading = None
	raw_latitude 	= None
	raw_longitude 	= None
	fLat 	= None
	fLon 	= None
	flight 	= None
	ew_velocity = None
	ns_velocity = None
	vert_rate 	= None
	velocity 	= None
	fs 			= None
	altitude 	= None
	unit 	= None
	bFlags 	= None

	def __init__(self, modesMessage):
		self.msg = "".join("{:02x}".format(ord(c)) for c in modesMessage.msg)
		self.addr = "{:06x}".format(modesMessage.addr)
		self.altitude = modesMessage.altitude
		self.unit = 'feet' if modesMessage.unit == 0 else 'meter'

		print self.addr


class ModeSDetector(object):

	ADSB_FREQ = 1090000000
	ADSB_RATE = 2000000
	ADSB_BUF_SIZE = 4*16*16384 # 2MB

	def __init__(self, device_index=0):
		"""
		self.rtlsdr = RtlSdr(device_index=device_index)
		self.rtlsdr.set_center_freq(self.ADSB_FREQ)
		self.rtlsdr.set_sample_rate(self.ADSB_RATE)
		self.rtlsdr.set_gain(100)
		"""

		f = open('/tmp/output.bin', 'rb')
		p = create_string_buffer(f.read()) 
		print p

		libModeS.modesInit()
		libModeS.setPhaseEnhance()
		libModeS.setAggressiveFixCRC()
		mm = libModeS.processData(p)
		#pprint(mm.contents.unit)
		foo = ModeSDetectorMessage(mm.contents)
		pprint(foo)
		#print self.foo.contents

modes = ModeSDetector()



