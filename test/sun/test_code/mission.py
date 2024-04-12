#!/usr/bin/env python3

import asyncio

from mavsdk import System
from mavsdk.mission import (MissionItem, MissionPlan)
import time
class GpsModel():
    def __init__(self) -> None:
        self.latitude_deg=0.0
        self.longitude_deg=0.0
        self.absolute_altitude_m=0.0
        self.relative_altitude_m=0.0
    def set_gps(self,lat,log,abso,rel):
        self.latitude_deg=lat
        self.longitude_deg=log
        self.absolute_altitude_m=abso
        self.relative_altitude_m=rel
    def get_gps(self):
        return (self.latitude_deg,self.longitude_deg,self.absolute_altitude_m,self.relative_altitude_m)

async def run():
    drone = System()
    await drone.connect(system_address="udp://:14540")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"-- Connected to drone!")
            break

    print_mission_progress_task = asyncio.ensure_future(
        print_mission_progress(drone))

    running_tasks = [print_mission_progress_task]
    termination_task = asyncio.ensure_future(
        observe_is_in_air(drone, running_tasks))

    
    print("Waiting for drone to have a global position estimate...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("-- Global position estimate OK")
            break

    print("-- Arming")
    await drone.action.arm()
    flag=False

    mission_items = []
    mission_items.append(MissionItem(47.398039859999997,
                                    8.5455725400000002,
                                    25,
                                    10,
                                    True,
                                    float('nan'),
                                    float('nan'),
                                    MissionItem.CameraAction.NONE,
                                    float('nan'),
                                    float('nan'),
                                    float('nan'),
                                    float('nan'),
                                    float('nan'),
                                    MissionItem.VehicleAction.NONE))

    mission_plan = MissionPlan(mission_items)
    await drone.mission.set_return_to_launch_after_mission(False)

    print("-- Uploading mission")
    await drone.mission.upload_mission(mission_plan)

    print("-- Starting mission")
    await drone.mission.start_mission()
    await termination_task
    
async def get_gps(drone,gpsmodel:GpsModel) :
    async for position in drone.telemetry.position():
        gpsmodel.set_gps(position.latitude_deg,position.longitude_deg,position.absolute_altitude_m,
                                     position.relative_altitude_m)
    
async def print_mission_progress(drone):
    async for mission_progress in drone.mission.mission_progress():
        print("hello")


async def observe_is_in_air(drone, running_tasks):
    """ Monitors whether the drone is flying or not and
    returns after landing """

    was_in_air = False

    async for is_in_air in drone.telemetry.in_air():
        if is_in_air:
            was_in_air = is_in_air

        if was_in_air and not is_in_air:
            for task in running_tasks:
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass
            await asyncio.get_event_loop().shutdown_asyncgens()

            return


if __name__ == "__main__":
    # Run the asyncio loop
    asyncio.run(run())