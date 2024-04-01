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

    def run(self):
        camera_thread=Thread(target=self.__controller.run_camera)
        camera_thread.run()
        print('asdfadfs')
        self.__view.run()
        
        
    async def run_pilot(self) :
        await self.__controller.run_pilot()
        
if __name__=="__main__":
    main_function=Main()
    print("start")
    main_function.run()
    asyncio.run(main_function.run_pilot())
        
        
    