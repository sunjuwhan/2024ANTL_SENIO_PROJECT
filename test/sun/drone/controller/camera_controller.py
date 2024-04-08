import time
import cv2

from model.video_mode import *
class CameraController():
    def __init__(self,model:VideoModel) -> None:
        self.__model=model
        self.__cap=model.get_cap()
    def set_frame(self):
        ret,frame=self.__cap.read()
        d=frame.flattend()
        s=d.tostring()
        self.__model.set_frame(s)
    def run(self):
        while True:
            self.set_frame()