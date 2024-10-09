##cd OneDrive/Desktop/cyber\ systems/ass3
##ampy --port /dev/ttyS3 --baud 115200 put Task1.py
##ampy --port /dev/ttyS3 --baud 115200 run Task1.py
import machine
import time
pin = machine.Pin(27, machine.Pin.OUT)

butt= machine.Pin(32, machine.Pin.IN, machine.Pin.PULL_DOWN)##connect as in task 2

while butt.value()==1:
    pin.on()
    time.sleep(0.5)
    pin.off()
    time.sleep(0.5)
