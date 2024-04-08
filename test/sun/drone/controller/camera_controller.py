import time
import cv2

from model.video_mode import *
class CameraController():
    def __init__(self,model:VideoModel) -> None:
        self.__model=model
        self.__cap=model.get_cap()
    def set_frame(self):
        ret,frame=self.__cap.read()
        #frame=cv2.resize(frame,(320,240))
        d=frame.flatten()
        s=d.tostring()
        self.__model.set_frame(s)
    def run(self):
        time.sleep(3)
        while True:
            self.set_frame()