#! /usr/bin/env python3

# Example to display measured voltage of LabBoard voltage inputs
# Serial protocol available at: https://docs.totemmaker.net/labboard/serial/protocol/
import sys
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
# Start listening for voltage input
port.write("LB:IN:!\n".encode())
# Single read all values
port.write("LB:IN:?\n".encode())
# Commands list
commands = {
    b"VIN" : ["VIN", 0],
    b"50V" : ["±50V", 0],
    b"5V" : ["±5V", 0],
    b"05V" : ["±0.5V", 0],
    b"AMP" : ["SHUNT", 0],
}
print("Voltages:\tVIN\t±50V\t±5V\t±0.5V\tSHUNT(mAmp)")
try:
    while True:
        result = port.readline().split(b":")
        # Check if command format is correct
        if len(result) != 4:
            continue
        # Check if voltage command received
        if result[2] not in commands:
            continue
        # Store updated value
        try:
            commands[result[2]][1] = int(result[3])/1000
        except:
            continue
        # Refresh value display
        print("\r", end="\x1b[2K\t")
        for v in commands:
            print("\t{}".format(commands[v][1]), end="")
# Exit on Ctrl+C
except KeyboardInterrupt:
    port.close()
    exit()
