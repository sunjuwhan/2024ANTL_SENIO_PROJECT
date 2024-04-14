#!/usr/bin/env python3

"""
Caveat when attempting to run the examples in non-gps environments:

`drone.offboard.stop()` will return a `COMMAND_DENIED` result because it
requires a mode switch to HOLD, something that is currently not supported in a
non-gps environment.
"""

import asyncio

from mavsdk import System
from mavsdk.offboard import (OffboardError, PositionNedYaw)
from math import radians, sin, cos, sqrt, atan2, degrees

def get_distance(lat1, lon1, lat2, lon2):
    # 지구의 반지름 (미터 단위)
    R = 6371000.0

    # 위도 및 경도를 라디안으로 변환
    lat1_rad, lon1_rad, lat2_rad, lon2_rad = map(radians, [lat1, lon1, lat2, lon2])

    # 두 지점 간의 차이를 계산
    delta_lon = lon2_rad - lon1_rad
    delta_lat = lat2_rad - lat1_rad

    # x축과 y축으로의 거리 계산
    x = R * delta_lon * cos((lat1_rad + lat2_rad) / 2)
    y = R * delta_lat

    return x, y

def get_bearing(lat1, lon1, lat2, lon2):
    # 위도 및 경도를 라디안으로 변환
    lat1_rad, lon1_rad, lat2_rad, lon2_rad = map(radians, [lat1, lon1, lat2, lon2])

    # 두 점을 기준으로 하는 벡터의 각도를 계산
    delta_lon = lon2_rad - lon1_rad
    y = sin(delta_lon) * cos(lat2_rad)
    x = cos(lat1_rad) * sin(lat2_rad) - sin(lat1_rad) * cos(lat2_rad) * cos(delta_lon)
    bearing_rad = atan2(y, x)

    # 라디안 값을 도 단위로 변환하여 반환
    bearing_deg = degrees(bearing_rad)
    # 음수 값 처리
    bearing_deg = (bearing_deg + 360) % 360

    return bearing_deg

# # 예시 좌표
# lat1 = 37.7749
# lon1 = -122.4194
# lat2 = 34.0522
# lon2 = -118.2437

# x_distance, y_distance = get_distance(lat1, lon1, lat2, lon2)
# bearing = get_bearing(lat1, lon1, lat2, lon2)
# print("두 지점 간의 각도는 {:.2f} 도입니다.".format(bearing))
# print("x축으로 {:.2f} 미터, y축으로 {:.2f} 미터 이동해야 합니다.".format(x_distance, y_distance))
async def get_gps(drone,latitude,longitude,absoulte_altitude,relative_altitude):
    async for position in drone.telemetry.position():
        latitude=position.latitude_deg
        longitude=position.longitude_deg
        absoulte_altitude=position.absolute_altitude_m
        relative_altitude=position.relative_altitude_M
        
async def run():
    """ Does Offboard control using position NED coordinates. """

    drone = System()
    await drone.connect(system_address="udp://:14540")

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
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, 0.0, 0.0))

    print("-- Starting offboard")
    try:
        await drone.offboard.start()
    except OffboardError as error:
        print(f"Starting offboard mode failed \
                with error code: {error._result.result}")
        print("-- Disarming")
        await drone.action.disarm()
        return
    latitude_s=0
    longitude_s=0
    absolute_altitude_s=0
    relative_altitude_s=0
    get_gps(drone,latitude_s,longitude_s,absolute_altitude_s,relative_altitude_s) 
    print("-- Go 0m North, 0m East, -5m Down \
            within local coordinate system")
    await drone.offboard.set_position_ned(
            PositionNedYaw(0.0, 0.0, -5.0, 0.0))    
    await asyncio.sleep(10)
    #    + 북 - 남    /     +동 - 서      /    +up - donw    /  각도는 시계방향으로 
    print("-- Go 5m North, 0m East, -5m Down \
            within local coordinate system, turn to face East")
    await drone.offboard.set_position_ned(
            PositionNedYaw(5.0, 0.0, -5.0, 90.0))
    await asyncio.sleep(10)
    #여기까지 움직였다고 치고

    while True:
        latitude_d=0
        longitude_d=0
        absolute_altitude_d=0
        relative_altitude_d=0
        get_gps(drone,latitude_d,longitude_d,absolute_altitude_d,relative_altitude_d)
        x,y=get_distance(latitude_s,longitude_s,latitude_d,longitude_d)
        degree_number=get_bearing(latitude_s,longitude_s,latitude_d,longitude_d)
        print(f"x:  {x}  y:  {y}   degree:  {degree_number}")
        await drone.offboard.set_position_ned(
            PositionNedYaw(y, x, -5.0, degree_number))
        await asyncio.sleep(10)
if __name__ == "__main__":
    # Run the asyncio loop
    asyncio.run(run())