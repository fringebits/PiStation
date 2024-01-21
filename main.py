import asyncio
import logging 
import argparse
import time
from bleak import BleakScanner
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData

logger = logging.getLogger()

import station

def print_bytes(data):    
    print(f"Raw Data = ({len(data)}) {data}")
    print(" ".join(hex(n) for n in data))

def device_found(device: BLEDevice, advertisement_data: AdvertisementData):
    try:
        raw_data = advertisement_data.manufacturer_data[0xEC88]
        print_bytes(raw_data)
        data = station.Record(raw_data)

        station.station.update(device.name, data)
        
        print(f"# Device Found: {device}")
        print(f"Temp     : {data.temp}")
        print(f"Humidity : {data.humidity}")
        print(f"Battery  : {data.battery}")
        print(f"RSSI     : {advertisement_data.rssi} dBm")
        print(47 * "-")

    except KeyError:
        # Apple company ID (0x004c) not found
        pass

async def main():
    parser = argparse.ArgumentParser()
    #parser.add_argument("--debug", help="Debug mode, forces use of windows", action="store_true")
    parser.add_argument("--delay", help="Num seconds to delay between samples", type=int, default=15)
    args = parser.parse_args()

    station.init_logs()
    logger.info("PiStation v1.0")

    try:
        scanner = BleakScanner(detection_callback=device_found)

        while True:
            logger.info("Scanning stations...")            
            station.clear()
            await scanner.start()
            await asyncio.sleep(10.0)
            await scanner.stop()
            station.publish()

            time.sleep(args.delay)
            #await asyncio.sleep(60.0)

    finally:
        logger.info("Station is DOWN")
        #station.Slack.send('Station is DOWN')

if __name__ == "__main__":
    asyncio.run(main())
