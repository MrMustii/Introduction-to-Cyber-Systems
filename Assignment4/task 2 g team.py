import machine, time
import network
import socket

#initializing the button
button = machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_UP)

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

#web browser display

print('listening on', addr)

while True:
        
    cl, addr = s.accept()
    print('client connected from', addr)
    cl_file = cl.makefile('rwb', 0)
    while True:
        
        line = cl_file.readline()
        #print(line)
        if not line or line == b'\r\n':
            break
    rows = ['<tr><td>%s</td><td>%d</td></tr>' % (str(p), p.value()) for p in pins]
    #
    button_cur = button.value()
    temp_cur = temp_c(i2c.readfrom_mem(address, temp_reg, 2))
    rows.append('<tr><td>Temperature</td><td>%d</td></tr>' % float(temp_cur))
    rows.append('<tr><td>Button</td><td>%d</td></tr>' % float(button_cur))
    #
    response = html % '\n'.join(rows)
    cl.send(response)
    cl.close()
    
    

