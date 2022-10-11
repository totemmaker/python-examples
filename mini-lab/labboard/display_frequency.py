#! /usr/bin/env python3

# Example to display measured frequency of LabBoard DIG1 pin
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
# Start frequency measure module on DIG1 pin
port.write("LB:RXD:RUN:1\n".encode())
# Start listening for frequency change
port.write("LB:RXD:!\n".encode())
# Single read all values
port.write("LB:RXD:?\n".encode())
# Commands list
commands = {
    b"CNT" : ["Count", 0],
    b"FHZ" : ["Frequency", 0],
}
print("Pin DIG1:\tCount\tFrequency (Hz)")
try:
    while True:
        result = port.readline().split(b":")
        # Check if command format is correct
        if len(result) != 4:
            continue
        # Check if frequency command received
        if result[2] not in commands:
            continue
        # Store updated value
        try:
            commands[result[2]][1] = int(result[3])
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
