import json
import thingspeak
import logging
logger = logging.getLogger()

class Channel:
    def __init__(self, filename:str):
        self.channel_id = None
        self.read_key = None
        self.write_key = None
        self.field_offset = 0
        if filename is not None:
            self.load(filename)

    def write(self, data):        
        ch = thingspeak.Channel(self.channel_id, self.write_key)
        ch.update(data)

    def load(self, filename:str):
        try:
            logger.info(f'loading channel config {filename}')
            with open(filename) as f:
                config = json.load(f)
                self.channel_id = config['channel_id'] if 'channel_id' in config else None
                self.read_key = config['read_key'] if 'read_key' in config else None
                self.write_key = config['write_key'] if 'write_key' in config else None
                self.field_offset = config['field_offset'] if 'field_offset' in config else 0
                                             
        except FileNotFoundError:
            logger.error(f'Channel config file not found ({filename})')
            pass
