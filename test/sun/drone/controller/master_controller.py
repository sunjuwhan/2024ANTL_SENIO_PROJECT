from controller.pilot_controller import *
from controller.camera_controller import *
from model.pilot_model import *
from model.video_mode import *
class MasterController():
    def __init__(self,pilot_model:PilotModel,video_model:VideoModel) :
        self.__pilot_controller=None
        self.__pilot_model=pilot_model
        self.__camera_model=video_model
        self.__camera_controller=CameraController(self.__camera_model)
   
    def get_camera(self):
        while True:
            print('1')
            time.sleep(1)
    def run_camera(self):
        print("run_camera 1")
        self.__camera_controller.run()
    async def run_pilot(self):    #asyncio .run()으로 실행하고 나머지는 thread로 실행해야할거같은데
        try:
            self.__pilot_controller=PilotController(self.__pilot_model)
            await self.__pilot_controller.init_dron()
            await self.__pilot_controller.run()
        except Exception as E:
            print(E)
            print("Asynci did Bad action !! __run_pilot")
        