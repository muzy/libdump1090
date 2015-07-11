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

	messages = []

	def __init__(self, device_index=0):
		self.device_index = device_index
		libModeS.modesInit()
		libModeS.setPhaseEnhance()
		libModeS.setAggressiveFixCRC()
		

	def readFromFile(self, filename):
		with open(filename,'rb') as f:
			while True:
				data = f.read(self.ADSB_BUF_SIZE)
				if not data:
					break
				else:
					buff = create_string_buffer(data)
					mm = libModeS.processData(buff)
					self.readDataToBuffer(mm)


	def initRTLSDR(self):
		self.rtlsdr = RtlSdr(device_index=self.device_index)
		self.rtlsdr.set_center_freq(self.ADSB_FREQ)
		self.rtlsdr.set_sample_rate(self.ADSB_RATE)
		self.rtlsdr.set_gain(100)
		self.rtlsdr.init = True


	def readFromRTLSDR(self,times):
		if not self.rtlsdr.init:
			self.initRTLSDR()
		for i in xrange(0,times):
			data = self.rtlsdr.read_bytes(self.ADSB_BUF_SIZE)
			self.processFromRTLSDR(data)

	def processFromRTLSDR(self,data,rtlsdr=None):
		mm = libModeS.processData(cast(data,c_char_p))
		self.readDataToBuffer(mm)

	def readFromRTLSDRAsync(self):
		self.rtlsdr.read_bytes_async(self.processFromRTLSDR,num_bytes=self.ADSB_BUF_SIZE)

	def stopReadFromRTLSDRAsync(self):
		self.rtlsdr.cancel_read_async()

	def readDataToBuffer(self,mm):
		while mm:
			message = ModeSDetectorMessage(mm.contents)
			self.messages.append(message)
			mm = mm.contents.next

	def printMessages(self):
		for message in self.messages:
			pprint(vars(message))


modes = ModeSDetector()
modes.readFromFile("output.bin")
modes.printMessages()



