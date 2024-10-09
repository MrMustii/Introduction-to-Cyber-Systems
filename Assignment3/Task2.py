##pull down resistor 

import machine
import time

red = machine.Pin(27, machine.Pin.OUT)
orange = machine.Pin(33, machine.Pin.OUT)
green = machine.Pin(15, machine.Pin.OUT)

butt= machine.Pin(32, machine.Pin.IN, machine.Pin.PULL_DOWN)

green.on()
while True:
    if butt.value()==1:
        if green.value()==1:
            while butt.value()==1:
                green.off()
                orange.on()
        elif orange.value()==1:
            while butt.value()==1:
                orange.off()
                red.on()
        elif red.value()==1:
            while butt.value()==1:
                red.off()
                green.on()
    