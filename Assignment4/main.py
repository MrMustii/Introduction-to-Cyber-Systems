##cd OneDrive/Desktop/cyber\ systems/ass4
##ampy --port /dev/ttyS3 --baud 115200 put server.py
##ampy --port /dev/ttyS3 --baud 115200 run server.py

##putty com3 
##115200
##ctrl +e
##right click
##ctrl d

##main.py if it works
##os.remove("test.txt")


#import needed packages
import machine
import network
import socket
import json
import neopixel

ap = network.WLAN (network.AP_IF)
ap.active (True)
ap.config (essid = 'MustafaNet')
ap.config (authmode = 3, password = 'something')

##pins used
pins = [machine.Pin(i, machine.Pin.IN) for i in (14,33,22,23,34)]
button = machine.Pin(33, machine.Pin.IN, machine.Pin.PULL_UP)
potentiometer=machine.ADC(machine.Pin(34))
potentiometer.width(potentiometer.WIDTH_9BIT)
potentiometer.atten(potentiometer.ATTN_11DB)
led= neopixel.NeoPixel(machine.Pin(14), 1)
led[0]=(250,0,0)


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

###for temp
i2c=machine.I2C(scl=machine.Pin(22), sda=machine.Pin(23))
address=24
temp_reg=5
data=i2c.readfrom_mem(address, temp_reg, 2)
def temp_c(data):
    value = data[0] << 8 | data[1]
    temp = (value & 0xFFF) / 16.0
    if value & 0x1000:
        temp -= 256.0
    return temp




print('listening on', addr)

while True:
    cl, addr = s.accept()
    print('client connected from', addr)
    cl_file = cl.makefile('rwb', 0)
    path=''

    while True:
        line = cl_file.readline()
        line1=str(line)
        path=path+line1
        pot_val=potentiometer.read()
        Temp=temp_c(i2c.readfrom_mem(address, temp_reg, 2))
        if not line or line == b'\r\n':
            break
    Data={
        "led":led[0],
        "button": button.value(),
        "temperature":Temp,
        "potentiometer":pot_val
    }
    sense=Data
    path_list = path.split('/')
    print(path_list)
    if ("pins"in path_list and not ("button" in path_list or "led" in path_list or"potentiometer" in path_list or "temperature" in path_list or"pin14")) :
        sense=Data
        del sense["temperature"]
        sense=list(sense.keys())

    elif ("pins" in path_list and "button" in path_list) :
        sense=Data
        del sense["temperature"]
        del sense["led"]
        del sense["potentiometer"]
        sense=list(sense.values())

    elif "pins" in path_list and "led"in path_list:
        sense=Data
        del sense["temperature"]
        del sense["button"]
        del sense["potentiometer"]
        sense=list(sense.values())
        
    elif "pins"in path_list and "potentiometer"in path_list:
        sense=Data
        del sense["temperature"]
        del sense["button"]
        del sense["led"]
        sense=list(sense.values())

    elif "sensors" in path_list and not "temperature"in path_list:
        sense=Data
        del sense["potentiometer"]
        del sense["button"]
        del sense["led"]
        sense=list(sense.keys())

    elif "temperature" in path_list and  "sensors" in path_list:
        sense=Data
        del sense["potentiometer"]
        del sense["button"]
        del sense["led"]
        sense=list(sense.values())
    
    elif "setcolor"in path_list and "pins"  and "pin14"  in path_list:
        index=path_list.index("setcolor")
        print(index)
        firstnumber=int(path_list[index+1])
        print(firstnumber)
        secondnumber=int(path_list[index+2])
        thirdnumber=int(path_list[index+3])
        led[0]=(firstnumber,secondnumber,thirdnumber)
        led.write()
    
    

    elif "sethigh" in path_list and "pins" in path_list and "pin14" in path_list:
        sense=Data
        led[0]=(100,150,200)
        led.write()
        del sense["temperature"]
        del sense["button"]
        del sense["potentiometer"]
        sense=list(sense.values())
        

    elif "setlowhigh" in path_list and "pins" in path_list and "pin14"  in path_list:
        sense=Data
        led[0]=(0,0,0)
        led.write()
        del sense["temperature"]
        del sense["button"]
        del sense["potentiometer"]
        sense=list(sense.values())
        
    print("                ")
    print(path)
    print(path_list)
    print("                ")
    rows = ['<tr><td>%s</td><td>%d</td></tr>' % (str(p), p.value()) for p in pins]
    rows.append('<tr><td>Temperature</td><td>%d</td></tr>' % float(Temp))
    rows.append('<tr><td>potentiometer</td><td>%d</td></tr>' % float(pot_val))
    rows.append('<tr><td>button_val</td><td>%d</td></tr>' % button.value())   
    response = html % '\n'.join(rows)    
    response=json.dumps(sense)
    cl.send(response)
    cl.close()


