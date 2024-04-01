import asyncio
from model.pilot_model import *
class PilotController:
    def __init__(self,pilotmodel:PilotModel) -> None:
        self.__pilot_model=pilotmodel  
        self.__drone=Drone()
        
    async def init_dron(self):
        await self.__drone.make_drone()
        pass
    
    def __recv_data(self,key,mode): #master 부터 recv해서 드론 컨트롤 하는 부분 
        self.__pilot_model.set_data(key,mode)
    
    async def run(self):
        while True:
            (key,mode)=self.__pilot_model.get_data()
            (yaw,throttle,roll,pitch)=key.get_key()
            print(throttle)
            if(mode==0):
                await self.__drone.get_drone().manual_control.set_manual_control_input(pitch,yaw,throttle,roll)
              
        