from model import *
import asyncio
class GpsController:
    def __init__(self,model:GpsModel,drone:Drone) -> None:
        self.__gps_mode=model
        self.__drone=drone
        
    async def run_gps(self):
        async for position in self.__drone.telemetry.position():
            print(position.latitude_deg,position.longitude_deg)
            self.__gps_mode.set_gps(position.latitude_deg,position.longitude_deg,position.absolute_altitude_m,position.relative_altitude_m)
            
            
            
            
    