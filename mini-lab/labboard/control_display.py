#! /usr/bin/env python3

# Example to control LabBoard display and LED
# Serial protocol available at: https://docs.totemmaker.net/labboard/serial/protocol/
import sys
import time
import serial
import serial.tools.list_ports

def print_ports_list():
    ports = serial.tools.list_ports.comports()
    print("Available: ", end="")
    if len(ports) == 0:
        print("none")
        return
    for port, desc, hwid in sorted(ports):
        print("{} ".format(port), end="")
    print()

##########################
## Serial connection code
##########################
# Check if correct amount of parameters is provided
if len(sys.argv) != 2:
    print_ports_list()
    exit("Serial port name not provided")
# Check if provided port is opened
port = None
try:
    port = serial.Serial(sys.argv[1], 57600, timeout=0.5)
except:
    print_ports_list()
    exit("Serial port {} cannot be opened".format(sys.argv[1]))
##########################
## Version display code
##########################
# Receive board revision and firmware version
port.flush()
port.write("\n".encode())
port.write("LB:CFG:REV:?\n".encode())
result_rev = port.readline().split(b":")
port.write("LB:CFG:VER:?\n".encode())
result_ver = port.readline().split(b":")
if len(result_rev) != 4 or len(result_ver) != 4:
    exit("Failed to communicate with LabBoard\nCheck wiring, baud rate, direction (PC), or try again")
# Print versions
print("LabBoard revision: ", int(result_rev[3]))
print("Firmware version: ", int(result_ver[3]))
##########################
## Application example code
##########################
print("Running...")
counter = 0
try:
    while True:
        port.write("LB:LED:{:x}\n".format(counter).encode())
        port.write("{}\n".format(counter).encode()) # Simply prints serial output if not a command
        counter += 1
        if counter > 0x7FF: counter = 0
        time.sleep(0.1)
# Exit on Ctrl+C
except KeyboardInterrupt:
    port.close()
    exit()
