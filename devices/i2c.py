import smbus

class Bus:
    def __init__(self, bus_index):
        self._index = bus_index
        self._bus = smbus.SMBus(self._index)
