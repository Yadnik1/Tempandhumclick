from machine import I2C, Pin
import time
import os

class HTU21D(object):
    ADDRESS = 0x40
    ISSUE_TEMP_ADDRESS = 0xE3
    ISSUE_HU_ADDRESS = 0xE5

    def __init__(self, scl, sda):
         self.i2c = I2C("I2C_0")
         scl=Pin(("GPIO_0", 25), Pin.IN)
         sda=Pin(("GPIO_0", 26), Pin.IN)



    def _crc_check(self, value):
       
        remainder = ((value[0] << 8) + value[1]) << 8
        remainder |= value[2]
        divsor = 0x988000

        for i in range(0, 16):
            if remainder & 1 << (23 - i):
                remainder ^= divsor
            divsor >>= 1

        if remainder == 0:
            return True
        else:
            return False

    def _issue_measurement(self, write_address):
        
        self.i2c.start()
        self.i2c.writeto_mem(int(self.ADDRESS), int(write_address), '')
        self.i2c.stop()
        time.sleep_ms(50)
        data = bytearray(3)
        self.i2c.readfrom_into(self.ADDRESS, data)
        if not self._crc_check(data):
            raise ValueError()
        raw = (data[0] << 8) + data[1]
        raw &= 0xFFFC
        return raw

    
    def temperature(self):
        
        raw = self._issue_measurement(self.ISSUE_TEMP_ADDRESS)
        return -46.85 + (175.72 * raw / 65536)

   
    def humidity(self):
       
        raw =  self._issue_measurement(self.ISSUE_HU_ADDRESS)
        return -6 + (125.0 * raw / 65536)

    def test(self):
        print("Working")
        
    
htu = HTU21D(25,26)
hum = htu.humidity()
temp = htu.temperature()
print(hum)
print(temp)
