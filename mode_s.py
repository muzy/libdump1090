from ctypes import *
from rtlsdr import *
from time import gmtime
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
	capability 		= None
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
	modeA 		= None
	altitude 	= None
	unit 	= None
	bFlags 	= None

	"""
	Initializes the object with a mode_s message struct
	TODO: support for bflags
	"""
	def __init__(self, modesMessage):
		self.msg 		= "".join("{:02x}".format(ord(c)) for c in modesMessage.msg)
		# this msg needs to be sanitized...
		if modesMessage.msgbits == 56:
			self.msg 	= self.msg[:14]
		self.msgbits 	= modesMessage.msgbits
		self.msgtype 	= modesMessage.msgtype
		self.crcok 		= False if modesMessage == 0 else True
		self.crc 		= "{:06x}".format(modesMessage.crc)
		self.correctedbits = modesMessage.correctedbits
		self.corrected 	= modesMessage.corrected
		self.addr 		= "{:06x}".format(modesMessage.addr)
		self.phase_corrected = False if modesMessage.phase_corrected == 0 else True
		# note: this timestamp is left out at the moment
		self.timestampMsg 	= gmtime()
		self.remote 		= modesMessage.remote
		self.signalLevel	= ord(modesMessage.signalLevel)
		self.capability		= modesMessage.ca	
		self.iid			= modesMessage.iid
		self.metype			= modesMessage.metype
		self.mesub			= modesMessage.mesub
		self.heading		= modesMessage.heading
		self.raw_latitude	= modesMessage.raw_latitude
		self.raw_longitude	= modesMessage.raw_longitude
		self.fLat			= modesMessage.fLat
		self.fLon			= modesMessage.fLon
		self.flight			= modesMessage.flight
		self.ew_velocity	= modesMessage.ew_velocity
		self.ns_velocity	= modesMessage.ns_velocity
		self.vert_rate		= modesMessage.vert_rate
		self.velocity 		= modesMessage.velocity
		self.fs 			= modesMessage.fs
		self.modeA 			= modesMessage.modeA
		self.altitude 	= modesMessage.altitude
		self.unit 		= 'feet' if modesMessage.unit == 0 else 'meter'
		self.bFlags		= modesMessage.bFlags



class ModeSDetector(object):

	ADSB_FREQ = 1090000000
	ADSB_RATE = 2000000
	ADSB_BUF_SIZE = 4*16*16384 # 1MB

	def __init__(self, device_index=0):
		self.rtlsdr = RtlSdr(device_index=device_index)
		self.rtlsdr.set_center_freq(self.ADSB_FREQ)
		self.rtlsdr.set_sample_rate(self.ADSB_RATE)
		self.rtlsdr.set_gain(100)

		#f = open('output.bin', 'rb')
		#p = create_string_buffer(f.read()) 
		#print p

		libModeS.modesInit()
		libModeS.setPhaseEnhance()
		libModeS.setAggressiveFixCRC()
		for i in xrange(0,20):
			data = self.rtlsdr.read_bytes(self.ADSB_BUF_SIZE)
			mm = libModeS.processData(cast(data,c_char_p))
			#pprint(mm.contents.unit)
			while mm:
				foo = ModeSDetectorMessage(mm.contents)
				pprint(vars(foo))
				mm = mm.contents.next
			#print self.foo.contents

modes = ModeSDetector()



