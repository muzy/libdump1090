// dump1090, a Mode S messages decoder for RTLSDR devices.
//
// Copyright (C) 2012 by Salvatore Sanfilippo <antirez@gmail.com>
//
// All rights reserved.
//
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions are
// met:
//
//  *  Redistributions of source code must retain the above copyright
//     notice, this list of conditions and the following disclaimer.
//
//  *  Redistributions in binary form must reproduce the above copyright
//     notice, this list of conditions and the following disclaimer in the
//     documentation and/or other materials provided with the distribution.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
// "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
// LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
// A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
// HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
// SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
// LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
// DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
// THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
// (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
// OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
//
#ifndef __DUMP1090_H
#define __DUMP1090_H

// File Version number
// ====================
// Format is : MajorVer.MinorVer.DayMonth.Year"
// MajorVer changes only with significant changes
// MinorVer changes when additional features are added, but not for bug fixes (range 00-99)
// DayDate & Year changes for all changes, including for bug fixes. It represent the release date of the update
//
#define MODES_DUMP1090_VERSION     "1.10.3010.14"

// ============================= Include files ==========================
#include <stdint.h>
#include <stdio.h>
#include <time.h>
#include <string.h>

#include <stdlib.h>
#include <stdint.h>
#include <errno.h>
#include <unistd.h>
#include <math.h>
#include <sys/time.h>
#include <sys/timeb.h>
#include <fcntl.h>
#include <ctype.h>
#include <sys/stat.h>
#ifndef _WIN32
	#include <sys/ioctl.h>
#endif

#define MODES_ASYNC_BUF_SIZE       (4*16*16384)               // 1M
#define MODES_ASYNC_BUF_SAMPLES    (MODES_ASYNC_BUF_SIZE / 2) // Each sample is 2 bytes
#define MODES_MSG_SQUELCH_LEVEL    0x02FF                     // Average signal strength limit
#define MODES_MSG_ENCODER_ERRS     3                          // Maximum number of encoding errors

// When changing, change also fixBitErrors() and modesInitErrorTable() !!
#define MODES_MAX_BITERRORS        2                          // Global max for fixable bit erros
#define MODES_USER_LATITUDE_DFLT   (0.0)
#define MODES_USER_LONGITUDE_DFLT  (0.0)

#define MODES_ICAO_CACHE_LEN 1024 // Power of two required
#define MODES_ICAO_CACHE_TTL 60   // Time to live of cached addresses

#define MODES_PREAMBLE_US        8              // microseconds = bits
#define MODES_PREAMBLE_SAMPLES  (MODES_PREAMBLE_US       * 2)
#define MODES_PREAMBLE_SIZE     (MODES_PREAMBLE_SAMPLES  * sizeof(uint16_t))
#define MODES_LONG_MSG_BYTES     14
#define MODES_SHORT_MSG_BYTES    7
#define MODES_LONG_MSG_BITS     (MODES_LONG_MSG_BYTES    * 8)
#define MODES_SHORT_MSG_BITS    (MODES_SHORT_MSG_BYTES   * 8)
#define MODES_LONG_MSG_SAMPLES  (MODES_LONG_MSG_BITS     * 2)
#define MODES_SHORT_MSG_SAMPLES (MODES_SHORT_MSG_BITS    * 2)
#define MODES_LONG_MSG_SIZE     (MODES_LONG_MSG_SAMPLES  * sizeof(uint16_t))
#define MODES_SHORT_MSG_SIZE    (MODES_SHORT_MSG_SAMPLES * sizeof(uint16_t))


#define MODES_ICAO_CACHE_LEN 1024 // Power of two required
#define MODES_ICAO_CACHE_TTL 60   // Time to live of cached addresses

#define MODES_UNIT_FEET 0
#define MODES_UNIT_METERS 1

#define MODES_ACFLAGS_LATLON_VALID   (1<<0)  // Aircraft Lat/Lon is decoded
#define MODES_ACFLAGS_ALTITUDE_VALID (1<<1)  // Aircraft altitude is known
#define MODES_ACFLAGS_HEADING_VALID  (1<<2)  // Aircraft heading is known
#define MODES_ACFLAGS_SPEED_VALID    (1<<3)  // Aircraft speed is known
#define MODES_ACFLAGS_VERTRATE_VALID (1<<4)  // Aircraft vertical rate is known
#define MODES_ACFLAGS_SQUAWK_VALID   (1<<5)  // Aircraft Mode A Squawk is known
#define MODES_ACFLAGS_CALLSIGN_VALID (1<<6)  // Aircraft Callsign Identity
#define MODES_ACFLAGS_EWSPEED_VALID  (1<<7)  // Aircraft East West Speed is known
#define MODES_ACFLAGS_NSSPEED_VALID  (1<<8)  // Aircraft North South Speed is known
#define MODES_ACFLAGS_AOG            (1<<9)  // Aircraft is On the Ground
#define MODES_ACFLAGS_LLEVEN_VALID   (1<<10) // Aircraft Even Lot/Lon is known
#define MODES_ACFLAGS_LLODD_VALID    (1<<11) // Aircraft Odd Lot/Lon is known
#define MODES_ACFLAGS_AOG_VALID      (1<<12) // MODES_ACFLAGS_AOG is valid
#define MODES_ACFLAGS_FS_VALID       (1<<13) // Aircraft Flight Status is known
#define MODES_ACFLAGS_NSEWSPD_VALID  (1<<14) // Aircraft EW and NS Speed is known
#define MODES_ACFLAGS_LATLON_REL_OK  (1<<15) // Indicates it's OK to do a relative CPR

#define MODES_ACFLAGS_LLEITHER_VALID (MODES_ACFLAGS_LLEVEN_VALID | MODES_ACFLAGS_LLODD_VALID)
#define MODES_ACFLAGS_LLBOTH_VALID   (MODES_ACFLAGS_LLEVEN_VALID | MODES_ACFLAGS_LLODD_VALID)
#define MODES_ACFLAGS_AOG_GROUND     (MODES_ACFLAGS_AOG_VALID    | MODES_ACFLAGS_AOG)


// When debug is set to MODES_DEBUG_NOPREAMBLE, the first sample must be
// at least greater than a given level for us to dump the signal.
#define MODES_DEBUG_NOPREAMBLE_LEVEL 25


#define MODES_NOTUSED(V) ((void) V)

// The struct we use to store information about a decoded message.
struct modesMessage {
    // Generic fields
    unsigned char msg[MODES_LONG_MSG_BYTES];      // Binary message.
    uint32_t      msgpos;                         // Position of message in the buffer 
    int           msgbits;                        // Number of bits in message 
    int           msgtype;                        // Downlink format #
    int           crcok;                          // True if CRC was valid
    uint32_t      crc;                            // Message CRC
    int           correctedbits;                  // No. of bits corrected 
    char          corrected[MODES_MAX_BITERRORS]; // corrected bit positions
    uint32_t      addr;                           // ICAO Address from bytes 1 2 and 3
    int           phase_corrected;                // True if phase correction was applied
    uint64_t      timestampMsg;                   // Timestamp of the message
    int           remote;                         // If set this message is from a remote station
    unsigned char signalLevel;                    // Signal Amplitude

    // DF 11
    int  ca;                    // Responder capabilities
    int  iid;

    // DF 17, DF 18
    int    metype;              // Extended squitter message type.
    int    mesub;               // Extended squitter message subtype.
    int    heading;             // Reported by aircraft, or computed from from EW and NS velocity
    int    raw_latitude;        // Non decoded latitude.
    int    raw_longitude;       // Non decoded longitude.
    double fLat;                // Coordinates obtained from CPR encoded data if/when decoded
    double fLon;                // Coordinates obtained from CPR encoded data if/when decoded
    char   flight[16];          // 8 chars flight number.
    int    ew_velocity;         // E/W velocity.
    int    ns_velocity;         // N/S velocity.
    int    vert_rate;           // Vertical rate.
    int    velocity;            // Reported by aircraft, or computed from from EW and NS velocity

    // DF4, DF5, DF20, DF21
    int  fs;                    // Flight status for DF4,5,20,21
    int  modeA;                 // 13 bits identity (Squawk).

    // Fields used by multiple message types.
    int  altitude;
    int  unit; 
    int  bFlags;                // Flags related to fields in this structure
    struct modesMessage *next; // next message
};

// Program global state
struct {                             // Internal state

    uint16_t       *pData; // Raw IQ sample buffers from RTL
    uint32_t       *icao_cache;      // Recently seen ICAO addresses cache
    uint16_t       *magnitude;       // Magnitude vector
    uint16_t       *maglut;          // I/Q -> Magnitude lookup table

    // Configuration
    int   phase_enhance;             // Enable phase enhancement if true
    int   nfix_crc;                  // Number of crc bit error(s) to correct
    int   check_crc;                 // Only display messages with good CRC
    int   debug;                     // Debugging mode
    int   quiet;                     // Suppress stdout
    struct modesMessage *modeMessages;
} Modes;


// ======================== function declarations =========================

#ifdef __cplusplus
extern "C" {
#endif


//
// Functions exported from mode_s.c
//
void detectModeS        (uint16_t *m, uint32_t mlen);
void decodeModesMessage (struct modesMessage *mm, unsigned char *msg);
void displayModesMessage(struct modesMessage *mm);
void useModesMessage    (struct modesMessage *mm);
void computeMagnitudeVector(uint16_t *pData);
void modesInitErrorInfo();
void modesInit();
void modesInitConfig();
void setAggressiveFixCRC();
void setFixCRC();
void setPhaseEnhance();
struct modesMessage *processData(unsigned char *buf);

#ifdef __cplusplus
}
#endif

#endif // __DUMP1090_H
