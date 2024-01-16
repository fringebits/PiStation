


class EscDevice:
    def __init__(self, bus, address):
        self._bus = bus
        self._address = address

    def write(self, buffer, start, end):
        self._bus.write_i2c_block_data(self._address, )
        return 0

    def readinto(self, buffer):
        count = len(buffer)
        self._bus.read_i2c_block_data(self._address, 0, count)
        return 0