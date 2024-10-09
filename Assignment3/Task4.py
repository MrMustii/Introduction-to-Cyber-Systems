import machine
import time
import neopixel



i2c=machine.I2C(scl=machine.Pin(22), sda=machine.Pin(23))
np = neopixel.NeoPixel(machine.Pin(14), 8)
# i2c.scan()


address=24
temp_reg=5
res_reg=8

data=i2c.readfrom_mem(address, temp_reg, 2)
print(data)
data=bytearray(2)
i2c.readfrom_mem_into(address, temp_reg, data)
print(data)


def temp_c(data):
    value = data[0] << 8 | data[1]
    temp = (value & 0xFFF) / 16.0
    if value & 0x1000:
        temp -= 256.0
    return temp

while True:
    read=temp_c(i2c.readfrom_mem(address, temp_reg, 2))
    if (read<23):
        np[0] = (255, 0, 0)
        np[1] = (255, 0, 0)  
        np.write()
    elif(read>=23 )and (read<25):
        np[0] = (0, 128, 0)
        np[1] = (0, 128, 0)
        np.write()
    elif (read>=25):
        np[0] = (0, 0, 255)
        np[1] = (0, 0, 255)
        np.write()








    # np = neopixel.NeoPixel(machine.Pin(14), 2)
    
    # np[0] = (255, 0, 0) # set to red, full brightness
    # np[1] = (0, 128, 0) # set to green, half brightness
    # np.write()
    