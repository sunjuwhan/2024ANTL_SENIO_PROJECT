import time
from model.video_mode import *
class CameraController():
    def __init__(self,model:VideoModel) -> None:
        self.__model=model
        self.__frame=0
        pass
    
    def set_frame(self):
        self.__model.set_frame(self.__frame)
        self.__frame+=1
        
    def get_frame(self):
        pass
    
    def run(self):
        while True:
            self.set_frame()
            time.sleep(4)