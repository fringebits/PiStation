import smbus
import farm
import logging
logger = logging.getLogger()

#
# Reference reading tmp102 device; https://github.com/n8many/TMP102py/blob/master/tmp102.py
#

_DEFAULT_ADDRESS = 0x48

_REG_TEMPERATURE = 0x00
_REG_CONFIG = 0x01
_REG_TLOW = 0x02
_REG_THIGH = 0x03

tempConvert = {
    'C': lambda x: x,
    'K': lambda x: x+273.15,
    'F': lambda x: x*9/5+32,
    'R': lambda x: (x+273.15)*9/5
}

tempConvertInv = {
    'C': lambda x: x,
    'K': lambda x: x-273.15,
    'F': lambda x: (x-32)*5/9,
    'R': lambda x: (x*5/9)-273.15
}

class Sensor_tmp102(farm.Sensor):
    def __init__(self, name, field_map=None, i2c_bus=1, i2c_address=_DEFAULT_ADDRESS):
        super().__init__(name, field_map)
        self.bus = smbus.SMBus(i2c_bus)
        self.i2c_address = i2c_address
        self._units = 'F'

    def read(self):
        data = self.read_i2c(_REG_TEMPERATURE, 2)
        tempC = self.bytesToTemp(data)
        result = tempConvert[self._units](tempC)
        logger.info(f'read: result=[{result}]')
        self.last_sample = [result]
        return self.last_sample

    def readConfig(self, num, location=0, length=0):
        data = self.read_i2c(_REG_CONFIG, 2)
        if (num == 3):
            #Full register dump
            return data
        else:
            mask = 2**length - 1
            return (data[num] >> location) & mask        

    def bytesToTemp(self, data):
        # Adjustment for extended mode
        ext = self.readConfig(1, 4, 1)
        #ext = data[1] & 0x01
        res = int((data[0] << (4+ext)) + (data[1] >> (4-ext)))

        if ((data[0] | 0x7F) == 0xFF):
            # Perform 2's complement operation (x = x-2^bits)
            res = res - 4096*(2**ext)
        # Outputs temperature in degC
        return res*0.0625


    # def write(self, buffer, start, end):
    #     if (end is None):
    #         end = len(buffer)

    #     # I can't tell if 'start' is the destination or the first byte in the buffer.
    #     # if it's the first byte in the buffer, what is the destination??

    #     return self._bus.write_i2c_block_data(self._address, start, list(buffer[:end]))

    def read_i2c(self, location, count):
        data = self.bus.read_i2c_block_data(self.i2c_address, location, count)
        logger.info(f'read_ic2: loc={location}, count={count}, data={data}')
        return data