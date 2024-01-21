import logging
from .sensor_govee5075 import Govee5075, Record
logger = logging.getLogger()

sensors = {}

def update(name:str, data:Record):
    if not name in sensors:
        sensors[name] = Govee5075(name)    
    sensors[name].update(data)

def clear():
    sensors.clear()

def publish():
    for sensor in [sensors[k] for k in sensors if sensors[k] is not None]:
        sensor.publish()
    
