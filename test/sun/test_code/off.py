#!/usr/bin/env python3

# Warning: Only try this in simulation!
#          The direct attitude interface is a low level interface to be used
#          with caution. On real vehicles the thrust values are likely not
#          adjusted properly and you need to close the loop using altitude.

import asyncio

from mavsdk import System
from mavsdk.offboard import (Attitude, OffboardError)
import socket

sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind(("192.168.232.137",5001))

async def run():
    """ Does Offboard control using attitude commands. """

    drone = System()
    await drone.connect(system_address="serial:///dev/ttyAMA0")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"-- Connected to drone!")
            break

    print("Waiting for drone to have a global position estimate...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("-- Global position estimate OK")
            break

    print("-- Arming")
    await drone.action.arm()

    print("-- Setting initial setpoint")
    await drone.offboard.set_attitude(Attitude(0.0, 0.0, 0.0, 0.0))

    print("-- Starting offboard")
    try:
        await drone.offboard.start()
    except OffboardError as error:
        print(f"Starting offboard mode failed with error code: \
              {error._result.result}")
        print("-- Disarming")
        await drone.action.disarm()
        return
    while True:
        data=sock.recv(100)
        data=data.decode()
        yaw=data[0]
        throttle=data[1]
        roll=data[2]
        pitch=data[3]
        print(roll," ",pitch," ",yaw," ",throttle) #roll ? ? throttle
        await drone.offboard.set_attitude(Attitude(roll, pitch, yaw, throttle))
        await asyncio.sleep(0.1)



if __name__ == "__main__":
    # Run the asyncio loop
    asyncio.run(run())