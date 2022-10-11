# LabBoard serial control

## Dependencies

`pyserial` is required to run example scripts. Can be installed with:  
`pip install pyserial`

## Run examples

Specify correct port (same as selected in Arduino IDE -> Tools -> Port)  
To exit - press Ctrl+C  

**Windows:**  
`python3 .\display_voltage.py COM3`  
**macOS:**  
`python3 display_voltage.py /dev/cu.usbmodem`  
**Linux:**  
`python3 display_voltage.py /dev/ttyACM0`  

## Examples list

- **control_display.py** - outputs incrementing number to display and LED (binary)   
```bash
$ py .\control_display.py COM3
LabBoard revision:  23
Firmware version:  250
Running...
```
- **display_frequency.py** - view frequency measured on **DIG1** pin   
```bash
$ py .\display_frequency.py COM3
LabBoard revision:  23
Firmware version:  250
Pin DIG1:       Count   Frequency (Hz)
                0       0
```
- **display_voltage.py** - view voltages measured on **INPUTS** pins   
```bash
$ py .\display_voltage.py COM3
LabBoard revision:  23
Firmware version:  250
Voltages:       VIN     ±50V    ±5V     ±0.5V   SHUNT(mAmp)
                15.1    0.0     0.02    0.001   0.002
```
- **set_frequency.py** - control output frequency of **TXD** pin   
```bash
$ py .\set_frequency.py COM3
LabBoard revision:  23
Firmware version:  250
Frequency: 10 Hz
Period: 100000 μs
Pulse width: 50000 μs
Duty cycle: 50.0 %
Enter (Hz) (%): 50 25.8
Frequency: 50 Hz
Period: 20000 μs
Pulse width: 5160 μs
Duty cycle: 25.8 %
Enter (Hz) (%):
```