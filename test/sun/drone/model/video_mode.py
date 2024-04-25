from picamera2 import Picamera2

import cv2
class VideoModel():
    def __init__(self) -> None:
        self.__cap=cv2.VideoCapture(0)
        #self.__cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        #self.__cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.__picam2=Picamera2()
        self.__picam2.preview_configuration.main.size = (640, 480)
        self.__picam2.preview_configuration.main.format = "RGB888"
        self.__picam2.preview_configuration.align()
        self.__picam2.configure("preview")
        self.__frame=None
        self.__image_slice=None
    def set_frame(self,frame): 
        self.__frame=frame
    def get_frame(self):
        return self.__frame
    def get_picam(self) :
        return self.__picam2
    def get_cap(self):
        return self.__cap
    def split_image(self, num_slices):
        slice_height = self.__frame.shape[0] // num_slices
        slices = []
        for i in range(num_slices):
            start = i * slice_height
            end = start + slice_height
            slices.append(self.__frame[start:end, :])
        return slices