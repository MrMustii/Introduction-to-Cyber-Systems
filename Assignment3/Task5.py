from machine import Pin, PWM, ADC
import time
import neopixel

led = neopixel.NeoPixel(Pin(14), 2)



potentiometer=ADC(Pin(34))             #creating potentiometer object
potentiometer.width(potentiometer.WIDTH_9BIT)   #setting ADC resolution to 10 bit
potentiometer.atten(potentiometer.ATTN_11DB) 

while True:
  potentiometer_value=potentiometer.read()           #reading analog pin
  potentiometer_value=round(potentiometer_value/2)
  print(potentiometer_value)
  led[0] = (0, 0, potentiometer_value)
  led[1] = (0, 0, potentiometer_value)
  led.write()
  time.sleep(0.1)