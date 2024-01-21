from .channel import Channel
import logging
logger = logging.getLogger()

class Record:
    def __init__(self, raw_data):
        basenum = int.from_bytes(raw_data[1:4]) #raw_data[1] << 16 + raw_data[2] << 8 + raw_data[3]
        self._temp = (basenum / 10000)
        self.humidity = (basenum % 1000) / 10
        self.battery = raw_data[4]

    @property
    def temp(self):
        return self._temp * (9/5) + 32

class Govee5075:
    def __init__(self, id:str):
        self.id = id
        self.channel = Channel(f'{id}.channel')
        self.record = None

    def update(self, record:Record):
        self.record = record

    def clear(self):
        self.record = None

    def publish(self):
        data = {}
        fid = self.channel.field_offset
        data[f'field{fid+1}'] = self.record.temp
        data[f'field{fid+2}'] = self.record.humidity
        data[f'field{fid+3}'] = self.record.battery
        logger.info(f'publish {self.id} -> {self.channel.channel_id} field[{fid+1}..{fid+3}]')
        self.channel.write(data)