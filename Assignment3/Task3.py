
import machine
import time
i2c=machine.I2C(scl=machine.Pin(22), sda=machine.Pin(23))
red = machine.Pin(27, machine.Pin.OUT)
orange = machine.Pin(33, machine.Pin.OUT)
green = machine.Pin(15, machine.Pin.OUT)
i2c.scan()


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

temp_c(data)
print(i2c.scan())
while True:
    read=temp_c(i2c.readfrom_mem(address, temp_reg, 2))
    if (read<23):
        red.on()
        green.off()
        orange.off()
        time.sleep(0.1)
    elif(read>=23 )and (read<25):
        red.off()
        green.on()
        orange.off()
        time.sleep(0.1)
    elif (read>=25):
        red.off()
        green.off()
        orange.on()
        time.sleep(0.1)
