#!/usr/bin/env python3

import asyncio
import numpy
from mavsdk import System


async def run():
    # Init the drone
    drone = System()
    await drone.connect(system_address="udp://:14540")

    # Start the tasks
    #asyncio.ensure_future(print_position(drone))
    await print_position(drone)
    #while True:
        #await asyncio.sleep(2)



async def print_position(drone):
    async for position in drone.telemetry.position():
        print(position.latitude_deg)
        print(position.longitude_deg)
        print(position.absolute_altitude_m)
        


if __name__ == "__main__":
    # Start the main function
    asyncio.run(run())