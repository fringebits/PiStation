import farm
import logging
logger = logging.getLogger()

# represents an array of sensors to sample
class SensorArray:
    def __init__(self):
        self.array = []
        self.samples = []

    def append(self, sensor:farm.Sensor):
        self.array.append(sensor)

    def read(self):
        ret = []
        for s in self.array:
            ret.append(s.read())
        return ret

    def publish(self):
        for s in self.array:
            s.publish()