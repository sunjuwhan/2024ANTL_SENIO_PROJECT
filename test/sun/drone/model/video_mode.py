import cv2
class VideoModel():
    def __init__(self) -> None:
        self.__cap=cv2.VideoCapture(0)
        self.__ret=None
        self.__frame=None
        self.__d=None
        self.__s=None
        
    def set_frame(self,s): 
        self.__s=s
    def get_frame(self):
        return self.__s
    
    def get_cap(self):
        return self.__cap