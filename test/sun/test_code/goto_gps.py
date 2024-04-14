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
class GpsModel:
    def __init__(self) -> None:
        self.__latitude_deg=None #위도
        self.__longitude_deg=None #경도
        self.__absolute_altitude=None  
        self.__relative_altitude=None  #실제 높이 
    def set_gps(self,latitude,longitude,absolute,relative):
        self.__latitude_deg=latitude
        self.__longitude_deg=longitude
        self.__absolute_altitude=absolute
        self.__relative_altitude=relative
        

    def get_gps(self):
        return(self.__latitude_deg,self.__longitude_deg,self.__absolute_altitude,self.__relative_altitude)
    
def get_direction(start_lat, start_lon, end_lat, end_lon):
    # 위도와 경도의 차이 계산
    dlat = end_lat - start_lat
    dlon = end_lon - start_lon

    # x축과 y축 방향 계산
    x_distance = dlon * 111319.9 * cos(radians(start_lat))  # 1도의 경도 차이는 적도에서 약 111319.9 미터
    y_distance = dlat * 111319.9  # 1도의 위도 차이는 항상 약 111319.9 미터

    return x_distance, y_distance 
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
from math import radians, sin, cos, sqrt, atan2




def haversine(lat1, lon1, lat2, lon2):
    # 지구의 반지름 (미터 단위)
    R = 6371000.0

    # 라디안 변환
    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)

    # 위도와 경도의 차이
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Haversine 공식 계산
    a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # 거리 계산
    distance = R * c
    return distance

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
        
async def get_gps(drone,drone_model:GpsModel) :

    async for position in drone.telemetry.position():
        drone_model.set_gps(position.latitude_deg,position.longitude_deg,position.absolute_altitude_m,
                                    position.relative_altitude_m)
        
        
async def run():
    """ Does Offboard control using position NED coordinates. """

    drone = System()
    gps_mode=GpsModel()
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
    asyncio.ensure_future(get_gps(drone,gps_mode))
    
    print("-- Go 0m North, 0m East, -5m Down \
            within local coordinate system")
    await drone.offboard.set_position_ned(
            PositionNedYaw(0.0, 0.0, -5.0, 0.0))    
    await asyncio.sleep(10)
    data=gps_mode.get_gps() 
    latitude_s=data[0]
    longitude_s=data[1]
    await asyncio.sleep(1)
    #    + 북 - 남    /     +동 - 서      /    +up - donw    /  각도는 시계방향으로 
    print("-- Go 5m North, 0m East, -5m Down \
            within local coordinate system, turn to face East")
    await drone.offboard.set_position_ned (PositionNedYaw(5.0, 0.0, -5.0, 0.0))  
    await asyncio.sleep(10)
    
    
    
    #여기까지 움직였다고 치고
    while True:
        data_2=gps_mode.get_gps()
        latitude_d=data_2[0]
        longitude_d=data_2[1]
        #distance = get_distance(latitude_d,longitude_d,latitude_s,longitude_s)  #거리 계산 프로그램 
        print(f"도착지는 {latitude_s}   {longitude_s}  ",end="   ")
        print(f"현재 위치는 {latitude_d}   {longitude_d}")
        x,y=get_direction(latitude_d,longitude_d,latitude_s,longitude_s)
        print(f"x 축으로 {x}  만큼 y축으로 {y} 만큼 움직여야합니다.")
        #x,y=get_distance(latitude_d,longitude_d,latitude_s,longitude_s)
        #degree_number=get_bearing(latitude_d,longitude_d,latitude_s,longitude_s)

        await drone.offboard.set_position_ned(
            PositionNedYaw(y, x, -5.0,0.0))
        await asyncio.sleep(15)
        print("\n\n")
if __name__ == "__main__":
    # Run the asyncio loop
    asyncio.run(run())