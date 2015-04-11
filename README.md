libdump1090 README
===

libdump1090 is based on Dump 1090 which is a Mode S decoder specifically designed for RTLSDR devices.

The main features are:

* Robust decoding of weak messages, with mode1090 many users observed
  improved range compared to other popular decoders.
* Single bit errors correction using the 24 bit CRC.
* Ability to decode DF11, DF17 messages.
* Ability to decode DF formats like DF0, DF4, DF5, DF16, DF20 and DF21
  where the checksum is xored with the ICAO address by brute forcing the
  checksum field using recently seen ICAO addresses.

Installation
---

On Linux and OS X run the following command first:

 gcc -fPIC -g -c -Wall mode_s.c 

On Linux then run:

 gcc -shared -o libmodes.so mode_s.o /usr/lib/x86_64-linux-gnu/libm.so

On OS X then run:

 gcc -dynamiclib -o libmodes.so mode_s.o


To cross-compile for windows with mingw on linux (for 64bit):

/usr/bin/x86_64-w64-mingw32-gcc -g -c -Wall mode_s.c
/usr/bin/x86_64-w64-mingw32-gcc -shared -o libmodes.dll mode_s.o -Wl,--out-implib,libmodes.a

For windows 32 bit use:

/usr/bin/i686-w64-mingw32-gcc -g -c -Wall mode_s.c
/usr/bin/i686-w64-mingw32-gcc -shared -o libmodes.dll mode_s.o -Wl,--out-implib,libmodes.a

Credits
---

Dump1090 was written by Salvatore Sanfilippo <antirez@gmail.com> and is
released under the BSD three clause license.

libdump1090 was written by Sebastian Muszytowski and is released under the BSD
three clause license.
