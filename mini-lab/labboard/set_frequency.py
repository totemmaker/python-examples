#! /usr/bin/env python3

# Example to control LabBoard frequency generator
# Allows to enter frequency and duty cycle
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
# Start start output on TXD pin
port.write("LB:TXD:RUN:1\n".encode())
# Commands list
commands = {
    b"FHZ" : ["Frequency", "Hz", 0],
    b"FUS" : ["Period", "μs", 0],
    b"DUS" : ["Pulse width", "μs", 0],
    b"DPCT" : ["Duty cycle", "%", 0],
}
try:
    while True:
        # Single read all values
        port.write("LB:TXD:?\n".encode())
        # Read received values
        updated = False
        while True:
            result = port.readline().split(b":") # Will timeout after 0.5s
            # Stop if no correct result read
            if len(result) != 4:
                break
            # Check if valid command received
            if result[2] not in commands:
                continue
            # Store updated value
            try:
                commands[result[2]][2] = int(result[3])
                updated = True
            except:
                continue
        # Print stored values if anything new was received
        if updated:
            for v in commands:
                if v == b"DPCT":
                    print("{}: {} {}".format(commands[v][0], commands[v][2]/10, commands[v][1]))
                else:
                    print("{}: {} {}".format(commands[v][0], commands[v][2], commands[v][1]))
        # Read new frequency and duty input
        params = input("Enter (Hz) (%): ").split()
        # Wait for 2 value input
        if len (params) != 2:
            continue
        try:
            freq = int(params[0])
            duty = float(params[1])
            duty = int(duty * 10) # Convert to required format
            port.write("LB:TXD:FHZ:{}\n".format(freq).encode())
            port.write("LB:TXD:DPCT:{}\n".format(duty).encode())
        except:
            print("Bad input")
            continue
# Exit on Ctrl+C
except KeyboardInterrupt:
    port.close()
    exit()
