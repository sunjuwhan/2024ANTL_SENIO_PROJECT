import asyncio
from model.pilot_model import *
from model.gps_model import *
class PilotController:
    def __init__(self,pilotmodel:PilotModel,gpsmodel:GpsModel) -> None:
        self.__pilot_model=pilotmodel  
        self.__drone=Drone()
        self.__gps_model= gpsmodel
    async def init_dron(self):  #자자 이친구 잘 꺼내씁니다. return 해서 써 
        await self.__drone.make_drone()
        pass
    def get_dron_from_controller(self):
        return self.__drone.get_drone()
    
    
    
    def __recv_data(self,key,mode): #master 부터 recv해서 드론 컨트롤 하는 부분 
        self.__pilot_model.set_data(key,mode)
        
        
    async def get_gps(self) :

        async for position in self.__drone.get_drone().telemetry.position():
            self.__gps_model.set_gps(position.latitude_deg,position.longitude_deg,position.absolute_altitude_m,
                                     position.relative_altitude_m)
            
            
    async def run(self):
        while True:
            (key,mode)=self.__pilot_model.get_data()
            (yaw,throttle,roll,pitch)=key.get_key()
            asyncio.ensure_future(self.get_gps())
            
            
            if (mode=="arm"):
                print("-- Arming")
                await self.__drone.get_drone().action.arm()
                await asyncio.sleep(2)

            elif (mode=="takeoff") :
                print("--  Takeoff")
                await self.__drone.get_drone().action.takeoff()
                await asyncio.sleep(1)

            elif (mode=="land"):
                print("-- land")
                await self.__drone.get_drone().action.land()
             
            elif (mode=="manual"):
                await self.__drone.get_drone().manual_control.set_manual_control_input(pitch,roll,throttle,yaw)
            elif (mode=="gps") : #gps mode
                (go_a,go_b,go_c,go_d)=(self.__gps_model.get_gps())
                while True:
                    (key,mode)=self.__pilot_model.get_data()
                    if(mode!="1") :
                        break
                    await self.__drone.get_drone().goto_location(go_a,go_b,go_c,go_d)
        