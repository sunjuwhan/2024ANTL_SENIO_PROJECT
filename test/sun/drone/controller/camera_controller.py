import time
import cv2
from model.pilot_model import *
from model.video_mode import *
class CameraController():
    def __init__(self,model:VideoModel,pilot_model:PilotModel) -> None:
        self.__model=model
        self.__cap=model.get_cap()
        self.__pilot_model=pilot_model
        self.__picam2=self.__model.get_picam()
    def set_frame(self):
        now_mode=self.__pilot_model.get_data()[1]
        print(now_mode)
        if(now_mode=="gps" or now_mode =="detection"):
            frame=self.__picam2.capture_array()
            self.__model.set_frame(frame)
        else:
            ret,frame=self.__cap.read()
            self.__model.set_frame(frame)

    def run(self):
        time.sleep(3)
        self.__picam2.start()
        while True:
            self.set_frame()