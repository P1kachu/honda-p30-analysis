#!/usr/bin/env python3

import sys
import os

known_addresses = [
        [0x0652, 3,  "Injector test bypass #1, Change to J label_065F(03 5F 06)"],
        [0x11B6, 1,  "VTP/VTS error removal, Change to 30"],
        [0x11CA, 1,  "VTEC Coolant Temp Check, (0x44 enables, 0xFF disables)"],
        [0x1580, 3,  "Injector test bypass #2, Change to J label_159A(03 9A 15)"],
        [0x1831, 1,  "Speed limiter Value, B9 is 180 km/h (115mph); FE is 254 km/h (158 mph)"],
        [0x1832, 2,  "Speed Limiter Jump Routine, Change from jge (CD 0A) to two NOPs (00 00) to disable speed limiter"],
        [0x208D, 3,  "O2 heater disable, Change to J label_20C7(03 C7 20)"],
        [0x2855, 2,  "Checksum Jump Instruction, Change JEQ 2867 (C9 10) to SJ 2867 (CB 10) to disable checksum"],
        [0x2B75, 2,  "Target Idle RPM, This is a Little Endian OBD1_16bit RPM ''untested''"],
        [0x3C6E, 2,  "IAC Jump Instruction, Change JEQ 3C71 (C9 01) to JEQ 3C70 (C9 00) to disable IAC error"],
        [0x3D06, 2,  "VTP/VTS error removale, Change to CB1C"],
        [0x3D27, 2,  "VTP/VTS error removale, Change to CB16"],
        [0x6001, 1,  "Vtec enable, 0xFF enables, 0x00 disables"],
        [0x6002, 1,  "Knock Sensor Enable, 0xFF enables, 0x00 disables"],
        [0x6003, 1,  "Oxygen heater Sensor, 0xFF enables, 0x00 disables"],
        [0x6004, 1,  "Barometric Sensor Enable, 0xFF enables, 0x00 disables"],
        [0x6005, 1,  "Oxygen Sensor, 0xFF enables, 0x00 disables"],
        [0x6006, 1,  "Injector Test, 0xFF disables, 0x00 enables"],
        [0x6009, 1,  "EGR System, 0xFF enables, 0x00 disables"],
        [0x600B, 1,  "Speed limiter - normal mode, 0x00 enables, 0xFF disables"],
        [0x6010, 1,  "Vtec VSS check, 0x00 enables, 0xFF disables"],
        [0x6011, 1,  "Debug/Test mode, 0xFF enables, 0x00 disables, has a lot of effects - more info hinted at here"],
        [0x6012, 2,  "Auto/Manual Enable, (no idea) lots of good stuff in this thread needs to be deciphered here"],
        [0x6013, 1,  "Speed Limiter Setting for debug mode, 0x00 disables, 0xFF enables"],
        [0x6375, 2,  "Low Cam Rev Limit Reset, OBD1_16bit RPM format"],
        [0x637B, 2,  "Low Cam Rev Limit Set"],
        [0x6381, 2,  "High Cam Rev Limit Reset"],
        [0x6387, 2,  "High Cam Rev Limit Set"],
        [0x638B, 12,  "Base A/F Low"],
        [0x6397, 12,  "Base A/F High"],
        [0x6432, 2,  "VTEC Point #1, VTEC Crossover RPM #1 Two OBD1_8bit Low Cam RPM values - first is reset, second is set."],
        [0x6434, 2,  "VTEC Point #2, VTEC Crossover RPM #2"],
        [0x6436, 2,  "VTEC Point #3, VTEC Crossover RPM #3"],
        [0x6438, 2,  "VTEC Point #4, VTEC Crossover RPM #4"],
        [0x6988, 47,  "Unkown table, has something to do with IACV pulse"],
        [0x7000, 10,  "mBar Scale, mBar scale row - OBD1_8bit MBar"],
        [0x700A, 20,  "Low Cam RPM Scale, Low cam RPM scale row - OBD1_8bit Low Cam RPM values"],
        [0x701E, 20,  "High RPM Scale, High RPM scale row - OBD1_8bit High Cam RPM values"],
        [0x7032, 200,  "Low Cam Fuel Table, 10 col x 20 row - OBD1_8bit Fuel ''v'' values"],
        [0x70FA, 10,  "Low Cam Fuel Coeff, 10 col x 1 row - OBD1_8bit Fuel ''m'' values"],
        [0x7104, 200,  "High Cam Fuel Table, 10 col x 20 row"],
        [0x71CC, 10,  "High Cam Fuel Coeff, 10 col x 1 row"],
        [0x71D6, 100,  "Extra Fuel Table LIMP MODE, 10 col x 10 row"],
        [0x7244, 10,  "Extra Fuel Coeff, 10 col x 1 row"],
        [0x724E, 200,  "Low Cam Ignition Table, 10 col x 20 row - OBD1_8bit Advance values"],
        [0x7316, 200,  "High Cam Ignition Table, 10 col x 20 row"],
        [0x73DE, 100,  "Extra Ignition Table LIMP MODE, 10 col x 10 row"],
        [0x744C, 200,  "Low Cam Table - CLOSE LOOP (target lambda), 10 col x 20 row"],
        [0x7514, 200,  "High Cam Table - CLOSE LOOP (target lambda), 10 col x 20 row"],
        [0x75DC, 100,  "Extra Table - no idea, all 00s, 10 col x 10 row "],
        ]

if len(sys.argv) < 3:
    print("USAGE: {0} STOCK_BINARY MODIFIED BINARY".format(sys.argv[0]))
    exit(1)

try:
    size_stock = os.path.getsize(sys.argv[1])
    size_modified = os.path.getsize(sys.argv[2])
    if size_stock != size_modified:
        print("Warning: size mismatch ({0} / {1})".format(size_stock, size_modified))
    else:
        print("Size OK")

    print("Stock rom used:    {0}".format(os.path.basename(sys.argv[1])))
    print("Modified rom used: {0}".format(os.path.basename(sys.argv[2])))
    print()

except Exception as e:
    print("Error in checking file size: {0}".format(e))


stock = open(sys.argv[1], 'rb').read(size_stock)
modified = open(sys.argv[2], 'rb').read(size_modified)


print("    Address     |          Modified value")
print("--" * 40)
for address in known_addresses:
    match = stock[address[0]:address[0] + address[1]] == modified[address[0]:address[0] + address[1]]
    if match == False and address[1] != 1:
        print("0x{:04X} : 0x{:04X} | {}".format(address[0], address[0] + address[1], address[2]))
        print()
    elif match == False and address[1] == 1:
        print("0x{:04X}          | {}".format(address[0], address[2]))
        print("\t\t| 0x{:02X} (stock) vs 0x{:02X} (modified)".format(stock[address[0]], modified[address[0]]))
        print()

    else:
        pass
