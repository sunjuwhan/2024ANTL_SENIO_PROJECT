import controller
import model
import view 
import asyncio
from threading import *
class Main():
    def __init__(self) -> None:

        self.__pilot_model=model.PilotModel()
        self.__camera_model=model.VideoModel()
        self.__controller=controller.MasterController(self.__pilot_model,self.__camera_model)
        self.__view= view.SocketView(self.__pilot_model,self.__camera_model)

    async def run(self):
        camera_thread=Thread(target=self.__controller.run_camera())
        self.__view.run()
        asyncio.run(self.__controller.run_pilot())
    
    
if __name__=="__main__":
    main_function=Main()
    main_function.run()
        
        
    