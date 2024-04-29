import asyncio
from model.pilot_model import *
from model.gps_model import *
import time
from mavsdk.offboard import (OffboardError, PositionNedYaw)
class PilotController:
    def __init__(self,pilotmodel:PilotModel,gpsmodel:GpsModel) -> None:
        self.__pilot_model=pilotmodel  
        self.__drone=Drone()
        self.__gps_model= gpsmodel
        self.flag_arm=""

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
        time.sleep(3)
        while True:
            (key,mode)=self.__pilot_model.get_data()
            (yaw,throttle,roll,pitch)=key.get_key()
            #print(mode,"  ",yaw,throttle,roll,pitch)
            #asyncio.ensure_future(self.get_gps())
            if (mode=="arm"):
                try:
                    if self.flag_arm!="arm":
                        print("-- Arming")
                        await self.__drone.get_drone().action.arm()
                        await asyncio.sleep(3)
                        self.__pilot_model.set_drone_state("arm")
                        print("-- success Arming") 
                        self.flag_arm="arm"
                except Exception as e:
                    print(e)
            elif (mode=="takeoff") :
                try:
                    print("--  Takeoff")
                    await self.__drone.get_drone().action.takeoff()
                    await asyncio.sleep(3)
                    print(" --sucesse takeoff") 
                except Exception as e:
                    print(e)
            elif (mode=="land"):
                try:
                    if self.flag_arm!="land":
                        print("-- land")
                        await self.__drone.get_drone().action.land()
                        await asyncio.sleep(5)
                        print("-- success landing")
                        self.__pilot_model.set_drone_state("land")  #착륙이 완료되었다는 신호를 보내줘
                        self.flag_arm=="land" 
                except Exception as e:
                    print(e)
            #elif( mode=="disarm"):
            #    try:
            #        print("--disarm")
            #        await self.__drone.get_drone().action.disarm()
            #        await   asyncio.sleep(5)
            #        self.__pilot_model.set_drone_state("off")

            #    except Exception as e:
            #        print(e)
            elif (mode=="manual"):
                try:
                    if throttle==1.0:
                       throttle=0.8 
                    await self.__drone.get_drone().manual_control.set_manual_control_input(pitch,roll,throttle,yaw)
                except Exception as e:
                    await self.__drone.get_drone().manual_control.set_manual_control_input(0.0,0.0,0.5,0.0)
                    await asyncio.sleep(0.1)
                    print(e)
            elif (mode=="gps") : #gps mode
                now_latitude =self.__gps_model.get_gps()[0]
                now_longitude=self.__gps_model.get_gps()[1]
                now_height=self.__gps_model.get_gps()[3]
                try:
                    await self.__drone.get_drone().offboard.set_position_ned(PositionNedYaw(0.0,0.0,0.0,0.0))  #setting 하는 곳 
                    await self.__drone.get_drone().offboard.start() #순서 바꿔봤음
                except OffboardError as error:
                    print(f"Starting offboard mode failed \
                    with error code: {error._result.result}")
                    await self.__drone.get_drone().action.land()
                y=0
                x=0
                while True:
                    (a,chk_now_mode)=self.__pilot_model.get_data()
                    if(chk_now_mode!="gps"):
                        try:
                            await self.__drone.get_drone().offboard.stop()
                            await asyncio.sleep(1)
                            print("Success stop offboard")
                        except Exception as e:
                            print(e)
                    await self.__drone.get_drone().offboard.set_position_ned(PositionNedYaw
                        (self.__gps_model.get_direction(self.__gps_model.get_gps()[0],self.__gps_model.get_gps()[1],now_latitude,now_longitude)[1], 
                        self.__gps_model.get_direction(self.__gps_model.get_gps()[0],self.__gps_model.get_gps()[1],now_latitude,now_longitude)[0], -5.0,0.0)) 
                    #높이는 -5로 고정하고 
                    await asyncio.sleep(5)
                    x,y=self.__gps_model.get_direction(self.__gps_model.get_gps()[0],self.__gps_model.get_gps()[1],now_latitude,now_longitude)
                    print(f"x 축으로 {x}  만큼 y축으로 {y} 만큼 움직여야합니다.")