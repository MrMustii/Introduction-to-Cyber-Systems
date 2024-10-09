import machine
from machine import Pin
import network
import socket
import json

#initializing button and led
button = machine.Pin(15, Pin.IN, Pin.PULL_UP)
led = machine.Pin(12, Pin.IN)

#temperature
i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(23))

address = 24
temp_reg = 5
res_reg = 8

data = i2c.readfrom_mem(address, temp_reg, 2)

def temp_c(data):
    value = data[0] << 8 | data[1]
    temp = (value & 0xFFF) / 16.0
    if value & 0x1000:
        temp -= 256.0
    return temp

data = bytearray(2)
i2c.readfrom_mem_into(address, temp_reg, data) 

#web server setup
ap = network.WLAN (network.AP_IF)
ap.active (True)
ap.config (essid = 'ESPgroup32')
ap.config (authmode = 3, password = 'ANDERSISGAY')

pins = [machine.Pin(i, machine.Pin.IN) for i in (0, 2, 4, 5, 12, 13, 14, 15)]
print(pins)

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

    temp_cur = temp_c(i2c.readfrom_mem(address, temp_reg, 2))
    val = {
        "led": led.value(),
        "button": button.value(),
        "Temperature": temp_cur
    }

    while True:
        line = cl_file.readline()
        if "/pins" in line:
            del val["Temperature"]
            val = list(val.keys())
        elif "/sensors" in line:
            del val["led"]
            del val["button"]
            val = list(val.keys())
        elif "/pins/pin_name" in line:
            del val["Temperature"]
            val = list(val.values())
        elif "/sensors/sensor_name" in line:
            del val["led"]
            del val["button"]
            val = list(val.values())

        print(line)
        if not line or line == b'\r\n':
            break
    
    response = json.dumps(val)

    cl.send(response)
    cl.close()

