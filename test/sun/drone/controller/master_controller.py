from controller.pilot_controller import *
from controller.camera_controller import *
from controller.gps_controller import  *
from model.pilot_model import *
from model.video_mode import *
from model.gps_model import *
class MasterController():
    def __init__(self,pilot_model:PilotModel,video_model:VideoModel,gps_model:GpsModel) : 
        self.__pilot_controller=None
        self.__pilot_model=pilot_model
        self.__camera_model=video_model
        self.__gps_model=gps_model
        self.__drone=None
        self.__camera_controller=CameraController(self.__camera_model)
        self.__gps_controller=None
    def run_camera(self):
        self.__camera_controller.run()
    async def run_pilot(self):    #asyncio .run()으로 실행하고 나머지는 thread로 실행해야할거같은데
        try:
            self.__pilot_controller=PilotController(self.__pilot_model,self.__gps_model)
            await self.__pilot_controller.init_dron()
            self.__drone=self.__pilot_controller.get_dron_from_controller()  
            self.__gps_controller=GpsController(self.__gps_model,self.__drone) #만든 드론을 넣고 
            await self.__gps_controller.run_gps()  #gps 시작하고 
            await self.__pilot_controller.run()  #controller 시작하고 
        except Exception as E:
            print(E)
            print("Asynci did Bad action !! __run_pilot")
        