#!/usr/bin/env python3

import asyncio
import numpy
from sun_mavsdk import System


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
        print(position.get_gps())
        asyncio.sleep(1)


if __name__ == "__main__":
    # Start the main function
    asyncio.run(run())