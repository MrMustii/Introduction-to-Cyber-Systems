import machine
import network
import socket
import json

# Button
BUTTON = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_UP)  

# Potentiometer
POTENTIOMETER = machine.ADC(machine.Pin(32))                    
POTENTIOMETER.width(machine.ADC.WIDTH_10BIT)
POTENTIOMETER.atten(machine.ADC.ATTN_11DB)

# Temperature
I2C = machine.I2C(scl = machine.Pin(22), sda = machine.Pin(23)) 
DATA = I2C.readfrom_mem(24, 5, 2)    

def CELSIUS(DATA):                                                 
    VALUE = (DATA[0] << 8 | DATA[1])
    TEMPERATURE = (VALUE & 0xFFF) / 16.0
    if VALUE & 0x1000:
        TEMPERATURE = -256
    return TEMPERATURE

DATA = bytearray(2)                                           
I2C.readfrom_mem_into(24, 5, DATA)

# Server
ap = network.WLAN (network.AP_IF)
ap.active (True)
ap.config (essid = 'GROUP-16')
ap.config (authmode = 3, password = 'password1')

pins = [machine.Pin(i, machine.Pin.IN) for i in (0, 2, 4, 5, 12, 13, 14, 15)]

html = """<!DOCTYPE html>
<html>
    <head> <title>ESP32 Pins</title> </head>
    <body> <h1>ESP32 Pins</h1>
        <table border="1"> <tr><th>Pin</th><th>Value</th></tr> %s </table>
    </body>
</html>
"""

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

print('listening on', addr)

while True:
    cl, addr = s.accept()
    print('client connected from', addr)
    cl_file = cl.makefile('rwb', 0)
    
    p = [(str(p), p.value()) for p in pins]
    button = BUTTON.value()
    temp = CELSIUS(I2C.readfrom_mem(24, 5, 2))
    potentiometer = round(POTENTIOMETER.read() / 4.01) 
    JSON_VALUES = {"Pins": p, "Button": button, "Temperature": temp, "Potentiometer": potentiometer}
    
    while True:
        line = cl_file.readline()
        if "/pins" in line:
            del JSON_VALUES["Button"]
            del JSON_VALUES["Potentiometer"]
            JSON_VALUES = list(JSON_VALUES.key()) 
            
        elif "/sensors" in line:
            del JSON_VALUES["Temperature"]
            JSON_VALUES = list(JSON_VALUES.key()) 
            
        elif "/pins/pin_name" in line:
            del JSON_VALUES["Button"]
            del JSON_VALUES["Potentiometer"]
            JSON_VALUES = list(JSON_VALUES.values())  
            
        elif "/sensors/sensor_name" in line:
            del JSON_VALUES["Temperature"]
            JSON_VALUES = list(JSON_VALUES.values())
        
        print(line)
        if not line or line == b'\r\n':
            break
    
    response = json.dumps(JSON_VALUES)
    cl.send(response)
    cl.close()
