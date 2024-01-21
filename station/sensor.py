import logging
import random
logger = logging.getLogger()

class Sensor():
    def __init__(self, name, field_map=None):
        logger.debug(f'Creating sensor {name}...')
        self.name = name
        self.last_sample = None
        self.thing = farm.Thing.Create(name, field_map)

    def read(self):
        self.last_sample = 0
        return self.last_sample

    def publish(self, flush=False):
        if self.thing is not None:
            return self.thing.publish(self.last_sample, flush)            
        return False

    def fetch(self):
        if self.thing is not None:
            field_map = self.thing.field_map
            if field_map is None:
                field_map = [*range(1,9)]

            result = []
            record = self.thing.read()
            logger.info(f'{type(record)}')
            logger.info(f'{record}')
            feeds = record['feeds']
            feed = feeds[0]
            for ii in field_map:
                f = f'field{ii}'
                if f in feed:
                    result.append(int(feed[f]))
                else:
                    result.append(None)
            return result
        return None

class RandomSensor(Sensor):
    def __init__(self, name, num_fields=3, field_map=None, sample_range=100):
        super().__init__(name, field_map)
        self.num_fields = num_fields
        self.sample_range = sample_range

    def read(self):
        ret = []
        for ii in range(self.num_fields):
            val = random.randrange(self.sample_range)
            ret.append(val)
        self.last_sample = ret
        return ret