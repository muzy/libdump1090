from ctypes import *
from ctypes.util import find_library

def load_libmodes():
    driver_files = ['modes.dll', 'libmodes.so']
    driver_files += ['..//modes.dll', '..//libmodes.so']
    driver_files += ['modes//modes.dll', 'modes//libmodes.so']
    driver_files += [find_library('modes'), find_library('libmodes')]

    dll = None

    for driver in driver_files:
        try:
            dll = CDLL(driver)
            break
        except:
            pass
    else:
        raise ImportError('Error loading libmodes. Make sure libmodes '\
                          '(and all of its dependencies) are in your path')

    return dll

libmodes = load_libmodes()

print libmodes

class modesMessage(Structure):
    pass

modesMessage._fields_ = [("msg", c_char_p),
                        ("msgbits", c_int),
                        ("msgtype", c_int),
                        ("crcok", c_int),
                        ("crc", c_uint),
                        ("correctedbits", c_int),
                        ("corrected", c_char_p),
                        ("addr", c_uint),
                        ("phase_corrected", c_int),
                        ("timestampMsg", c_uint),
                        ("remote", c_uint),
                        ("signalLevel", c_char),
                        ("ca", c_int),
                        ("iid", c_int),
                        ("metype", c_int),
                        ("mesub", c_int),
                        ("heading", c_int),
                        ("raw_latitude", c_int),
                        ("raw_longitude", c_int),
                        ("fLat", c_double),
                        ("fLon", c_double),
                        ("flight", c_char_p),                        
                        ("ew_velocity", c_int),
                        ("ns_velocity", c_int),
                        ("vert_rate", c_int),
                        ("velocity", c_int),
                        ("fs", c_int),
                        ("altitude", c_int),                        
                        ("unit", c_int),
                        ("bFlags", c_int),
                        ("next", POINTER(modesMessage))]

# void modesInit();
f = libmodes.modesInit
f.restype, f.argtypes = None, None

# void setAggressiveFixCRC();
f = libmodes.setAggressiveFixCRC
f.restype, f.argtypes = None, None

# void setFixCRC();
f = libmodes.setFixCRC
f.restype, f.argtypes = None, None

# void setPhaseEnhance();
f = libmodes.setPhaseEnhance
f.restype, f.argtypes = None, None

# struct modesMessage *processData(unsigned char *buf);
f = libmodes.processData
f.restype, f.argtypes = POINTER(modesMessage), [c_char_p]

